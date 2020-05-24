# 在 config.py 模块下
import logging


class Config:
    """Base config."""
    # 公共配置
    pass

class DevelopConfig(Config):
    """Dev env config."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class TestConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductConfig(Config):
    """Prod env config."""
    LOG_LEVEL = logging.ERROR


config = {
    "development": DevelopConfig,
    "test": TestConfig,
    "production": ProductConfig,
}


# __init__.py 下
# def create_app(conf_name):
#     app = Flask(__name__)
#     app.config.from_object(config[conf_name])
#     return app
