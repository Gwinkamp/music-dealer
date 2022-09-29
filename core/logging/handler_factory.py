import sys
import logging
from logging import StreamHandler
from constants import (
    LOGGING_DATE_FORMAT,
    LOGGING_MESSAGE_FORMAT,
    LOGGING_MESSAGE_STYLE
)


class LoggingHandlerFactory:
    """Фабрика обработчиков логов"""

    @staticmethod
    def create_default_handler() -> StreamHandler:
        handler = logging.StreamHandler(sys.stdout)

        log_formatter = logging.Formatter(
            fmt=LOGGING_MESSAGE_FORMAT,
            datefmt=LOGGING_DATE_FORMAT,
            style=LOGGING_MESSAGE_STYLE)

        handler.setFormatter(log_formatter)
        return handler
