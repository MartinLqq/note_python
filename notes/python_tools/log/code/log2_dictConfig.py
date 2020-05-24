import logging
from logging import config

from config.dict_config import LOG_CONF

logger = logging.getLogger('my_logger1')

# Logger 对象被设计为一个树形结构
print(logger.parent)

# 使配置生效
config.dictConfig(LOG_CONF)


def foo():
    logger.debug('dictConfig DEBUG')
    logger.info('dictConfig INFO')
    logger.warning('dictConfig WARNING')
    logger.error('dictConfig ERROR')
    logger.critical('dictConfig CRITICAL')

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception('dictConfig logger.exception')

    logger.error('xxxx test filter xxx')

foo()
