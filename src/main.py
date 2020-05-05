from flask import Flask
from logging.config import dictConfig

from .auth import init_auth, current_user, login_required

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

    app.debug = True
    app.config['SECRET_KEY'] = 'super-secret'

    init_auth(app)

    @login_required
    @app.route("/logout")
    def logout():
        user_id = current_user.id
        return {'status': 'ok', 'user_id': user_id}

    @login_required
    @app.route("/profile2")
    def profile():
        user = current_user
        return user

    @app.route("/healthcheck")
    def hi():
        return 'Im fine'

    return app
