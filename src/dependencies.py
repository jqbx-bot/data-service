from typing import Type, Callable

from injector import Binder, singleton

from src.environment import AbstractEnvironment, Environment
from src.file_repository.abstract_file_repository import AbstractFileRepository
from src.file_repository.local_file_repository import LocalFileRepository
from src.file_repository.s3_file_repository import S3FileRepository


def __compose(file_repository: Type[AbstractFileRepository]) -> Callable[[Binder], None]:
    def __configure(binder: Binder) -> None:
        binder.bind(AbstractFileRepository, to=file_repository, scope=singleton)
        binder.bind(AbstractEnvironment, to=Environment, scope=singleton)

    return __configure


def compose_local() -> Callable[[Binder], None]:
    return __compose(LocalFileRepository)


def compose_deployed() -> Callable[[Binder], None]:
    return __compose(S3FileRepository)
