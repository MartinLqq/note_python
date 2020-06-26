import pytest
import requests


@pytest.mark.unit
class TestUser:

    def test_user_get(self, urls):
        resp = requests.get(urls['user_get'],)
        assert resp.ok

    def test_user_post(self, urls):
        data = {
            'username': 'Martin',
            'password': '123456',
            'password_confirm': '123456',
            'email': 'xxx@yyy.com'
        }
        resp = requests.post(urls['user_post'], data)
        assert resp.ok
