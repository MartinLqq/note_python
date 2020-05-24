import falcon
from wsgiref import simple_server

from app1.db import StorageEngine
from app1.exceptions import StorageError
from app1.middlewares import AuthMiddleware, RequireJSON, JSONTranslator
from app1.proxies import SinkAdapter
from app1.resources import ThingsResource


db = StorageEngine()

def create_app():
    # Configure your WSGI server to load "things.app" (app is a WSGI callable)
    _app = falcon.App(middleware=[
        AuthMiddleware(),
        RequireJSON(),
        JSONTranslator(),
    ])

    # If a responder ever raised an instance of StorageError, pass control to
    # the given handler.
    _app.add_error_handler(StorageError, StorageError.handle)

    return _app


app = create_app()

app.add_route('/{user_id}/things', ThingsResource(db))

# Proxy some things to another service; this example shows how you might
# send parts of an API off to a legacy system that hasn't been upgraded
# yet, or perhaps is a single cluster that all data centers have to share.
app.add_sink(SinkAdapter(), r'/search/(?P<engine>ddg|y)\Z')


# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
