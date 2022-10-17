import discord
import random
from core.models import Track
from services import MusicPlayer, MusicStorage
from typing import List, Dict, Callable, Coroutine


class SkipView(discord.ui.View):
    """Представление кнопки для пропуска трека"""

    def __init__(self, player: MusicPlayer):
        super().__init__()
        self._player = player

    @discord.ui.button(label='skip', style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._player.skip()
        button.style = discord.ButtonStyle.gray
        button.disabled = True
        await interaction.response.edit_message(view=self)


class TrackSelector(discord.ui.Select):
    """Представление списка для выбора трека"""

    EMOJIS = ['🟩', '🟥', '🟦', '🟨', '🟧', '🟪']

    def __init__(
            self,
            tracks: List[Track],
            callback: Callable[[Track], Coroutine]):
        self._callback = callback
        self._tracks: Dict[str, Track] = dict()

        for track in tracks:
            self._tracks[track.name] = track

        options = [discord.SelectOption(label=track.name, emoji=random.choice(self.EMOJIS)) for track in tracks]

        super().__init__(
            placeholder=f'Найдено {len(tracks)} совпадений. Выберите из списка...',
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """Играть выбранную песню"""
        if not self.disabled:
            self.disabled = True

            track_name = self.values[0]
            track = self._tracks[track_name]

            await interaction.response.send_message(f'Выбрана песня ```{track_name}```')
            await self._callback(track)
        else:
            await interaction.response.send_message(f'Песня уже была выбрана')


class SelectTrackView(discord.ui.View):

    def __init__(
            self,
            tracks: List[Track],
            callback: Callable[[Track], Coroutine]
    ):
        super().__init__()
        self.selector = TrackSelector(tracks, callback)
        self.add_item(self.selector)
