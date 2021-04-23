import traceback

from flask import Flask, Response
from flask_cors import CORS
from injector import inject

from src.app.blueprints.welcome_message import blueprint as welcome_message
from src.app.logger import AbstractLogger

app = Flask(__name__)
CORS(app)
app.register_blueprint(welcome_message)


@inject
@app.errorhandler(500)
def __error(exception: Exception, logger: AbstractLogger):
    logger.error(exception)
    return Response(traceback.format_exc(), status=500, mimetype='application/text')
