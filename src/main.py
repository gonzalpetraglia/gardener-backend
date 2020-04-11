from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity, logout_user

from .User import User


from logging.config import dictConfig

default_config = {
     'logger': {
            'version': 1,
            'formatters': {'default': {
                'format':
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }},
            'handlers': {'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            }
        }
    }


def create_app(config=default_config):

    dictConfig(config.get('logger'))

    app = Flask(__name__)

    def authenticate(username, password):
        app.logger.info(password)
        return User(1, 'a', 'ee.cm', 'aaaa', is_admin=False)

    def identity(payload):
        user_id = payload['identity']
        return User(user_id, 'a', 'ee.cm', 'aaaa', is_admin=False)

    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'super-secret'

    JWT(
        app,
        identity_handler=identity,
        authentication_handler=authenticate
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return "{}".format(current_identity.name)

    @app.route("/logout")
    @jwt_required
    def logout():
        logout_user()
        return 'ok'

    @app.route("/healthcheck")
    def hi():
        return 'Im fine'

    return app
