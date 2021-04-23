from typing import Optional

from flask import Blueprint, jsonify, make_response, request
from injector import inject

from src.app.file_repository.abstract_file_repository import AbstractFileRepository

blueprint = Blueprint('welcome_message', __name__, url_prefix='/welcome_message')


@inject
@blueprint.route('/<room_id>', methods=['GET'])
def get_welcome_message(room_id: str, file_repository: AbstractFileRepository):
    welcome_message = file_repository.get(__get_key(room_id))
    if not welcome_message:
        return make_response(jsonify(None), 404)
    return jsonify({
        'welcome_message': file_repository.get(__get_key(room_id))
    })


@inject
@blueprint.route('/<room_id>', methods=['POST'])
def set_welcome_message(room_id: str, file_repository: AbstractFileRepository):
    body: dict = request.json
    welcome_message: Optional[str] = body.get('welcome_message')
    if not welcome_message:
        return make_response(jsonify(None), 400)
    file_repository.set(__get_key(room_id), welcome_message)
    return make_response(jsonify(None), 201)


@inject
@blueprint.route('/<room_id>', methods=['DELETE'])
def delete_welcome_message(room_id: str, file_repository: AbstractFileRepository):
    file_repository.delete(__get_key(room_id))
    return make_response(jsonify(None), 204)


def __get_key(room_id: str) -> str:
    return 'welcome_message/%s.txt' % room_id
