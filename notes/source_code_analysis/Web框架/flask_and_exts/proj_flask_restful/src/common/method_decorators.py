from functools import wraps

import flask_restful as restful


def basic_authentication():
    print('authenticating...')
    return True


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = basic_authentication()  # custom account lookup function

        if acct:
            print('authenticated')
            return func(*args, **kwargs)

        restful.abort(401)
    return wrapper
