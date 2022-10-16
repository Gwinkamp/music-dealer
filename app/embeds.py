import discord
from typing import List
from services import MusicPlayer
from core.models import Track, DelayedTrack


class PlaylistEmbed:
    """Встроенное сообщение, отображающее состояние playlist`а"""

    MAX_QUEUE_RENDERING_LENGTH = 50

    def __init__(self, player: MusicPlayer):
        self._player = player
        self._embed = discord.Embed(title='Playlist', color=discord.Color.random())

    def create(self):
        if self._player.playing_track is not None:
            self._embed.add_field(
                name='Сейчас играет:',
                value=f'```{self._player.playing_track.name}```',
                inline=False
            )

        if self._player.is_playlist_empty:
            self._embed.add_field(
                name='В очереди:',
                value='```diff\n- пусто\n```',
                inline=False
            )
            return self._embed

        message = '```\n'

        for index, track in enumerate(self._player.playlist):
            if index > self.MAX_QUEUE_RENDERING_LENGTH - 1:
                message += f'и еще {len(self._player.playlist) - self.MAX_QUEUE_RENDERING_LENGTH}...'
                break
            message += f'{index + 1}) {track.name}\n'

        message += '```'
        self._embed.add_field(name='В очереди:', value=message, inline=False)
        return self._embed


class SearchEmbed:
    """Встроенное сообщение, отображающее результат поиска"""

    def __init__(self, tracks_found: List[Track]):
        self._tracks = tracks_found
        self._embed = discord.Embed(
            title='Результат поиска',
            color=discord.Color.random()
        )

    def create(self):
        if len(self._tracks) == 0:
            self._embed.description = 'Совпадения не найдены'
            return self._embed

        self._embed.description = f'Найдены совпадения:\n```\n'
        for index, item in enumerate(self._tracks):
            self._embed.description += f'{index + 1}) {item.name}\n'
        self._embed.description += '```'

        return self._embed
