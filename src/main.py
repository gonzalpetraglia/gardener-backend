from flask import Flask
from logging.config import dictConfig

from src.db import create_session_builder
from src.auth.handlers import init_auth

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


def create_app(config=default_config, create_session=create_session_builder()):

    dictConfig(config.get('logger'))

    app = Flask(__name__)

    app.debug = True

    get_current_user, login_required = init_auth(app, create_session)

    @login_required
    @app.route("/logout")
    def logout():
        user_id = get_current_user().id
        return {'status': 'ok', 'user_id': user_id}

    @app.route("/profile")
    @login_required
    def profile():
        user = get_current_user()
        print(user)
        return user.profile()

    @app.route("/healthcheck")
    def hi():
        return {'version': 'v0.0.1'}

    return app
