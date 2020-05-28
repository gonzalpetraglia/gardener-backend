from chai import Chai
import pytest


@pytest.mark.usefixtures("clean_client")
class UserRegistrationTests(Chai):

    def test_register_new_user(self):
        data = {
            "username": "rick",
            "password": "1234567890aA!",
            "email": "gmail@gmail.com",
            "is_admin": True
        }
        response = self.client.post('/user', json=data)
        self.assert_equal({'status': 'ok'}, response.json)
        self.assert_equal(200, response.status_code)

    def test_register_new_user_with_same_name_should_fail(self):
        data = {
            "username": "rick",
            "password": "1234567890aA!",
            "email": "gmail@gmail.com",
            "is_admin": True
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'already_used_username'},
            response.json
            )
        self.assert_equal(400, response.status_code)

    def test_register_with_unrecognized_key_should_fail(self):
        data = {
            "username": "joe",
            "password": "1234567890aA!",
            "email": "gmail@gmail.com",
            "is_admin": True,
            "extra_param_not_used": 1
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'unrecognized_key'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_without_email_and_is_admin_should_succeed(self):
        data = {
            "username": "joe2",
            "password": "1234567890aA!"
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'ok'},
            response.json
            )
        self.assert_equal(200, response.status_code)

    def test_register_without_username_should_fail(self):
        data = {
            "password": "1234567890aA!",
            "email": "gmail@gmail.com",
            "is_admin": True
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'missing_key'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_without_password_should_fail(self):
        data = {
            "username": "joe",
            "email": "gmail@gmail.com",
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'missing_key'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_with_insecure_password_should_fail(self):
        data = {
            "username": "joe",
            "password": "1234",
            "email": "gmail@gmail.com",
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'insecure_password'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_with_invalid_email_should_fail(self):
        data = {
            "username": "joe",
            "password": "1234567890aA!",
            "email": "gmailgmail.com",
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'invalid_email'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_with_username_of_wrong_type_should_fail(self):
        data = {
            "username": 1,
            "password": "1234567890aA!",
            "email": "gmail@gmail.com",
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'unexpected_type'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_with_password_of_wrong_type_should_fail(self):
        data = {
            "username": "joe2",
            "password": 1,
            "email": "gmail@gmail.com",
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'unexpected_type'},
            response.json
            )
        self.assert_equal(401, response.status_code)

    def test_register_with_email_of_wrong_type_should_fail(self):
        data = {
            "username": "joe",
            "password": "1234567890aA!",
            "email": 1,
            "is_admin": True,
        }
        response = self.client.post('/user', json=data)
        self.assert_equal(
            {'status': 'error', 'msg': 'unexpected_type'},
            response.json
            )
        self.assert_equal(401, response.status_code)
