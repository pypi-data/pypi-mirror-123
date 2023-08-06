#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from kast.Services import Services
from kast.interface.qt5.dialogs import dialogError, dialogQuestionOkCancel
from kast.interface.qt5.service.BackgroundRunner import BackgroundRunner
from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.service.UiEvent import Progress, UiEvent, UiState
from kast.interface.qt5.service.UiStateService import UiStateService
from kast.media.casting.CastException import CastException
from kast.media.casting.CastState import DeviceName, CastState, CastMediaState
from kast.media.processing.MetaData import MetaData
from kast.media.processing.SubtitleUtils import SubtitleException
from kast.media.processing.SubtitlesSource import SubtitlesFromFile, SubtitlesFromStream
from kast.media.processing.SubtitlesSourceList import SubtitlesSourceList
from kast.media.processing.Transcoder import Codecs, Streams, TranscodeParams, Transcoder
from kast.media.processing.common import StreamId, containerExtension
from kast.utils.Loggable import Loggable
from kast.utils.chrono import Seconds


@dataclass
class StreamParams:
    deviceName: DeviceName
    audioStreamId: StreamId
    subtitlesId: Optional[int] = None


class MediaControlService(Loggable):

    VideoOpenedCallback = Callable[[MetaData], None]
    TaskCallback = Callable[[], None]

    def __init__(
        self,
        services: Services,
        interfaceScheduler: InterfaceScheduler,
        backgroundRunner: BackgroundRunner,
        uiStateService: UiStateService
    ) -> None:
        self._services = services
        self._interfaceScheduler = interfaceScheduler
        self._backgroundRunner = backgroundRunner
        self._uiStateService = uiStateService

        self._videoFilePath: Optional[Path] = None
        self._metaData = MetaData()
        self._subtitlesSourceList = SubtitlesSourceList()
        self._lastStreamParams: Optional[StreamParams] = None
        self._lastTranscodeParams: Optional[TranscodeParams] = None

    @property
    def _castState(self) -> CastState:
        return self._uiStateService.castState

    @property
    def _mediaState(self) -> CastMediaState:
        return self._castState.mediaState

    def playOrPause(self) -> None:
        if self._mediaState.isPlaying():
            self._services.castController.pause()
        else:
            self._services.castController.play()

    def stop(self) -> None:
        self._services.castController.stop()  # TODO: Make it possible to replay movie!

    def seekForward(self) -> None:
        self._services.castController.seekForward()

    def seekBackward(self) -> None:
        self._services.castController.seekBackward()

    def seek(self, position: Seconds) -> None:
        self._services.castController.seek(position)

    def setMute(self, mute: bool = True) -> None:
        self._services.castController.setMute(mute)

    def setVolume(self, value: float) -> None:
        self._services.castController.setVolume(value)

    def openVideo(self, filePath: Path, callback: VideoOpenedCallback) -> None:
        self._videoFilePath = filePath

        self._saveLastMediaDir(filePath)

        self._uiStateService.dispatch(UiEvent(state=UiState.VideoProbe, progress=Progress(complete=False)))

        def interfaceCallback(metaData: MetaData) -> None:
            self._metaData = metaData

            self._subtitlesSourceList.clear()
            for streamId in range(len(metaData.subtitleStreamLangs)):
                self._subtitlesSourceList.append(SubtitlesFromStream(
                    mediaProcessingService=self._services.mediaProcessingService,
                    mediaFile=filePath,
                    streamId=streamId
                ))

            callback(metaData)

            self._uiStateService.dispatch(UiEvent(state=UiState.Idle))

        def backgroundTask() -> None:
            metaData = self._services.mediaProcessingService.extractMetaData(inputFile=filePath)
            self._interfaceScheduler.schedule(lambda: interfaceCallback(metaData))

        self._backgroundRunner.execute(backgroundTask)

    def addSubtitles(self, filePath: Path) -> None:
        self._saveLastMediaDir(filePath)

        self._subtitlesSourceList.append(SubtitlesFromFile(
            mediaProcessingService=self._services.mediaProcessingService,
            subtitlesFile=filePath
        ))

    def startStream(
        self,
        deviceName: DeviceName,
        audioStreamId: StreamId,
        subtitlesId: Optional[int] = None
    ) -> None:
        if not self._videoFilePath:
            dialogError("No video file has been selected!")
            return

        self._lastStreamParams = StreamParams(deviceName, audioStreamId, subtitlesId)

        self._uiStateService.dispatch(UiEvent(state=UiState.Preprocessing, progress=Progress(complete=False)))

        self._runInBackground(self._initTranscoding)

    def _initTranscoding(self) -> None:
        cancelEvent = threading.Event()

        def progressCallback(percent: int, complete: bool) -> None:
            self.log.info(f"Transcoding progress: {percent}% ({'Complete' if complete else 'Running'})")
            self._uiStateService.dispatch(UiEvent(state=UiState.AvProcessing, progress=Progress(
                complete=complete, percentage=percent, cancelEvent=cancelEvent
            )))

        castController = self._services.castController

        inputContainer = containerExtension(self._videoFilePath)
        outputContainer = inputContainer if inputContainer in castController.supportedContainerFormats \
            else castController.preferredContainerFormat

        outputCodecNames = Codecs(
            video=castController.preferredVideoCodec,
            audio=castController.preferredAudioCodec
        )

        transcoder = self._services.mediaProcessingService.createTranscoder(
            inputFile=self._videoFilePath,
            inputStreamIds=Streams(video=0, audio=self._lastStreamParams.audioStreamId),
            outputCodecNames=outputCodecNames,
            containerFormat=outputContainer,
            progressCallback=progressCallback,
            cancelEvent=cancelEvent
        )
        self.log.info(f"Input file: container='{inputContainer}', codecs={transcoder.inputCodecNames}")
        self.log.info(f"Output file: container='{outputContainer}', codecs={transcoder.outputCodecNames}")
        if transcoder.requireProcessing and self._lastTranscodeParams != transcoder.params:
            self._runInForeground(lambda: self._confirmTranscoding(transcoder))
            return

        self._startStreaming(transcoder.outputFile)

    def _confirmTranscoding(self, transcoder: Transcoder) -> None:
        message = "Selected media is not supported in it's current form. " \
            "Either because of a codec mismatch or not supported media container type. " \
            "Your file can be transcoded or remuxed to address those issues respectively.\n" \
            "\n" \
            "Remuxing is a quick process. While duration of transcoding varies. " \
            "It is usually fast for audio codecs and can take some time for video codecs. " \
            "Actual times will depend on your machine processing power.\n" \
            "\n" \
            "Provided Container -> Supported Container:\n" \
            f"- {containerExtension(transcoder.inputFile)} -> {containerExtension(transcoder.outputFile)}\n" \
            "\n" \
            "Provided Codecs -> Supported Codecs:\n" \
            f"- Video: '{transcoder.inputCodecNames.video}' -> '{transcoder.outputCodecNames.video}'\n" \
            f"- Audio: '{transcoder.inputCodecNames.audio}' -> '{transcoder.outputCodecNames.audio}'\n" \
            "\n" \
            "Proceed with media processing?\n" \
            "(Your original file will not be modified.)\n"

        if not dialogQuestionOkCancel(title="Media Processing", message=message):
            self._cancelAction()
            return

        self._runInBackground(lambda: self._startTranscoding(transcoder))

    def _startTranscoding(self, transcoder: Transcoder) -> None:
        if not transcoder.run():
            self._cancelAction()
            return

        self._lastTranscodeParams = transcoder.params

        self._runInForeground(lambda: self._confirmStreaming(transcoder.outputFile))

    def _confirmStreaming(self, videoFile: Path) -> None:
        message = "Media processing finished!\n\nProceed with streaming?\n"

        if not dialogQuestionOkCancel(title="Streaming", message=message):
            self._cancelAction()
            return

        self._runInBackground(lambda: self._startStreaming(videoFile))

    def _startStreaming(self, videoFile: Path) -> None:
        mediaContent = self._services.mediaServer.mediaContent
        mediaContent.movieFile = videoFile
        mediaContent.subtitlesFile = self._getSubtitlesFilePath()

        self._uiStateService.dispatch(UiEvent(state=UiState.Connecting, progress=Progress(complete=False)))

        self._services.castController.connect(name=self._lastStreamParams.deviceName)
        self._services.castController.stream(
            movieUrl=self._services.mediaServer.movieUrl,
            subtitlesUrl=self._services.mediaServer.subtitleUrl,
            thumbnailUrl=self._services.mediaServer.thumbnailUrl,
            title=self._metaData.title
        )

        self._uiStateService.dispatch(UiEvent(state=UiState.Streaming))

    def _getSubtitlesFilePath(self) -> Optional[Path]:
        subtitlesId = self._lastStreamParams.subtitlesId
        return self._subtitlesSourceList[subtitlesId].toVtt() if subtitlesId is not None else None

    def _cancelAction(self) -> None:
        self._uiStateService.dispatch(UiEvent(state=UiState.Idle))

    def _runInForeground(self, callback: TaskCallback) -> None:
        self._interfaceScheduler.schedule(callback)

    def _runInBackground(self, callback: TaskCallback) -> None:
        def backgroundCallback() -> None:
            try:
                callback()
            except (SubtitleException, CastException) as ex:
                message = str(ex)  # Workaround for a 'free variable referenced before assignment' problem.
                self.log.exception(ex)
                self._reportError(message)

        self._backgroundRunner.execute(backgroundCallback)

    def _reportError(self, message) -> None:
        def interfaceCallback() -> None:
            dialogError(message=message)
            self._uiStateService.dispatch(UiEvent(state=UiState.Idle), synchronous=True)

        self._interfaceScheduler.schedule(interfaceCallback)

    def _saveLastMediaDir(self, filePath) -> None:
        self._services.settings.browseMediaDir = filePath.parent
