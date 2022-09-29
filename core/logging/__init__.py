import logging
from logging import Logger
from .storage import LoggingStorage
from .handler_factory import LoggingHandlerFactory


def create_default_logger(name: str) -> Logger:
    logger = LoggingStorage.get_logger(name)

    if logger is None:
        logger = logging.getLogger(name)
        logger.addHandler(LoggingStorage.get_default_handler())
        logger.setLevel(logging.DEBUG)

        LoggingStorage.add_logger(logger)

    return logger
