from flask import request, jsonify
from schema import (
    Schema,
    Optional,
    SchemaWrongKeyError,
    SchemaMissingKeyError,
    SchemaError,
    Regex,
    And,
    Or
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy.exc import IntegrityError

from src.models.User import User

from src.auth.errors import UserNotFound, IncorrectPassword, \
    ProviderNotImplemented


def init_auth(app, create_session): # noqa

    # Setup the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

    login_schema = Schema(
        {
            'username': str,
            'password': str,
            'provider': Or('native')
        }
    )

    @app.route('/login', methods=['POST'])
    def login():
        with create_session() as session:

            login_schema.validate(request.json)
            # work with session
            username = request.json['username']
            password = request.json['password']
            provider = request.json['provider']

            user = session.query(User).get(username)
            if user is None:
                raise UserNotFound()
            if provider == 'native':
                if not user.check_password(password):
                    raise IncorrectPassword()
                access_token = create_access_token(identity=username)
                return jsonify(access_token=access_token), 200
            else:
                raise ProviderNotImplemented()

    def identity(payload):

        print(payload)
        username = payload['identity']

        session = create_session()
        # work with session
        user = session.query(User).get(username)

        return user

    JWTManager(app)

    password_regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})' # noqa
    email_regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$' # noqa
    initial_profile_schema = Schema(
        {
            'username': str,
            'password': And(
                str,
                Regex(password_regex, error='insecure_password')
            ),
            Optional('email'): Optional(And(
                str,
                Regex(email_regex, error='invalid_email')
            )),
            Optional('is_admin'): Optional(
                bool),
        },
        ignore_extra_keys=False,
        )

    @app.route('/user', methods=['POST'])
    def create_user():
        user_data = request.json

        try:
            initial_profile_schema.validate(user_data)

            with create_session() as session:
                new_user = User(**user_data)
                session.add(new_user)
        except IntegrityError:
            return {'status': 'error', 'msg': 'already_used_username'}, 400

        except SchemaWrongKeyError:
            return {'status': 'error', 'msg': 'unrecognized_key'}, 401

        except SchemaMissingKeyError:
            return {'status': 'error', 'msg': 'missing_key'}, 401

        except SchemaError as e:
            if 'should be' in e.code:
                return {'status': 'error', 'msg': 'unexpected_type'}, 401
            else:
                return {'status': 'error', 'msg': e.code}, 401
        return {'status': 'ok'}

    def get_current_user():
        username = get_jwt_identity()
        with create_session() as session:
            user = session.query(User).get(username)
        return user

    return get_current_user, jwt_required
