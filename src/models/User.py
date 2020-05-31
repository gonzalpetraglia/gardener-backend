from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Boolean

from src.models.Base import Base


class User(Base):
    __tablename__ = 'user'

    username = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)

    def __init__(self, username, password, email=None, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @property
    def id(self):
        return self.username

    def profile(self):
        return {
            'id': self.username,
            'username': self.username,
            'email': self.email
            }
