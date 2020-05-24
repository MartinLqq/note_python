import os

from flask import Flask
from flask_migrate import init, migrate, upgrade, history
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from src.fm.user import BP_USER
    app.register_blueprint(BP_USER)

    # tests about flask-migrate
    @app.before_first_request
    def migrate_db():
        if not os.path.exists('migrations'):
            init()
            migrate()
            upgrade()
            history()

    return app
