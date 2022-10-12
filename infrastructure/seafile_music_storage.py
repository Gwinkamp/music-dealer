from logging import Logger
from typing import List, Tuple
import ffmpeg_downloader as ffdl
from io import BytesIO
from aseafile import SeafileHttpClient
from aseafile.models import SearchResultItem
from discord import FFmpegPCMAudio
from services import MusicStorage


class SeafileMusicStorage(MusicStorage):

    def __init__(
            self,
            seafile: SeafileHttpClient,
            username: str,
            password: str,
            logger: Logger,
            repo_name: str = 'music'):
        self._seafile = seafile
        self._repo_id = str()
        self._repo_name = repo_name
        self._username = username
        self._password = password
        self._logger = logger

    async def setup(self):
        await self._seafile.authorize(self._username, self._password)
        self._repo_id = await self._get_or_create_repo(self._repo_name)

    async def _get_or_create_repo(self, repo_name: str):
        """Поулчить идентификатор репозитория или создать новый репозиторий для хранения музыки, если его не существует

        :param repo_name: имя репозитория для хранения музыки
        :returns: id репозитория
        """
        response = await self._seafile.get_repos()

        if not response.success:
            self._logger.error('Не удалось получить список репозиториев seafile')
            return

        repos = list(filter(lambda repo_item: repo_item.name == repo_name, response.content))

        if len(repos) == 0:
            response = await self._seafile.create_repo(repo_name)

            if not response.success:
                self._logger.error(f'Не удалось создать репозиторий "{repo_name}" в seafile')
                return

            return response.content.id

        repo = repos.pop()
        return repo.id

    async def search(self, query: str) -> List[SearchResultItem]:
        response = await self._seafile.search_file(query, self._repo_id)

        if not response.success:
            self._logger.error(f'Не удалось получить список файлов по запросу {query}')
            return []

        return response.content

    async def get(self, query: str) -> Tuple[str, FFmpegPCMAudio] | None:
        files = await self.search(query)

        if len(files) == 0:
            return

        file = files.pop()
        response = await self._seafile.download(self._repo_id, file.path)

        if not response.success:
            self._logger.error(f'Не удалось скачать файл "{file.path}" из seafile')
            return

        return (file.path.split('/')[-1],
                FFmpegPCMAudio(BytesIO(response.content), pipe=True, executable=ffdl.ffmpeg_path))
