# Gunicorn

[Gunicorn](http://gunicorn.org/) (绿色独角兽)是一个高效的 Python WSGI Server,  通常用它来运行 wsgi application (由我们自己编写遵循 WSGI  application 的编写规范) 或者 wsgi framework (如 Django, Paster),  地位相当于 Java 中的 Tomcat。 

# 资源

- 文档:   https://docs.gunicorn.org/ 

# 安装

可以通过 pip 命令安装

```
pip3 install gunicorn
```

### 安装异步 workers

有两种可选的 Async Worker:

1. Eventlet
2. Gevent

```bash
$ pip install greenlet            # Required for both Eventlet and Gevent

$ pip install eventlet            # For eventlet workers
$ pip install gunicorn[eventlet]  # Or, using extra

$ pip install gevent              # For gevent workers
$ pip install gunicorn[gevent]    # Or, using extra
```



### 额外的依赖包

一些 Gunicorn 选项需要安装额外的包, 可以使用 `[extra]` 在安装 Gunicorn 的同时安装这些选项依赖.

```
gunicorn[eventlet]		基于 Eventlet 的 greenlets workers
gunicorn[gevent]		基于 Gevent 的 greenlets workers
gunicorn[gthread]		基于线程的 workers
gunicorn[tornado]		基于 Tornado 的 workers, 不推荐.
```

如果运行不止一个  Gunicorn  实例,   设置 [proc_name](https://docs.gunicorn.org/en/stable/settings.html#proc-name) 可以帮助我们在 `ps` 和 `top` 命令信息中进行区分.

```
gunicorn[setproctitle]	Enables setting the process name

多个可选项结合:
pip install gunicorn[gevent,setproctitle]
```





# 运行 Gunicorn

1. 可以通过命令运行 Gunicorn
2. 可以集成在 web 框架中, 如 Django, Pyramid, TurboGears 

### 基础用法

```bash
$ gunicorn [OPTIONS] APP_MODULE

# APP_MODULE 参数的格式:  $(MODULE_NAME):$(VARIABLE_NAME)
# 	MODULE_NAME: 一个用点 `.` 表示分隔符的路径
# 	VARIABLE_NAME: 可以指向一个 WSGI 可调用对象, 该对象必须在 MODULE_NAME 指定的路径文件中已定义.
#                  也可以指向一个函数调用.  gunicorn --workers=2 'main:create_app()'
#                  也可以不指定, 默认会找名为 `application` 的可调用对象 (如函数)
```

一个 WSGI 可调用对象的例子

```python
# main.py
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])

"""
启动命令:
	gunicorn --workers=2 main:app
或绑定地址:
	gunicorn --workers=2 -b '0.0.0.0:8000' main:app
"""
```



### 通用配置

一些命令行参数

> 查看更多参数:   `gunicorn -h`

- `-c CONFIG, --config=CONFIG` - Specify a config file in the form `$(PATH)`, `file:$(PATH)`, or `python:$(MODULE_NAME)`.
- `-b BIND, --bind=BIND` - Specify a server socket to bind. Server sockets can be any of `$(HOST)`, `$(HOST):$(PORT)`, `fd://$(FD)`, or `unix:$(PATH)`. An IP is a valid `$(HOST)`.
- `-w WORKERS, --workers=WORKERS` - The number of worker processes. This number should generally be between 2-4 workers per core in the server. Check the [FAQ](https://docs.gunicorn.org/en/stable/faq.html#faq) for ideas on tuning this parameter.
- `-k WORKERCLASS, --worker-class=WORKERCLASS` - The type of worker process to run. You’ll definitely want to read the production page for the implications of this parameter. You can set this to `$(NAME)` where `$(NAME)` is one of `sync`, `eventlet`, `gevent`, `tornado`, `gthread`. `sync` is the default. See the [worker_class](https://docs.gunicorn.org/en/stable/settings.html#worker-class) documentation for more information.
- `-n APP_NAME, --name=APP_NAME` - If [setproctitle](https://pypi.python.org/pypi/setproctitle) is installed you can adjust the name of Gunicorn process as they appear in the process system table (which affects tools like `ps` and `top`).



### Django

Django 集成 Gunicorn 时,  可以不指定 `VARIABLE_NAME`,  会根据 `MODULE_NAME` 指定的模块文件中找 `application`

```bash
$ gunicorn --env DJANGO_SETTINGS_MODULE=myproject.settings myproject.wsgi

# 在 Django 的 manage.py 路径下执行以上命令
```

> 可以看一下  Django  `myproject/wsgi.py`  的内容:
>
> ```python
> import os
> from django.core.wsgi import get_wsgi_application
> os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")  # blog应用
> application = get_wsgi_application()
> 
> # PS: 从上面可以看出, gunicorn 命令行不需要指定环境变量 DJANGO_SETTINGS_MODULE
> ```



**测试使用 Gunicorn 运行 Django 项目**

1. 全局安装 django

   ```bash
   $ pip3 install django==2.1.8
   ```

2. 创建一个 django 项目

   ```bash
   $ djnago-admin startproject myproj
   $ cd myproj
   $ django-admin startapp myapp1
   ```

3. 使用 Gunicorn 运行

   ```bash
   $ gunicorn -w=2 -b '0.0.0.0:8000' myproj.wsgi
   ```

   

### Paste Deployment

 Pyramid 和 Turbogears 框架专门使用 Paste Deployment 配置文件的方式配置 gunigorn

详见:   https://docs.gunicorn.org/en/stable/run.html#paste-deployment 



# 配置概览

### 配置加载方式

Gunicorn 按顺序从三个地方读取配置:

1. 框架指定的配置

2. 命令行 `-c, --config` 参数指定的配置文件,  或通过环境变量 `GUNICORN_CMD_ARGS` 指定

   ```bash
   $ GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=3" gunicorn myproj.wsgi:application
   ```

3. 命令参数:  通过命令参数单独指定配置

> 1. Framework Settings
> 2. Configuration File
> 3. Command Line
>
> 后面如果读取到相同配置,  会覆盖前面的配置， 即命令行配置的优先级最高



检查配置，  检查  application 是否可以加载

```bash
$ gunicorn --check-config APP_MODULE
```



### Configuration File

- 配置文件必须是一个合法的 python 源文件，  如  `gunicorn.conf.py `
- 配置文件不需要加到 python 的模块搜索路径中 ( sys.path, PYTHONPATH ) 

示例:

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

"""
运行示例:
	gunicorn -c gunicorn.conf.py myproj.wsgi
"""
```

### 官方配置示例及说明

 [gunicorn](https://github.com/benoitc/gunicorn)/[examples](https://github.com/benoitc/gunicorn/tree/master/examples)/example_config.py

```python
# Sample Gunicorn configuration file.

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

bind = '127.0.0.1:8000'
backlog = 2048

#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#

workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

#
#   spew - Install a trace function that spews every line of Python
#       that is executed when running the server. This is the
#       nuclear option.
#
#       True or False
#

spew = False

#
# Server mechanics
#
#   daemon - Detach the main Gunicorn process from the controlling
#       terminal with a standard fork/fork sequence.
#
#       True or False
#
#   raw_env - Pass environment variables to the execution environment.
#
#   pidfile - The path to a pid file to write
#
#       A path string or None to not write a pid file.
#
#   user - Switch worker processes to run as this user.
#
#       A valid user id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getpwnam(value) or None
#       to not change the worker process user.
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
#
#   umask - A mask for file permissions written by Gunicorn. Note that
#       this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string
#       compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid
#       for decimal, hex, and octal representations)
#
#   tmp_upload_dir - A directory to store temporary request data when
#       requests are read. This will most likely be disappearing soon.
#
#       A path to a directory where the process owner can write. Or
#       None to signal that Python should choose one on its own.
#

daemon = False
raw_env = [
    'DJANGO_SECRET_KEY=something',
    'SPAM=eggs',
]
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

#
#   Logging
#
#   logfile - The path to a log file to write to.
#
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output
#
#       A string of "debug", "info", "warning", "error", "critical"
#

errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

#
# Process naming
#
#   proc_name - A base to use with setproctitle to change the way
#       that Gunicorn processes are reported in the system process
#       table. This affects things like 'ps' and 'top'. If you're
#       going to be running more than one instance of Gunicorn you'll
#       probably want to set a name to tell them apart. This requires
#       that you install the setproctitle module.
#
#       A string or None to choose a default of something like 'gunicorn'.
#

proc_name = None

#
# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance
#       as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary
#       master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
```

详尽配置都在这里:   [settings](https://docs.gunicorn.org/en/stable/settings.html#settings)



### Framework Settings

目前只有 Paster Applications 支持框架配置,  还不支持 WSGI applications 和在 settings.py 中配置 gunicron

Paster Applications 配置示例

```ini
# gunicorn.conf.ini
[server:main]
use = egg:gunicorn#main
host = 192.168.0.1
port = 80
workers = 2
proc_name = brim
```

> 注意 Framework Settings 会被 Configuration File 和  Command line 覆盖.



# Settings

### Config File

```
-c CONFIG, --config CONFIG

指定 Gunicorn 配置文件, CONFIG 的形式可以是:
	a. PATH
	b. file:PATH
	c. python:MODULE_NAME  (Gunicorn 19.4 开始支持)
```



### Debugging

reload

```
--reload		(False)

是否在代码修改时自动重启 workers
应该仅在开发模式下开启
注意在使用 paste configuration 时此项配置无效, 因为 paste 不导入任何应用代码
```

reload_engine

```
--reload-engine STRING		(auto)

重载的引擎, 可选:
    a. auto
    b. poll
    c. inotify (requires inotify)
```

reload_extra_files

```
--reload-extra-file FILES		( [] )

添加额外需要监听改动并重载的文件
```

spew

```
--spew		(False)

是否打印服务执行的每一行代码
不要轻易开启, 因为 spew(喷出，涌出), 看屏幕会闪花眼.
```

check_config

```
--check-config		(False)

检查配置文件
```





### Logging

accesslog

```
--access-logfile FILE		(None)

指定 访问日志 的输出位置,
如果指定为 '-', 表示输出到 stdout
默认是 None: 既不输出到文件, 也不输出到 stdout
```

disable_redirect_access_to_syslog

```
--disable-redirect-access-to-syslog		(False)

取消重定向访问日志到 syslog. (Gunicorn 19.8 新增)
```

access_log_format

```
--access-logformat STRING

访问日志的记录格式
默认:  %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
```

| Identifier  | Description                           |
| ----------- | ------------------------------------- |
| h           | remote address                        |
| l           | `'-'`                                 |
| u           | user name                             |
| t           | date of the request                   |
| r           | status line (e.g. `GET / HTTP/1.1`)   |
| m           | request method                        |
| U           | URL path without query string         |
| q           | query string                          |
| H           | protocol                              |
| s           | status                                |
| B           | response length                       |
| b           | response length or `'-'` (CLF format) |
| f           | referer                               |
| a           | user agent                            |
| T           | request time in seconds               |
| D           | request time in microseconds          |
| L           | request time in decimal seconds       |
| p           | process ID                            |
| {header}i   | request header                        |
| {header}o   | response header                       |
| {variable}e | environment variable                  |



errorlog

```
--error-logfile FILE,  --log-file FILE

错误日志的记录文件
默认: '-'   即错误日志输出到 stderr
```

loglevel

```
--log-level LEVEL		(info)

指定错误日志输出的粒度
合法的日志水平字符串:
    debug
    info
    warning
    error
    critical
```

capture_output

```
--capture-output	(False)

Redirect stdout/stderr to specified file in errorlog.
```

logger_class

```
--logger-class STRING		( gunicorn.glogging.Logger )

可以写一个自定义日志器类, 继承自 gunicorn.glogging.Logger
```

logconfig

```
--log-config FILE		(None)

The log config file to use. 
Gunicorn uses the standard Python logging module’s Configuration file format.
```

logconfig_dict

```
--log-config-dict		( {} )
```

syslog_addr

```
--log-syslog-to SYSLOG_ADDR		( udp://localhost:514 )

指定 syslog 消息发送的目标地址
    unix://PATH#TYPE
    udp://HOST:PORT
    tcp://HOST:PORT
```

syslog

```
--log-syslog			(False)

参考 disable_redirect_access_to_syslog 选项
```

其他...





### Process Naming

proc_name

```
-n STRING, --name STRING		(None)
```

default_proc_name

```
gunicorn
```



### SSL

```
--keyfile FILE		(None)
--certfile FILE		(None)
--ca-certs FILE		(None)

--do-handshake-on-connect		(False)

更多...
```



### Security

limit_request_line

```
--limit-request-line INT		(4094)

The maximum size of HTTP request line in bytes.
可用于阻止 DDOS 攻击 (分布式拒绝服务攻击)
```

limit_request_fields

```
--limit-request-fields INT		(100)

限制在一次 HTTP 请求中, 请求头字段的总个数
```

limit_request_field_size

````
--limit-request-field_size INT		(8190)

限制在一次 HTTP 请求中, 请求头字段的大小
````





### Server Hooks

on_starting

```python
# Called just before the master process is initialized

def on_starting(server):
    pass
```

on_reload

```python
# Called to recycle workers during a reload via SIGHUP.

def on_reload(server):
    pass
```

when_ready

```python
# Called just after the server is started.

def when_ready(server):
    pass
```

pre_fork

```python
# Called just before a worker is forked

def pre_fork(server, worker):
    pass
```

post_fork

```python
# Called just after a worker has been forked

def post_fork(server, worker):
    pass
```

post_worker_init

```python
# Called just after a worker has initialized the application

def post_worker_init(worker):
    pass
```

更多

```
worker_int
worker_abort
pre_exec:  Called just before a new master process is forked
pre_request:  Called just before a worker processes the request
post_request:  Called after a worker processes the request
child_exit:  Called just after a worker has been exited, in the master process
worker_exit:  Called just after a worker has been exited, in the worker process
nworkers_changed:  Called just after num_workers has been changed
on_exit:  Called just before exiting Gunicorn
```





### Server Mechanics





### Server Socket

bind

```
-b ADDRESS, --bind ADDRESS
['127.0.0.1:8000']

ADDRESS 的格式: HOST, HOST:PORT, unix:PATH, fd://FD. 
一个 IP 是一个有效的 HOST.
可以绑定多个 ADDRESS:
	gunicorn -b 127.0.0.1:8000 -b [::1]:8000 test:app
	# will bind the test:app application on localhost both on ipv6 and ipv4 interfaces
```





### Worker Processes

workers

```
-w INT, --workers INT		(1)

The number of worker processes for handling requests
默认取 WEB_CONCURRENCY 环境变量的值, 如果没有定义此变量 取 1.
```

worker_class

```
-k STRING, --worker-class STRING		(sync)

workers 的类型
```

> The default class (`sync`) should handle most “normal” types of workloads. You’ll want to read [Design](https://docs.gunicorn.org/en/stable/design.html) for information on when you might want to choose one of the other worker classes. Required libraries may be installed using setuptools’ `extras_require` feature.
>
> A string referring to one of the following bundled classes:
>
> - `sync`
> - `eventlet` - Requires eventlet >= 0.24.1 (or install it via `pip install gunicorn[eventlet]`)
> - `gevent` - Requires gevent >= 1.4 (or install it via `pip install gunicorn[gevent]`)
> - `tornado` - Requires tornado >= 0.2 (or install it via `pip install gunicorn[tornado]`)
> - `gthread` - Python 2 requires the futures package to be installed (or install it via `pip install gunicorn[gthread]`)
>
> Optionally, you can provide your own worker by giving Gunicorn a Python path to a subclass of `gunicorn.workers.base.Worker`. This alternative syntax will load the gevent class: `gunicorn.workers.ggevent.GeventWorker`.

threads

```
--threads INT		(1)

Run each worker with the specified number of threads
注: 
	仅在使用 Gthread worker_class 时有效.
	如果在 sync worker_class 下指定 --threads 超过 1, 就会切换为 gthread worker
```

worker_connections

```
--worker-connections INT		(1000)

The maximum number of simultaneous clients.
This setting only affects the Eventlet and Gevent worker types.
```

max_requests

```
--max-requests INT		(0)

The maximum number of requests a worker will process before restarting
```

timeout

```
-t INT, --timeout INT		(30)

Workers silent for more than this many seconds are killed and restarted
```

graceful_timeout

```
--graceful-timeout INT		(30)

Timeout for graceful workers restart
workers 会在关闭前的 30 秒内继续处理一些未完成的请求
```

keepalive

```
--keep-alive INT		(2)

The number of seconds to wait for requests on a Keep-Alive connection
sync worker does not support persistent connections and will ignore this option
```





# 部署 Gunicorn

官方强烈建议在一个 代理服务器 下使用 Gunicorn,  且强烈建议使用 Nginx 代理



### Nginx 配置

一个 nginx.conf 示例

```nginx
worker_processes 1;

user nobody nogroup;
# 'user nobody nobody;' for systems with 'nobody' as a group instead
error_log  /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
  worker_connections 1024; # increase if you have lots of clients
  accept_mutex off; # set to 'on' if nginx worker_processes > 1
  # 'use epoll;' to enable for Linux 2.6+
  # 'use kqueue;' to enable for FreeBSD, OSX
}

http {
  include mime.types;
  # fallback in case we can't determine a type
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log combined;
  sendfile on;

  upstream app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response

    # for UNIX domain socket setups
    server unix:/tmp/gunicorn.sock fail_timeout=0;

    # for a TCP configuration
    # server 192.168.0.7:8000 fail_timeout=0;
  }

  server {
    # if no Host match, close the connection to prevent host spoofing
    listen 80 default_server;
    return 444;
  }

  server {
    # use 'listen 80 deferred;' for Linux
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen 80;
    client_max_body_size 4G;

    # set the correct host(s) for your site
    server_name example.com www.example.com;

    keepalive_timeout 5;

    # path for static files
    root /path/to/app/current/public;

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://app_server;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /path/to/app/current/public;
    }
  }
}
```





### 使用 Virtualenv

```bash
$ mkdir ~/venvs/
$ virtualenv ~/venvs/webapp
$ source ~/venvs/webapp/bin/activate
$ pip install gunicorn
$ deactivate
```

Then you just need to use one of the three Gunicorn scripts that was installed into `~/venvs/webapp/bin`.

Note: You can force the installation of Gunicorn in your Virtualenv by passing `-I` or `--ignore-installed` option to pip:

```bash
$ source ~/venvs/webapp/bin/activate
$ pip install -I gunicorn
```



### Monitoring

##### Gaffer

##### Runit

##### Supervisor

- http://supervisord.org/index.html 
- [supervisor.md](..\Process_Control_System\Supervisor.md)

gunicorn 官方配置 supervisor 的示例:   [gunicorn](https://github.com/benoitc/gunicorn)/[examples](https://github.com/benoitc/gunicorn/tree/master/examples)/supervisor.conf

```ini
[program:gunicorn]
command=/usr/local/bin/gunicorn main:application -c /path/to/project/gunicorn.conf.py
directory=/path/to/project
user=nobody
autorestart=true
redirect_stderr=true
```





##### Systemd



### Logging

官方的一个 log 示例:    [gunicorn](https://github.com/benoitc/gunicorn)/[examples](https://github.com/benoitc/gunicorn/tree/master/examples)/logging.conf

```ini
[loggers]
keys=root, gunicorn.error, gunicorn.access
# 我们可以在自己的 logging 配置中添加两个logger: 'gunicorn.error', 'gunicorn.access',
# 来配置 gunicorn 日志

[handlers]
keys=console, error_file, access_file

[formatters]
keys=generic, access

[logger_root]
level=INFO
handlers=console

[logger_gunicorn.error]
level=INFO
handlers=error_file
propagate=1
qualname=gunicorn.error

[logger_gunicorn.access]
level=INFO
handlers=access_file
propagate=0
qualname=gunicorn.access

[handler_console]
class=StreamHandler
formatter=generic
args=(sys.stdout, )

[handler_error_file]
class=logging.FileHandler
formatter=generic
args=('/tmp/gunicorn.error.log',)

[handler_access_file]
class=logging.FileHandler
formatter=access
args=('/tmp/gunicorn.access.log',)

[formatter_generic]
format=%(asctime)s [%(process)d] [%(levelname)s] %(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter

[formatter_access]
format=%(message)s
class=logging.Formatter
```





# 信号处理

 https://docs.gunicorn.org/en/latest/signals.html 





# 定制化 Application

*New in version 19.0.*

有时候如果你想集成 Gunicorn 到 WSGI 应用,  可以编写一个类,  继承自  gunicorn.app.base.BaseApplication

 https://docs.gunicorn.org/en/latest/custom.html 

# Gunicorn 的设计架构

### Server Model

一个主进程 master 管理可以多个子进程 worker 集合,  master 不了解任何一个独立的 client,  所有的请求和响应都是 worker 的进程来处理

1. Master
   - master 进程是一个简单地循环,  监听不同进程的信号,  做出相应处理.  
   - master 通过监听 TTIN, TTOU 和 CHLD 等信号 来管理正在运行的 workers,
   - master 监听信号 TTIN, TTOU 来增加或减少正在运行的 workers;   CHLD 信号表明一个子进程的终止,  master 以此来自动重启启动失败的 worker.
2. Sync Workers
   - 最基础的默认 worker 类型,  同时只能处理一个客户端请求
   - sync worker 不支持持续的连接 —— 在每一次响应发送出去之后连接就会断开，即使你在应用的请求头中添加了  `Keep-Alive` 或 ` Connection: keep-alive `.
3. Async Workers
   - 异步 worker  基于 [Greenlets](https://github.com/python-greenlet/greenlet) (via [Eventlet](http://eventlet.net/) and [Gevent](http://www.gevent.org/)) ,   Greenlets 是 python 的多线程实现
   - 如果要完全支持  greenlet ,  需要做一些适配,  例如想用  [Gevent](http://www.gevent.org/) and [Psycopg](http://initd.org/psycopg/) ,  就必须安装并配置好   [psycogreen](https://bitbucket.org/dvarrazzo/psycogreen) 
4. Tornado Workers
5. AsyncIO Workers

### 如何选择 worker ?

在以下场景中需要使用异步 workers:

- 应用在处理一次请求时花费时间较长 (阻塞)
- 直接向 internet 服务请求
-  流式请求和响应 
-  长轮询 
- Web sockets
- Comet  ( *Comet*是一种用于web的推送技术,能使服务器实时地将更新的信息传送到客户端,而无须客户端发出请求,目前有两种实现方式, 长轮询和 iframe 流。 )



### 启动多少 worker ?

Gunicorn 只需要 4-12 worker 进程来处理每秒数千次的请求,  官方推荐的 worker 数是 ` (2 x $num_cores) + 1 `

影响 worker 个数的因素有:

1. 硬件 (操作系统)
2. 软件 (应用程序)

### 使用多少线程 ?

 Depending on the system, using multiple threads, multiple worker processes, or some mixture, may yield the best results 





# FAQ

官网列出了一些常见问题及解答:   https://docs.gunicorn.org/en/latest/faq.html 

1. 怎么设置 SCRIPT_NAME ?
2. 如何重启通过 Gunicorn 运行的 应用程序 ?
3. 如何测试一个 proxy configuration ?
4. 如何命名 Gunicorn 进程 ?
5. 为什么 HTTP Keep-Alive 不生效 ?
6. 选择哪种 worker ?
7. 支持哪些 worker ?
8. 启动多少个 worker 最好 ?
9. 如何动态改变运行中的 worker 的个数 ?
10. Gunicorn 会遇到  惊群效应  吗 ?
11. 为什么控制台没有打印任何日志 ?
12. 怎么增加文件描述符的最大个数 ?
13. 怎么增加 socket backlog 个数 ?
14. 怎么关闭 `sendfile()` ?
15. 怎么解决 Django 报的 `ImproperlyConfigured` 错误 ?
16. ...