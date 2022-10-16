from typing import List
from core.models import Track
from discord import AudioSource
from abc import ABCMeta, abstractmethod


class MusicStorage(metaclass=ABCMeta):

    @abstractmethod
    async def setup(self) -> None:
        """Выполнение необходимых действий перед началом работы"""
        ...

    @abstractmethod
    async def search(self, query: str) -> List[Track]:
        """Поиск файлов

        :param query: ключевая фраза для поиска
        :returns: список найденных файлов
        """
        ...

    @abstractmethod
    async def get(self, query: str) -> AudioSource | None:
        """Получить трек

        :param query: ключевая фраза для поиска
        :returns: название песни, музыкальный трек
        """

    @abstractmethod
    async def get_list(self) -> List[Track]:
        """Получить список всех песен"""
        ...
