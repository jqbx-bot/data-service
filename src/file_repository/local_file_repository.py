import os
from pathlib import Path
from typing import Optional

from src.file_repository.abstract_file_repository import AbstractFileRepository


class LocalFileRepository(AbstractFileRepository):
    def get(self, key: str) -> Optional[str]:
        full_path = self.__get_full_path(key)
        if os.path.isfile(full_path):
            with open(full_path, 'r') as f:
                return f.read()
        return None

    def set(self, key: str, content: str) -> None:
        full_path = self.__get_full_path(key)
        Path(os.path.dirname(full_path)).mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w+') as f:
            f.write(content)

    def delete(self, key: str) -> None:
        full_path = self.__get_full_path(key)
        if os.path.isfile(full_path):
            os.remove(full_path)

    @staticmethod
    def __get_full_path(key: str) -> str:
        return os.path.join('.localdatalake', *[x for x in key.split('/') if x])