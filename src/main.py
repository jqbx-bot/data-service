from flask_injector import FlaskInjector

from src.app.app import app
from src.dependencies import compose_local, compose_deployed
import awsgi


def lambda_handler(event, context):
    FlaskInjector(app=app, modules=[compose_deployed()])
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    FlaskInjector(app=app, modules=[compose_local()])
    app.run(port=8080, debug=True)
