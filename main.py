import asyncio
import discord
from discord.ext import commands
from core.logging import LoggingStorage
from config import settings
from app import DiscordBot


async def main():
    intents = discord.Intents.default()

    discord.utils.setup_logging(
        handler=LoggingStorage.get_default_handler(),
        root=False)

    async with DiscordBot(commands.when_mentioned, intents=intents) as bot:
        await bot.start(settings.token)


if __name__ == '__main__':
    asyncio.run(main())
