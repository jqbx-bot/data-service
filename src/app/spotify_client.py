from abc import ABC, abstractmethod
from typing import Optional
import spotipy
from injector import inject

from src.app.environment import AbstractEnvironment


class AbstractSpotifyClient(ABC):
    @abstractmethod
    def relink(self, track_id: str, market: str) -> Optional[str]:
        pass


class SpotifyClient(AbstractSpotifyClient):
    @inject
    def __init__(self, env: AbstractEnvironment):
        self.__env = env
        self.__oauth: Optional[spotipy.oauth2.SpotifyOAuth] = None
        self.__token_info: Optional[dict] = None

    def relink(self, track_id: str, market: str) -> Optional[str]:
        client = self.__get_authenticated_client()
        try:
            return client.track(track_id, market=market).get('external_urls', {}).get('spotify')
        except:
            return None

    def __get_authenticated_client(self) -> spotipy.Spotify:
        if not self.__oauth:
            self.__oauth = spotipy.oauth2.SpotifyOAuth(
                client_id=self.__env.get_spotify_client_id(),
                client_secret=self.__env.get_spotify_client_secret(),
                redirect_uri=self.__env.get_spotify_redirect_uri()
            )
        if not self.__token_info or self.__oauth.is_token_expired(self.__token_info):
            self.__token_info = self.__oauth.refresh_access_token(self.__env.get_spotify_refresh_token())
        return spotipy.Spotify(auth=self.__token_info['access_token'])
