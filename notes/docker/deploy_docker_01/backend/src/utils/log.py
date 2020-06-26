import logging

from logging import config
from pathlib import Path

__all__ = ['logger']


LOG_DIR = Path().cwd() / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_DEBUG_FILE = LOG_DIR / 'debug.log'
LOG_ERROR_FILE = LOG_DIR / 'error.log'

standard_fmt = '[%(asctime)s] [%(threadName)s:%(thread)d] [%(filename)s:%(lineno)d]' \
                  ' [%(levelname)s]: %(message)s'
simple_fmt = '[%(asctime)s] %(levelname)s  %(module)s:%(lineno)d: %(message)s'

LOG_CONF = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': standard_fmt, 'datefmt': None
        },
        'simple': {
            'format': simple_fmt, 'datefmt': None
        }
    },
    'filters': {},
    'handlers': {
        'stream': {
            'level': logging.DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_info': {
            'level': logging.DEBUG,

            # 'class': 'logging.handlers.RotatingFileHandler',
            # 使用 RotatingFileHandler 会发生文件占用错误, 换成以下Handler
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            # 'maxBytes': 1024*1024*5,  # 日志大小 5M
            'maxBytes': 1024,            # 测试方便

            # 'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'when': 'D',

            'backupCount': 5,         # 日志文件最大备份个数
            'encoding': 'utf-8',      # 日志文件编码, 避免中文log乱码

            'filename': str(LOG_DEBUG_FILE),
            'formatter': 'standard',
        },
        'file_error': {
            'level': logging.ERROR,
            # 'class': 'logging.handlers.RotatingFileHandler',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'formatter': 'standard',
            'filename': str(LOG_ERROR_FILE),
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,  # 日志文件最大备份个数
            'encoding': 'utf-8',  # 日志文件编码, 避免中文log乱码
        }
    },
    'loggers': {
        'my_logger': {
            'level': logging.DEBUG,
            'propagate': False,
            'handlers': ['stream', 'file_info', 'file_error']
        }
    },
    'incremental': False,
    'disable_existing_loggers': True
}

logger = logging.getLogger('my_logger')
config.dictConfig(LOG_CONF)
