from flask_jwt import JWT, jwt_required, current_identity

from .User import User


def init_auth(app):

    def authenticate(username, password):
        app.logger.info(password)
        return User(1, 'a', 'ee.cm', 'aaaa', is_admin=False)

    def identity(payload):
        user_id = payload['identity']
        return User(user_id, 'a', 'ee.cm', 'aaaa', is_admin=False)

    JWT(
        app,
        identity_handler=identity,
        authentication_handler=authenticate
        )


login_required = jwt_required
current_user = current_identity
