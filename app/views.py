import discord
from services import MusicPlayer


class SkipView(discord.ui.View):
    """Представление кнопки для пропуска трека"""

    def __init__(self, track_name: str, player: MusicPlayer):
        super().__init__()
        self._player = player
        self._track_name = track_name

    @discord.ui.button(label='skip', style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self._player.playing_track.name != self._track_name:
            return await interaction.response.send_message('Трек уже неактуален', ephemeral=True)

        self._player.skip()
        button.style = discord.ButtonStyle.gray
        button.disabled = True
        await interaction.response.edit_message(view=self)
