from core.models import Track
from core.logging import create_default_logger
from services import MusicStorage, MusicPlayer
from discord.ext.commands import Cog, Context, command


class ControlCog(Cog):
    """Класс, инкапсулирующий все команы боту"""

    def __init__(self):
        super().__init__()
        self.logger = create_default_logger(__name__)
        self.storage = MusicStorage()
        self.player = MusicPlayer()

    @command()
    async def join(self, context: Context):
        """Подключиться к голосовому каналу"""
        await self.player.connect_to(context.author.voice.channel)

    @command()
    async def play(self, context: Context, *, track_name: str | None):
        """Воспроизвести песню или запустить playlist"""
        if not self.player.is_connected_to_voice_channel:
            await self.player.connect_to(context.author.voice.channel)

        if self.player.is_playing:
            return

        if self.player.is_paused:
            self.player.resume()
            return

        if track_name is None:
            return await self.player.run_playlist()

        track_source = self.storage.get(track_name)
        if track_source is None:
            context.send(f'Песня с названием "{track_name}" не найдена')

        track = Track(
            name=track_name,
            is_playing=False,
            source=track_source
        )

        await self.player.play(track)

    @command()
    async def add(self, context: Context, *, track_name: str):
        """Добавить песню в очередь playlist"""
        track_source = self.storage.get(track_name)
        if track_source is None:
            context.send(f'Песня с названием "{track_name}" не найдена')

        track = Track(
            name=track_name,
            is_playing=False,
            source=track_source
        )

        self.player.add_to_playlist(track)

    @command()
    async def queue(self, context: Context):
        """Отобразить очередь playlist"""
        if self.player.is_playlist_empty:
            return await context.send('> Playlist пуст')

        message = '> Текущий Playlist:\n'
        for track in self.player.playlist:
            message += f'> * {track.name}\n'

        await context.send(message)

    @command()
    async def pause(self, _: Context):
        """Поставить воспроизведение на паузу"""
        self.player.pause()

    @command()
    async def resume(self, _: Context):
        """Возобновить воспроизведение"""
        self.player.resume()

    @command()
    async def stop(self, _: Context):
        """Остановить воспроизведение"""
        self.player.stop()

    @command()
    async def disconnect(self, _: Context):
        """Останвоить воспроизведение и отключиться от голосового канала"""
        self.player.stop()
        await self.player.disconnect()
