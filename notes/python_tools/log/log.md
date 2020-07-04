# log

# 资源

- [python 3.7 log 文档](https://docs.python.org/3.7/library/logging.html)
- [python3.7 Logging Cookbook](https://docs.python.org/3.7/howto/logging-cookbook.html#logging-cookbook)

# log保存位置的选择

- 早期在 /var 下,  后面推荐在 /srv 下.  但问题是都需要 root 权限做初始化配置
- /tmp 不需要做初始化配置,  但重启 log 会丢失
- $HOME 一般是有权限的,  但需要 配置文件 支持环境变量或相对路径

如路径直接写 `$HOME/log/xxx.log`,  其中 '$HOME' 是无法直接转换成当前用户的家目录的,  此时可以先使用代码获取 家目录:  

```python
usr_home = os.path.expanduser('~')
usr_home = os.path.expanduser('$HOME')
```





# log 配置方式

### 1. `logging.basicConfig()`

```python
logging.basicConfig(
    filename,
    filemode,
    format,
    datefmt,
    style,
    level,
    stream,
    handlers
)
```

例子详见 code 目录



### 2. 自定义 logger

将 logging.basicConfig 的配置项进行拆分, 自定义 logger

> 注:  logger 是模块层次的,  当定义多个相同 name 的 logger 时,  只有第一次定义的 logger 会真正起作用

```python
"""
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
```

例子详见 code 目录

### 3. `logging.config.xxx`

##### `dictConfig`

一个配置例子 (详见 code 目录)

```python
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
```

使配置生效

```python
logger = logging.getLogger('my_logger1')

# Logger 对象被设计为一个树形结构
print(logger.parent)

# 使配置生效
config.dictConfig(LOG_CONF)
```





##### `fileConfig`

##### `listen`









### RotatingHandler

##### 配置示例

```python
import logging

from logging import config
from pathlib import Path

__all__ = ['logger']


LOG_DIR = Path(__file__).parent / 'logs'
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
            'maxBytes': 512,            # 测试方便

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

```



##### 问题1 - windows文件占用

- [python logging模块“另一个程序正在使用此文件，进程无法访问。”问题解决办法](https://www.cnblogs.com/zepc007/p/10936623.html)
- `concurrent-log-handler` 模块:   https://github.com/Preston-Landers/concurrent-log-handler 



##### 问题2 - 多进程写日志

https://www.jianshu.com/p/1772306cb3db 

在单进程环境下，使用上面两个 RotatingHandler 不会有问题。但是当有多个进程向同一个日志文件写入日志的时候，这两个 RotatingHandler 就会带来问题。

举个例子，假如某个 Web 应用通过 uWSGI 提供服务，uWSGI 一般以多进程 master/worker 的方式启动。然后该 Web 应用需要记录运行日志，并且希望日志能够每天午夜时刻自动切分回滚。如果使用 TimedRotatingFileHandler，那么由于 uWSGI 的多个 worker 可能同时也可能相差很小一段时间对日志文件进行回滚操作，这会导致先前回滚的存档日志被后来的 worker 的回滚操作覆盖，导致日志丢失。详细解释可以看看最后面附上的参考资料。

**解决方案**

针对这个午夜自动切分回滚日志存在的问题，有什么解决办法呢？我们采取的方案的思路不一样，重点来说有两点：

- 日志文件以日期结尾，当天的日志写入以当天日期结尾的文件
- 每到午夜，原子性地创建新的日志文件，新的日志文件以新日期结尾

如何原子性地创建文件呢？以 os.O_CREAT | os.O_EXCL 模式打开文件就可以了。如果日志文件已经存在，打开文件就失败。

可能有人会问，多个进程同时往一个日志文件里面写日志，不会导致日志混乱吗？只要每行日志大小不超过一定值，就不会错乱（这个还没有深入研究）。



```python
from logging import FileHandler
import os
import errno
import datetime

class MidnightRotatingFileHandler(FileHandler):
    def __init__(self, filename):
        self._filename = filename
        self._rotate_at = self._next_rotate_datetime()
        super(MidnightRotatingFileHandler, self).__init__(filename, mode='a')

    @staticmethod
    def _next_rotate_datetime():
        # rotate at midnight
        now = datetime.datetime.now()
        return now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)

    def _open(self):
        now = datetime.datetime.now()
        log_today = "%s.%s" % (self._filename, now.strftime('%Y-%m-%d'))
        try:
            # create the log file atomically
            fd = os.open(log_today, os.O_CREAT | os.O_EXCL)
            # if coming here, the log file was created successfully
            os.close(fd)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # should not happen
                raise
        self.baseFilename = log_today
        return super(MidnightRotatingFileHandler, self)._open()

    def emit(self, record):
        now = datetime.datetime.now()
        if now > self._rotate_at:
            # time to rotate
            self._rotate_at = self._next_rotate_datetime()
            self.close()
        super(MidnightRotatingFileHandler, self).emit(record)
```





### TimedRotatingFileHandler











# 开源 log 工具库

### loguru

Github:  https://github.com/Delgan/loguru

文档:   https://loguru.readthedocs.io/ 

```
pip install loguru
```



```python
通过旋转/保留/压缩更方便地记录文件
使用大括号样式的现代字符串格式
在线程或main中捕获异常
漂亮的日志颜色
异步、线程安全、多进程安全
完全描述性异常
根据需要进行结构化日志记录
可自定义级别
更好的日期时间处理
适用于脚本和库
完全兼容标准日志记录
通过环境变量的个性化默认值
```





