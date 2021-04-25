from abc import ABC, abstractmethod
from typing import Optional, List
import spotipy
from injector import inject

from src.app.environment import AbstractEnvironment


class AbstractSpotifyClient(ABC):
    @abstractmethod
    def relink(self, track_id: str, market: str) -> Optional[str]:
        pass

    @abstractmethod
    def create_playlist(self, name: str, description: str) -> str:
        pass

    @abstractmethod
    def add_to_playlist(self, playlist_id: str, track_id: str) -> None:
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
            track = client.track(track_id, market=market)
        except:
            return None
        if track_id in track.get('uri'):
            return None
        return track.get('external_urls', {}).get('spotify')

    def create_playlist(self, name: str, description: str) -> str:
        client = self.__get_authenticated_client()
        return client.user_playlist_create(
            self.__env.get_spotify_user_id(), name=name, description=description
        )['id']

    def add_to_playlist(self, playlist_id: str, track_id: str) -> None:
        client = self.__get_authenticated_client()
        client.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
        client.playlist_add_items(playlist_id, [track_id], 0)
        track_ids_to_keep: List[str] = [
            x['track']['id'] for x in
            client.playlist_items(playlist_id, limit=100)['items']
        ]
        client.playlist_replace_items(playlist_id, track_ids_to_keep)

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
