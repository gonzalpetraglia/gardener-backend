from chai import Chai
import pytest


@pytest.mark.usefixtures("clean_client")
class HealthcheckTest(Chai):
    def test_healthcheck(self):

        response = self.client.get('/healthcheck')
        self.assert_equal({'version': 'v0.0.1'}, response.json)
