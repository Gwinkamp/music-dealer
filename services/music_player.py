import time
import asyncio
from typing import Deque
from collections import deque
from core.models import Track
from core.logging import create_default_logger
from discord import VoiceClient, VoiceChannel


class MusicPlayer:

    def __init__(self):
        self._is_stopped = False
        self._voice_client: VoiceClient | None = None
        self._playlist: Deque[Track] = deque()
        self._logger = create_default_logger(__name__)

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

    async def connect_to(self, channel: VoiceChannel):
        self._voice_client = await channel.connect()

    def add_to_playlist(self, track: Track):
        self._playlist.append(track)

    async def run_playlist(self):
        self._is_stopped = False

        while not self.is_playlist_empty:
            if self.is_stopped:
                break

            track = self._playlist.popleft()
            await self.play(track)

    async def play(self, track: Track):

        def callack(e: Exception):
            track.is_playing = False

        self._voice_client.play(track.source, after=callack)

        def wait_until_complete(track: Track):
            track.is_playing = True

            while track.is_playing:
                if self.is_stopped:
                    track.is_running = False
                else:
                    time.sleep(1)

        await asyncio.to_thread(wait_until_complete, track)

    def pause(self):
        self._voice_client.pause()

    def resume(self):
        self._voice_client.resume()

    def stop(self):
        self._is_stopped = True
        self._voice_client.stop()

    async def disconnect(self):
        await self._voice_client.disconnect()
