import json
from logging import Logger
from core.models import Track
from services import MusicStorage, MusicPlayer
from discord.ext.commands import Cog, Context, command


class Commands(Cog):
    """Класс, инкапсулирующий все команды боту"""

    def __init__(self, storage: MusicStorage, player: MusicPlayer, logger: Logger):
        super().__init__()
        self.logger = logger
        self.storage = storage
        self.player = player

    async def setup(self):
        await self.storage.setup()

    @command()
    async def join(self, context: Context):
        """Подключиться к голосовому каналу"""
        await self.player.connect_to(context.author.voice.channel)

    @command()
    async def play(self, context: Context, *, query: str | None):
        """Воспроизвести песню или запустить playlist"""
        if not self.player.is_connected_to_voice_channel:
            await self.player.connect_to(context.author.voice.channel)

        if self.player.is_playing:
            return

        if self.player.is_paused:
            self.player.resume()
            return

        if query is None:
            return await self.player.run_playlist()

        track_meta = await self.storage.get(query)
        if track_meta is None:
            return await context.send(f'Песня по запросу "{query}" не найдена')

        track_name, track_source = track_meta
        track = Track(
            name=track_name,
            is_playing=False,
            source=track_source
        )

        await self.player.play(track)

    @command()
    async def add(self, context: Context, *, track_name: str):
        """Добавить песню в очередь playlist"""
        track_meta = await self.storage.get(track_name)
        if track_meta is None:
            await context.send(f'Песня с названием "{track_name}" не найдена')

        track_name, track_source = track_meta
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
            return await context.send('`Playlist пуст`')

        message = '```\nТекущий Playlist:\n'
        for track in self.player.playlist:
            message += f' * {track.name}\n'

        message += '```'

        await context.send(message)

    @command()
    async def search(self, context: Context, *, query: str):
        """Поиск трека"""
        if query is None:
            return await context.send('Не задан параметр для поиска')

        result = await self.storage.search(query)
        items = [{
            'name': item.path.split('/')[-1],
            'size': item.size,
            'updated': item.mtime.isoformat()
        } for item in result]
        return await context.send(f'```\n{json.dumps(items, indent=2)}\n```')

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