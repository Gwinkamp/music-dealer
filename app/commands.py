import discord
import random
import ffmpeg_downloader as ffdl
from io import BytesIO
from app.views import SkipView, SelectTrackView
from app.embeds import PlaylistEmbed, SearchEmbed
from core.models import Track, DelayedTrack
from core.exceptions import FFmpegNotFound
from services import MusicStorage, MusicPlayer
from discord.ext.commands import Cog, Context, command


class Commands(Cog):
    """Класс, инкапсулирующий все команды боту"""

    def __init__(self, storage: MusicStorage, player: MusicPlayer):
        super().__init__()
        self.storage = storage
        self.player = player

    async def setup(self):
        if ffdl.ffmpeg_path is None:
            raise FFmpegNotFound()

        await self.storage.setup()

    @command()
    async def join(self, context: Context):
        """Подключиться к голосовому каналу"""
        if not self._is_user_connected_to_voice(context):
            return await context.send('Вы не подключены к голосовому чату')

        await self.player.connect_to(context.author.voice.channel)

    @command()
    async def play(self, context: Context, *, query: str | None):
        """Воспроизвести песню или запустить playlist"""
        if not self.player.is_connected_to_voice_channel:
            await self.join(context)

        if not self.player.is_connected_to_voice_channel:
            return

        if self.player.is_playing:
            return

        if self.player.is_paused:
            self.player.resume()
            return

        if query is None:
            callback = self._create_next_track_default_callback(context)
            return await self.player.run_playlist(callback)

        search_result = await self.storage.search(query)

        async def download_and_play(t: Track):
            t_source = await self.storage.get(t.name)
            t.source = t_source
            await self.player.play(t)

        match len(search_result):
            case 0:
                return await context.send(f'По запросу `{query}` не найдено песен')
            case 1:
                track = search_result.pop()
                await download_and_play(track)
            case _:
                if len(search_result) > 25:
                    return await context.send('Найдено более 25 совпадений. Пожалуйста, конкретизируйте запрос')

                select_view = SelectTrackView(search_result, download_and_play)
                await context.send(view=select_view)

    @command()
    async def playall(self, context: Context):
        """Запустить playlist со всеми песнями в случайном порядке"""
        if not self.player.is_connected_to_voice_channel:
            await self.join(context)

        if not self.player.is_connected_to_voice_channel:
            return

        track_list = await self.storage.get_list()

        random.shuffle(track_list)

        for track in track_list:
            delayed_track = self._create_delayed_track(track)
            self.player.add_to_playlist(delayed_track)

        if not self.player.is_playing:
            callback = self._create_next_track_default_callback(context)
            await self.player.run_playlist(callback)

    @command()
    async def add(self, context: Context, *, query: str):
        """Добавить песню в очередь playlist"""
        search_result = await self.storage.search(query)

        async def add_to_playlist(t: Track):
            delayed_track = self._create_delayed_track(t)
            self.player.add_to_playlist(delayed_track)

        match len(search_result):
            case 0:
                return await context.send(f'По запросу `{query}` не найдено песен')
            case 1:
                track = search_result.pop()
                await add_to_playlist(track)
            case _:
                if len(search_result) > 25:
                    return await context.send('Найдено более 25 совпадений. Пожалуйста, конкретизируйте запрос')

                select_view = SelectTrackView(search_result, add_to_playlist)
                await context.send(view=select_view)

    @command()
    async def queue(self, context: Context):
        """Отобразить очередь playlist"""
        embed = PlaylistEmbed(self.player).create()
        await context.send(embed=embed)

    @command()
    async def search(self, context: Context, *, query: str):
        """Поиск трека"""
        if query is None:
            return await context.send('Не задан параметр для поиска')

        items = await self.storage.search(query)
        embed = SearchEmbed(items).create()
        await context.send(embed=embed)

    @command()
    async def list(self, context: Context):
        """Список доступных песен"""
        files = await self.storage.get_list()

        if len(files) == 0:
            return await context.send('Песен пока что нет')

        message = str()
        for file in files:
            message += file.name + '\n'

        stream = BytesIO(message.encode('utf-8'))
        await context.send('Список всех песен:', file=discord.File(stream, filename='Твоя любимая музыка.txt'))

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
        """Остановить воспроизведение и отключиться от голосового канала"""
        self.player.stop()
        await self.player.disconnect()

    @command()
    async def skip(self, _: Context):
        """Пропустить песню в playlist"""
        self.player.skip()

    @command()
    async def clear(self, _: Context):
        """Очистить playlist"""
        self.player.clear()

    @staticmethod
    def _is_user_connected_to_voice(context: Context):
        return context.author.voice is not None

    def _create_delayed_track(self, track: Track):
        async def source_filling_func():
            return await self.storage.get(track.name)

        return DelayedTrack(
            name=track.name,
            is_playing=track.is_playing,
            source=track.source,
            source_filling_func=source_filling_func
        )

    def _create_next_track_default_callback(self, context: Context):
        """Создать callback, который будет вызываться перед началом воспроизведения песни в playlist`е"""

        async def next_track_callback(t: Track):
            await context.send(f'Сейчас играет: ```{t.name}```', view=SkipView(self.player))

        return next_track_callback
