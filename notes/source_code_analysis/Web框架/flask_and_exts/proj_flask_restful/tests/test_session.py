import pytest
import requests


@pytest.mark.unit
class TestSession:

    def test_login(self, urls):
        data = {
            'username': 'Martin',
            'password': 123456,
        }
        resp = requests.post(urls['session'], data)
        print(resp.content)
        assert resp.ok
