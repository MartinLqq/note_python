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