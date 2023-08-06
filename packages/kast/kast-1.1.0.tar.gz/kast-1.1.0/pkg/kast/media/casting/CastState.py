#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from pychromecast.controllers.media import MEDIA_PLAYER_STATE_BUFFERING, MEDIA_PLAYER_STATE_IDLE, \
    MEDIA_PLAYER_STATE_PAUSED, \
    MEDIA_PLAYER_STATE_PLAYING, MEDIA_PLAYER_STATE_UNKNOWN, MediaStatus
from pychromecast.controllers.receiver import CastStatus
from pychromecast.socket_client import CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_CONNECTING, \
    CONNECTION_STATUS_DISCONNECTED, CONNECTION_STATUS_FAILED, CONNECTION_STATUS_FAILED_RESOLVE, CONNECTION_STATUS_LOST, \
    ConnectionStatus

from kast.utils.chrono import Seconds

DeviceName = str
VolumeLevel = float


class CastConnectionState(Enum):
    Connecting = CONNECTION_STATUS_CONNECTING
    Connected = CONNECTION_STATUS_CONNECTED
    Disconnected = CONNECTION_STATUS_DISCONNECTED
    Failed = CONNECTION_STATUS_FAILED
    FailedResolve = CONNECTION_STATUS_FAILED_RESOLVE
    Lost = CONNECTION_STATUS_LOST


class CastPlayerState(Enum):
    Playing = MEDIA_PLAYER_STATE_PLAYING
    Buffering = MEDIA_PLAYER_STATE_BUFFERING
    Paused = MEDIA_PLAYER_STATE_PAUSED
    Idle = MEDIA_PLAYER_STATE_IDLE
    Unknown = MEDIA_PLAYER_STATE_UNKNOWN


@dataclass
class CastCapabilities:
    canPause: bool = False
    canSeek: bool = False
    canSetMute: bool = False
    canSetVolume: bool = False
    canSkipForward: bool = False
    canSkipBackward: bool = False
    canQueueNext: bool = False
    canQueuePrevious: bool = False


@dataclass
class CastMediaState:
    volumeMuted: bool = False
    volumeLevel: VolumeLevel = 1.0
    playerState: CastPlayerState = CastPlayerState.Unknown
    duration: Seconds = Seconds()
    currentTime: Seconds = Seconds()
    title: str = ''
    displayName: str = ''
    iconUrl: str = ''
    imageUrl: str = ''
    contentUrl: Optional[str] = None
    lastPositionUpdateTimestamp: Optional[Seconds] = None

    @property
    def adjustedPosition(self) -> Seconds:
        return self.currentTime + (Seconds(time.time()) - self.lastPositionUpdateTimestamp) \
            if self.lastPositionUpdateTimestamp is not None else self.currentTime

    def isPlaying(self) -> bool:
        return self.playerState in [CastPlayerState.Playing, CastPlayerState.Buffering]

    def isPaused(self) -> bool:
        return self.playerState == CastPlayerState.Paused

    def isStopped(self) -> bool:
        return not self.isPlaying() and not self.isPaused()


@dataclass
class CastState:
    connection: CastConnectionState = CastConnectionState.Disconnected
    deviceName: Optional[DeviceName] = None
    capabilities: CastCapabilities = CastCapabilities()
    mediaState: CastMediaState = CastMediaState()

    def isConnected(self) -> bool:
        return self.connection in [
            CastConnectionState.Connected,
            CastConnectionState.Connecting
        ]

    def isConnectedOrRecoverable(self) -> bool:
        return self.isConnected() \
           or self.connection == CastConnectionState.Lost

    def update(
        self,
        mediaStatus: Optional[MediaStatus] = None,
        castStatus: Optional[CastStatus] = None,
        connectionStatus: Optional[ConnectionStatus] = None
    ) -> None:
        def validateValue(value: Any, defaultValue: Any) -> Any:
            return defaultValue if value is None else value

        if connectionStatus:
            self.connection = CastConnectionState(validateValue(connectionStatus.status, self.connection.value))

        if castStatus:
            self.mediaState.volumeMuted = validateValue(castStatus.volume_muted, self.mediaState.volumeMuted)
            self.mediaState.volumeLevel = validateValue(castStatus.volume_level, self.mediaState.volumeLevel)
            self.mediaState.displayName = validateValue(castStatus.display_name, self.mediaState.displayName)
            self.mediaState.iconUrl = validateValue(castStatus.icon_url, self.mediaState.iconUrl)

        if mediaStatus:
            self.capabilities.canPause = validateValue(mediaStatus.supports_pause, self.capabilities.canPause)
            self.capabilities.canSeek = validateValue(mediaStatus.supports_seek, self.capabilities.canSeek)
            self.capabilities.canSetMute = validateValue(mediaStatus.supports_stream_mute, self.capabilities.canSetMute)
            self.capabilities.canSetVolume = validateValue(mediaStatus.supports_stream_volume, self.capabilities.canSetVolume)
            self.capabilities.canSkipForward = validateValue(mediaStatus.supports_skip_forward, self.capabilities.canSkipForward)
            self.capabilities.canSkipBackward = validateValue(mediaStatus.supports_skip_backward, self.capabilities.canSkipBackward)
            self.capabilities.canQueueNext = validateValue(mediaStatus.supports_queue_next, self.capabilities.canQueueNext)
            self.capabilities.canQueuePrevious = validateValue(mediaStatus.supports_queue_prev, self.capabilities.canQueuePrevious)

            self.mediaState.volumeMuted = validateValue(mediaStatus.volume_muted, self.mediaState.volumeMuted)
            self.mediaState.volumeLevel = validateValue(mediaStatus.volume_level, self.mediaState.volumeLevel)
            self.mediaState.playerState = CastPlayerState(validateValue(mediaStatus.player_state, self.mediaState.playerState.value))
            self.mediaState.duration = Seconds(validateValue(mediaStatus.duration, self.mediaState.duration.value))
            self.mediaState.currentTime = Seconds(validateValue(mediaStatus.adjusted_current_time, self.mediaState.currentTime.value))
            self.mediaState.title = validateValue(mediaStatus.title, self.mediaState.title)
            self.mediaState.imageUrl = validateValue(mediaStatus.images[0].url if mediaStatus.images else '', self.mediaState.imageUrl)
            self.mediaState.contentUrl = validateValue(mediaStatus.content_id, self.mediaState.contentUrl)

            self.mediaState.lastPositionUpdateTimestamp = Seconds(time.time())
