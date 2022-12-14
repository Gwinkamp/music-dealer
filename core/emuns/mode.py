import os
from enum import Enum
from constants import MODE_ENVIRONMENT_VARNAME


class Mode(Enum):
    """Режим работы бота"""

    UNKNOWN = 0

    DEBUG = 1

    PRODUCTION = 2

    @classmethod
    def from_number(cls, number: int):
        match number:
            case 1:
                return cls.DEBUG
            case 2:
                return cls.PRODUCTION
            case _:
                return cls.UNKNOWN

    @classmethod
    def from_alias(cls, alias: str):
        alias = alias.upper()
        match alias:
            case 'DEBUG':
                return cls.DEBUG
            case 'PRODUCTION':
                return cls.PRODUCTION
            case _:
                return cls.UNKNOWN

    @classmethod
    def from_env(cls):
        value = os.environ.get(MODE_ENVIRONMENT_VARNAME, 'DEBUG')

        if value.isdigit():
            return cls.from_number(int(value))
        else:
            return cls.from_alias(value)
