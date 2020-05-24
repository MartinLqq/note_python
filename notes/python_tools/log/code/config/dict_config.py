import logging
from pathlib import Path

from .dict_config_filters import myFilter1

print(Path.home() / 'logs')

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

LOG_CONF = {
    'version': 1,
    'formatters': {
        'formatter_1': {
            'format': '%(levelname)s:%(name)s %(asctime)s: %(message)s',
            'datefmt': None
        },
        'formatter_2': {
            'format': '%(levelname)s - %(name)s - %(message)s',
            'datefmt': None
        }
    },
    'filters': {
        'filter_1': {
            '()': myFilter1,      # 使用 `()` 指定用那个类来实现过滤功能
            'name': 'name1'       # name 的值会在 Filter 实例化时传入
        }
    },
    'handlers': {
        'handler_1': {    # 指定一个文件 handler, 仅保存 ERROR 及其以上级别的日志
            'class': 'logging.FileHandler',
            'level': logging.ERROR,
            'formatter': 'formatter_1',
            'filters': ['filter_1'],
            'filename': LOG_DIR / 'test_dict_config_err.log',  # 需要先创建目录
        },
        'handler_2': {    # 指定一个 stream handler, 打印 DEBUG 及其以上级别的日志
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'formatter_2',
            # 'filters': ['filter_1']
        }
    },
    'loggers': {
        'my_logger1': {
            'level': logging.WARNING,     # 在这里指定的 level, 优先级更高
            # Logger 对象被设计为一个树形结构.  print(logger.parent)
            # 子logger 在完成对日志消息的处理后，默认会将日志消息传递给它的 parent logger
            'propagate': False,         # 1/0/True/False, 是否传递给父节点的 logger 来处理
            'filters': ['filter_1'],    # 在这里指定的 filter, 优先级更高
            'handlers': ['handler_1', 'handler_2']
        }
    },
    'root': {  # 专门配置 root logger
        'level': logging.DEBUG,
        # 'propagate': 1,  # 对于 root logger 来说, propagate 项无效
        'filters': [],
        'handlers': ['handler_2']   # 为了测试 propagate, 需要指定一个 handler
    },
    'incremental': False,
    'disable_existing_loggers': True
}
