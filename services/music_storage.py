from typing import List, Tuple
from discord import AudioSource
from abc import ABCMeta, abstractmethod


class MusicStorage(metaclass=ABCMeta):

    @abstractmethod
    async def setup(self) -> None:
        """Выполнение необходимых действий перед началом работы"""
        ...

    @abstractmethod
    async def search(self, query: str) -> List:
        """Поиск файлов

        :param query: ключевая фраза для поиска
        :returns: список найденных файлов
        """
        ...

    @abstractmethod
    async def get(self, query: str) -> Tuple[str, AudioSource] | None:
        """Получить трек

        :param query: ключевая фраза для поиска
        :returns: название песни, музыкальный трек
        """
