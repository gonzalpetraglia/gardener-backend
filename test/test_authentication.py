from chai import Chai
import pytest


@pytest.mark.usefixtures("clean_user")
class UserRegistrationTests(Chai):

    def test_login_with_native_data_should_return_token(self):

        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            'provider': 'native'
        }
        response = self.client.post('/login', json=login_data)

        self.assert_equal(response.status_code, 200)
        assert isinstance(response.json['access_token'], str)
