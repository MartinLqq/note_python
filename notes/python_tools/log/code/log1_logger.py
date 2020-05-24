"""
将 logging.basicConfig 的配置项进行拆分, 自定义 logger

自定义 一个logger 的步骤:
    1.获取一个 logger:               logging.getLogger(...)
    2.设置 level:                   logger.setLevel(...)
    3.定义一个/多个 formatter:       logging.Formatter(...)
    4.定义一个/多个 handler:         logging.XXXHandler(...)
    5.为 handler 设置一个 fomatter:  hd.setFormatter(...)
    6.为 handler 设置 level:        hd.setLevel(...)
    7.添加所有 handler 到 logger:    logger.addHandler(...), ...

    8.定义一个/多个 filter:          class MyFilter(logging.Filter): ...
    9.添加所有 filter 到 logger:     logger.addFilter(...), ...
"""

import logging


# 获取一个 logger
logger = logging.getLogger(__name__)


# 为 logger 设置 level
logger.setLevel(logging.DEBUG)


# 定义一个 formatter
formatter = logging.Formatter(
    '%(levelname)s:%(name)s %(asctime)s %(funcName)s: %(message)s'
)


# 定义一个 handler, 存储 INFO 及 INFO 以上级别的日志
# 为了方便测试, 将 mode 设为 w, 不追加
info_hd = logging.FileHandler('log1_info.log', mode='w')
info_hd.setFormatter(formatter)  # 为 handler 设置 formatter
info_hd.setLevel(logging.INFO)   # 为 handler 设置 level

# 定义另一个 handler, 存储 ERROR 及ERROR以上级别的日志
err_hd = logging.FileHandler('log1_error.log', mode='w')
err_hd.setFormatter(formatter)
err_hd.setLevel(logging.ERROR)

# 定义一个 handler, 用于 在控制台中打印 所有级别的日志
stream_hd = logging.StreamHandler()
stream_hd.setFormatter(formatter)
stream_hd.setLevel(logging.DEBUG)


# 添加所有 handler 到 logger
logger.addHandler(info_hd)
logger.addHandler(err_hd)
logger.addHandler(stream_hd)


# 实际定义 logger 时, 一般定义不同的 formatter, 用于存储/打印不同细节的日志


def foo():
    # 使用自定义 logger 打印日志
    logger.debug('test user defined logger DEBUG')
    logger.info('test user defined logger INFO')
    logger.warning('test user defined logger INFO')
    logger.error('test user defined logger ERROR')
    logger.critical('test user defined logger ERROR')


foo()


# 测试 logger.exception(), 记录异常的堆栈
def log_exc():
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception('tried to divide by 0')


log_exc()

# 测试 log_0.py 中默认的 root logger
# from log_0 import logging as default
# default.debug('default logger')
