from flask import Flask

from config import CONF
from src.common.exceptions import RestError
from src.resources.urls import add_routes


def create_app(conf_name):
    app = Flask(__name__)
    app.config.from_object(CONF[conf_name])

    add_routes()

    from src.resources.auth import bp_auth
    from src.resources.profile import bp_profile
    from src.resources.home import bp_home

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_profile)
    app.register_blueprint(bp_home)

    @app.errorhandler(RestError)
    def handle_demo_error(err: RestError):
        return {'error': err.message, 'code': err.code}, 400

    return app
