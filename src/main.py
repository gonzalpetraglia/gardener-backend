from flask import Flask
from logging.config import dictConfig
from simple_settings import settings

from src.db import create_session_builder
from src.auth.handlers import init_auth


def create_app(
    config=settings.as_dict(),
    create_session=create_session_builder(
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        settings.DB_PORT,
        settings.DB_NAME
    )
):

    dictConfig(config['LOGGER'])

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
