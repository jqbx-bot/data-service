from flask import Blueprint, jsonify

blueprint = Blueprint('welcome_message', __name__, url_prefix='/welcome_message')


@blueprint.route('/<room_id>')
def get_welcome_message(room_id: str):
    return jsonify({
        'room_id': room_id
    })
