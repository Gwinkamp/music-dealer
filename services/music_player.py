import time
import asyncio
from logging import Logger
from typing import Deque
from collections import deque
from core.models import Track, DelayedTrack
from discord import VoiceClient, VoiceChannel


class MusicPlayer:

    def __init__(self, logger: Logger):
        self._is_stopped = False
        self._is_skipped = False
        self._voice_client: VoiceClient | None = None
        self._playlist: Deque[Track | DelayedTrack] = deque()
        self._playing_track: Track | None = None
        self._logger = logger

    @property
    def is_connected_to_voice_channel(self):
        return self._voice_client is not None

    @property
    def is_playing(self):
        if self.is_connected_to_voice_channel:
            return self._voice_client.is_playing()
        else:
            return False

    @property
    def is_paused(self):
        if self.is_connected_to_voice_channel:
            return self._voice_client.is_paused()
        else:
            return False

    @property
    def is_stopped(self):
        return self._is_stopped

    @property
    def is_playlist_empty(self):
        return len(self._playlist) == 0

    @property
    def playlist(self):
        return self._playlist

    @property
    def playing_track(self):
        return self._playing_track

    async def connect_to(self, channel: VoiceChannel):
        self._voice_client = await channel.connect()

    def add_to_playlist(self, delayed_track: DelayedTrack):
        self._playlist.append(delayed_track)

    async def run_playlist(self):
        self._is_stopped = False

        while not self.is_playlist_empty:
            if self.is_stopped:
                break

            track = self._playlist.popleft()

            if track.source is None:
                track.source = await track.source_filling_func()

            await self.play(track)

    async def play(self, track: Track):
        self._is_skipped = False

        def callack(e: Exception):
            track.is_playing = False

        self._voice_client.play(track.source, after=callack)
        self._playing_track = track

        def wait_until_complete(t: Track):
            t.is_playing = True

            while t.is_playing:
                if self.is_stopped or self._is_skipped:
                    t.is_playing = False
                else:
                    time.sleep(1)

        await asyncio.to_thread(wait_until_complete, track)
        self._playing_track = None

    def pause(self):
        if self.is_connected_to_voice_channel:
            self._voice_client.pause()

    def resume(self):
        if self.is_connected_to_voice_channel:
            self._voice_client.resume()

    def stop(self):
        if self.is_connected_to_voice_channel:
            self._is_stopped = True
            self._voice_client.stop()

    def skip(self):
        if self.is_connected_to_voice_channel:
            self._is_skipped = True
            self._voice_client.stop()

    def clear(self):
        self._playlist.clear()

    async def disconnect(self):
        if self.is_connected_to_voice_channel:
            await self._voice_client.disconnect()
