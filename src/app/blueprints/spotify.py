from flask import Blueprint, jsonify, request, make_response
from injector import inject

from src.app.file_repository.abstract_file_repository import AbstractFileRepository
from src.app.jqbx_client import AbstractJqbxClient
from src.app.spotify_client import AbstractSpotifyClient

blueprint = Blueprint('spotify', __name__, url_prefix='/spotify')


@inject
@blueprint.route('/relink/<track_id>', methods=['GET'])
def relink(track_id: str, spotify_client: AbstractSpotifyClient):
    markets = [x for x in request.args.get('markets', '').split(',') if x]
    if not markets:
        return make_response('Missing required "markets" query parameter', 400)
    unfiltered = {x: spotify_client.relink(track_id, x) for x in markets}
    filtered = {k: v for k, v in unfiltered.items() if v}
    if not filtered:
        return make_response(jsonify(None), 404)
    return jsonify(filtered)


@inject
@blueprint.route('/favorite/<room_id>/<track_id>', methods=['POST'])
def add_track_to_favorites(room_id: str, track_id: str, spotify_client: AbstractSpotifyClient,
                           file_repository: AbstractFileRepository, jqbx_client: AbstractJqbxClient):
    playlist_id = file_repository.get(__get_playlist_id_key(room_id))
    if not playlist_id:
        room_info = jqbx_client.get_room_info(room_id)
        room_title = room_info.get('title')
        playlist_id = spotify_client.create_playlist(
            'JQBX :: %s :: Favorites' % room_title,
            'Tracks that %s rocked out to' % room_title
        )
        file_repository.set(__get_playlist_id_key(room_id), playlist_id)
    spotify_client.add_to_playlist(playlist_id, track_id)
    return jsonify({
        'playlist_id': playlist_id
    })


def __get_playlist_id_key(room_id: str) -> str:
    return 'playlist_id/%s.txt' % room_id
