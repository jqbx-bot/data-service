from typing import Optional

import boto3
from botocore.exceptions import ClientError
from injector import inject

from src.app.environment import AbstractEnvironment
from src.app.file_repository.abstract_file_repository import AbstractFileRepository


class S3FileRepository(AbstractFileRepository):
    @inject
    def __init__(self, env: AbstractEnvironment):
        self.__bucket = boto3.resource('s3').Bucket(env.get_s3_bucket())

    def get(self, key: str) -> Optional[str]:
        try:
            return self.__bucket.Object(key).get()['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            raise

    def set(self, key: str, content: str) -> None:
        self.__bucket.Object(key).put(Body=content)

    def delete(self, key: str) -> None:
        try:
            self.__bucket.Object(key).delete()
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return
            raise
