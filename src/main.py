from typing import Any

from flask import Flask
from flask_cors import CORS
from src.welcome_message import blueprint as welcome_message
import awsgi

app = Flask(__name__)
CORS(app)
app.register_blueprint(welcome_message)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
