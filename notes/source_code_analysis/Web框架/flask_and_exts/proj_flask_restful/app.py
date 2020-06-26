from flask import Flask

from config import CONF
from src.common.exceptions import RestError
from src.resources.urls import add_routes


def create_app(conf_name):
    app = Flask(__name__)
    app.config.from_object(CONF[conf_name])

    add_routes()

    from src.resources.session import bp_session
    from src.resources.user import bp_user

    app.register_blueprint(bp_session)
    app.register_blueprint(bp_user)

    @app.errorhandler(RestError)
    def handle_demo_error(err: RestError):
        return {
                   'error': err.message,
                   'code': err.code
               }, 400

    return app
