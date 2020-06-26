from pytest import fixture


@fixture
def urls():
    prefix = 'http://localhost:5000/api/v1'
    return {
        'session': prefix + '/session',
        'user_get': prefix + '/user/' + 'user_id',
        'user_post': prefix + '/user/',
    }
