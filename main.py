import asyncio
import discord
from aseafile import SeafileHttpClient
from discord.ext import commands
from config import settings
from app import DiscordBot, Commands
from core.logging import create_default_logger, LoggingStorage
from infrastructure import SeafileMusicStorage
from containers import Container
from dependency_injector import providers
from dependency_injector.wiring import Provide, inject


@inject
async def main(commands_cog: Commands = Provide[Container.commands]):
    intents = discord.Intents.default()
    await commands_cog.setup()

    discord.utils.setup_logging(
        handler=LoggingStorage.get_default_handler(),
        root=False)

    async with DiscordBot(commands.when_mentioned, intents=intents) as bot:
        await bot.add_cog(commands_cog)
        await bot.start(settings.token)


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    container.music_storage.override(
        providers.Factory(
            SeafileMusicStorage,
            seafile=SeafileHttpClient(base_url=settings.seafile.base_url),
            username=settings.seafile.username,
            password=settings.seafile.password,
            logger=create_default_logger('music_storage')
        )
    )

    asyncio.run(main())
