from abc import ABC, abstractmethod
from typing import Optional


class AbstractFileRepository(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def set(self, key: str, content: str) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


