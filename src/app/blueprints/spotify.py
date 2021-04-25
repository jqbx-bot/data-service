from flask import Blueprint, jsonify, request, make_response
from injector import inject

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
