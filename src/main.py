from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector

from src.dependencies import compose_local, compose_deployed
from src.welcome_message import blueprint as welcome_message
import awsgi

app = Flask(__name__)
CORS(app)
app.register_blueprint(welcome_message)


def lambda_handler(event, context):
    FlaskInjector(app=app, modules=[compose_deployed()])
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    FlaskInjector(app=app, modules=[compose_local()])
    app.run(port=8080, debug=True)
