"""
使用 logging.basicConfig() 配置日志
"""


import logging


# The default level of logging is warning.
# So we should change the level for logging debug/info message.
# logging.basicConfig(level=logging.DEBUG)


# If we want to save logs to files, we should config the param `filename`.
# Then the logs will be saved to file, instead of printing in console.
# logging.basicConfig(level=logging.DEBUG, filename='log_0.log')


# We can also change the format of logs
# Tip: be sure to know that the logging is singleton, please anatate the configs above.
# See more format on the document
_format = ('%(asctime)s '
           '%(name)s '  # the name of logger
           '%(levelname)s '
           '%(filename)s '
           '%(threadName)s '
           '%(lineno)d: '
           '%(message)s')
logging.basicConfig(
    level=logging.DEBUG,
    # filename='log_0.log',
    format=_format,
)


def add(a, b):
    return a + b

def minus(a, b):
    return a - b


logging.debug('The result of add(1,2): %s', add(1, 2))
logging.debug('The result of minus(1,2): %s', minus(1, 2))
