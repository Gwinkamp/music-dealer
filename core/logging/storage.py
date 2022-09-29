from .handler_factory import LoggingHandlerFactory
from logging import Handler, Logger


class LoggingStorage:

    LOGGING = {
        'loggers': {},
        'handlers': {
            'default': LoggingHandlerFactory.create_default_handler()
        }
    }

    @classmethod
    def get_default_handler(cls) -> Handler:
        return cls.LOGGING['handlers']['default']

    @classmethod
    def get_logger(cls, name: str) -> Logger | None:
        if name in cls.LOGGING['loggers']:
            return cls.LOGGING['loggers'][name]
        return None

    @classmethod
    def add_logger(cls, logger: Logger):
        cls.LOGGING['loggers'][logger.name] = logger
