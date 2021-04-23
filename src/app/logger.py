import json
import traceback
from abc import ABC, abstractmethod
from typing import Union, Optional


class AbstractLogger(ABC):
    @abstractmethod
    def info(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        pass

    @abstractmethod
    def error(self, exception: BaseException) -> None:
        pass


class Logger(AbstractLogger):
    def info(self, context: str, data: Optional[Union[str, dict, list]] = None) -> None:
        log = {
            'level': 'INFO',
            'context': context
        }
        if data:
            log['data'] = data
        print(json.dumps(log))

    def error(self, exception: BaseException) -> None:
        print(json.dumps({
            'level': 'ERROR',
            'error': str(exception),
            'trace': traceback.format_tb(exception.__traceback__)
        }))
