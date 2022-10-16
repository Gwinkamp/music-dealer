from dependency_injector import containers, providers
from app.commands import Commands
from core.logging import create_default_logger
from services import MusicPlayer, MusicStorage


class Container(containers.DeclarativeContainer):

    music_player = providers.Singleton(
        MusicPlayer,
        logger=create_default_logger('music_player')
    )

    music_storage = providers.AbstractFactory(MusicStorage)

    commands = providers.Singleton(
        Commands,
        storage=music_storage,
        player=music_player
    )

