from abc import ABC, abstractmethod
from dotenv import load_dotenv
from os import environ

load_dotenv()


class AbstractEnvironment(ABC):
    @abstractmethod
    def get_s3_bucket(self) -> str:
        pass


class Environment(AbstractEnvironment):
    def get_s3_bucket(self) -> str:
        return environ.get('S3_BUCKET')
