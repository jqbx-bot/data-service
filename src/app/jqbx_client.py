from abc import ABC, abstractmethod

import requests


class AbstractJqbxClient(ABC):
    @abstractmethod
    def get_room_info(self, room_id: str) -> dict:
        pass


class JqbxClient(AbstractJqbxClient):
    def get_room_info(self, room_id: str) -> dict:
        return requests.get('https://jqbx.fm/room/%s' % room_id).json()
