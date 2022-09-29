from core.logging import create_default_logger
from discord.ext import commands


class DiscordBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = create_default_logger(__name__)

    async def on_ready(self):
        self.logger.info('Bot is ready!')
