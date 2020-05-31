import pytest
from chai import Chai
from simple_settings import settings

from src.main import create_app
from src.db import create_session_builder
from src.models.User import User


@pytest.fixture(scope="class")
def create_session():
    return create_session_builder(
            settings.DB_USER,
            settings.DB_PASSWORD,
            settings.DB_HOST,
            settings.DB_PORT,
            settings.DB_NAME
            )


@pytest.fixture(scope="class")
def app(create_session):
    return create_app(create_session=create_session)


@pytest.fixture(scope="class")
def client(app, request):
    client = app.test_client()
    request.cls.client = client
    return client


@pytest.fixture(scope="class")
def user(client):
    rv = client.post('/auth')
    print(rv)


@pytest.fixture(scope="class")
def chai():
    return Chai()


@pytest.fixture(scope="class")
def clean_client(client, create_session, request):
    with create_session() as session:
        session.query(User).delete()

    request.cls.create_session = create_session

    yield

    with create_session() as session:
        session.query(User).delete()


@pytest.fixture(scope="class")
def clean_user(client, clean_client, request):
    data = {
        "username": "rick",
        "password": "1234567890aA!",
        "email": "gmail@gmail.com",
        "is_admin": True
    }

    request.cls.user_data = data
    response = client.post('/user', json=data)

    assert response.status_code == 200
