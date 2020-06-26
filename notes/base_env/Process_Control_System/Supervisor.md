# Supervisor

进程控制系统

# 资源

 http://supervisord.org/index.html 



# 介绍

Supervisor 是一个客户/服务端 系统, 允许用户控制类  UNIX  系统上的一些进程.

Supervisor 是用 Python 开发的一个 client/server 服务，是 Linux/Unix 系统下的一个进程管理工具，不支持 Windows 系统。它可以很方便的监听、启动、停止、重启一个或多个进程。用 Supervisor 管理的进程，当一个进程意外被杀死，supervisort 监听到进程死后，会自动将它重新拉起，很方便的做到进程自动恢复的功能，不再需要自己写 shell 脚本来控制。 



### Supervisor 的组成

#### - supervisord

supervisor 的服务端

- 处理客户端的命令行请求
- 重启崩溃或关闭的子进程
- 记录子进程标准输出和错误输出的日志
- 生成和处理子进程生命周期中的事件

服务端配置文件:

- `/etc/supervisord.conf`
- 是 “Windows-INI” 类型的配置文件



#### - supervisorctl

 supervisor  的命令行客户端

- 通过 supervisorctl, 用户可以同时连接不同的 supervisord 服务进程,  获取服务控制下的子进程的状态,  可以控制这些子进程的停止、启动，可以获取正在运行 的子进程列表等。
- CLI 通过  UNIX domain socket  或 TCP socket 与 supervisord 服务通信， supervisord 可以对客户端进行权限验证
- 客户端与服务端使用相同的配置文件， 但比服务端配置多了一个 ` [supervisorctl] ` 块。



#### - web server

 supervisor  的 web 客户端

- 需要配置 `/etc/supervisord.conf` 的 ` [inet_http_server] ` 块



#### - XML-RPC Interface

The same HTTP server which serves the web UI serves up an XML-RPC interface that can be used to interrogate and control supervisor and the programs it runs. See [*XML-RPC API Documentation*](http://supervisord.org/api.html#xml-rpc). 



# 安装

```bash
$ pip install supervisor
```



# 创建配置文件

启动 supervisord 前,  需要先手动创建一个配置文件,  supervisor 配置查找顺序:

1. `../etc/supervisord.conf` (Relative to the executable)
2. `../supervisord.conf` (Relative to the executable)
3. `$CWD/supervisord.conf`
4. `$CWD/etc/supervisord.conf`
5. `/etc/supervisord.conf`
6. `/etc/supervisor/supervisord.conf` (since Supervisor 3.3.0)



使用 -c 选项可以指定查找的路径

常用配置方式:

1. ` /etc/supervisord.conf `   需要 root 用户访问权限
2. `当前路径/supervisord.conf `   启动时 ` supervisord -c supervisord.conf `

执行  supervisord 命令时指定的配置项会覆盖配置文件中的对应配置



# 运行 Supervisor

### 添加一个程序

例如在 supervisord 进程启动时执行 cat 命令

```bash
[supervisord]  # 启动 supervisord 必须的 section

[supervisorctl] # 运行 supervisorctl 命令必须的 section

[program:foo]
command=/bin/cat
```



### 运行 supervisord

#### - supervisord 命令行选项

一些命令行选项

-  -c FILE, --configuration=FILE       指定 supervisrod 配置文件
- -n, --nodaemon        以前台方式运行
- -s, --silent         输出不重定向到标准输出
- -d PATH, --directory=PATH      当 supervisord 以守护进程方式运行时,  先切换到这个路径下
- -l FILE, --logfile=FILE     指定日志路径
- -y BYTES, --logfile_maxbytes=BYTES      日志文件分片的大小
- -z NUM, --logfile_backups=NUM               日志文件分片的最大数量
- -e LEVEL, --loglevel=LEVEL        日志级别
- -j FILE, --pidfile=FILE        将 supervisord 进程号输出到哪个文件
- -i STRING, --identifier=STRING      supervisor 实例的识别符  (运行多个 supervisor 时可区分)

查看更多选项:   supervisord --help



### 运行 supervisorctl

#### - supervisorctl 命令行选项

-  -c, --configuration     配置文件路径 ( 默认 /etc/supervisord.conf )
-  -i, --interactive          在执行命令之后,  打开一个交互式的 shell
-  -s, --serverurl URL   supervisord 服务正在监听哪个地址  ( 默认 [http://localhost:9001](http://localhost:9001/)  )
-  -u, --username 
-  -p, --password 
-  -r, --history-file          Keep a readline history (if readline is available)

#### - **supervisorctl** 交互式 shell 命令

一些 supervisorctl Actions:

-  help     查看所有支持的  actions
-  help <action>    查看指定 action 的说明
-  add <name> [...] 
-  remove <name> [...] 
-  update 
-  clear
- fg <process>
-  pid 
-  reload 
-  reread 
-  restart  
-  start  
-  status 
-  stop  
-  tail  
-  update <gname> [...] 



### 信号 Signals

Signal Handlers

```
SIGTERM
    supervisord and all its subprocesses will shut down. This may take several seconds.

SIGINT
    supervisord and all its subprocesses will shut down. This may take several seconds.

SIGQUIT
    supervisord and all its subprocesses will shut down. This may take several seconds.

SIGHUP
    supervisord will stop all processes, reload the configuration from the first config file it finds, and start all processes.

SIGUSR2
    supervisord will close and reopen the main activity log and all child log files.
```





# 配置详解

### 配置文件格式

 `supervisord.conf` 需要是一个 Windows-INI-style (Python ConfigParser)  文件,  由  sections  和  sections  下的 key=value 键值对组成



### 环境变量引用方式

$(ENV_VAR)s





### `[unix_http_server]`

```ini
[unix_http_server]  # 配置示例, 详见官网
file = /tmp/supervisor.sock
chmod = 0777
chown= nobody:nogroup
username = user
password = 123
```



### `[inet_http_server]`

```ini
[inet_http_server]  # 配置示例, 详见官网
port = 127.0.0.1:9001
username = user
password = 123
```

### `[supervisord]`

```ini
[supervisord]  # 配置示例, 详见官网
logfile = /tmp/supervisord.log
logfile_maxbytes = 50MB
logfile_backups=10
loglevel = info
pidfile = /tmp/supervisord.pid
nodaemon = false
minfds = 1024
minprocs = 200
umask = 022
user = chrism
identifier = supervisor
directory = /tmp
nocleanup = true
childlogdir = /tmp
strip_ansi = false
environment = KEY1="value1",KEY2="value2"
```

### `[supervisorctl]`

```ini
[supervisorctl]  # 配置示例, 详见官网
serverurl = unix:///tmp/supervisor.sock
username = chris
password = 123
prompt = mysupervisor
```

### `[program:x]`

```ini
[program:cat]  # 配置示例, 详见官网
command=/bin/cat
process_name=%(program_name)s
numprocs=1
directory=/tmp
umask=022
priority=999
autostart=true
autorestart=unexpected
startsecs=10
startretries=3
exitcodes=0
stopsignal=TERM
stopwaitsecs=10
stopasgroup=false
killasgroup=false
user=chrism
redirect_stderr=false
stdout_logfile=/a/path
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=/a/path
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=false
environment=A="1",B="2"
serverurl=AUTO
```

### `[include]`

```ini
[include]  # 配置示例, 详见官网
files = /an/absolute/filename.conf /an/absolute/*.conf foo.conf config??.conf
```

### `[group:x]`

```ini
[group:foo]  # 配置示例, 详见官网
programs=bar,baz
priority=999
```

### `[fcgi-program:x]`

```ini
[fcgi-program:fcgiprogramname]  # 配置示例, 详见官网
command=/usr/bin/example.fcgi
socket=unix:///var/run/supervisor/%(program_name)s.sock
socket_owner=chrism
socket_mode=0700
process_name=%(program_name)s_%(process_num)02d
numprocs=5
directory=/tmp
umask=022
priority=999
autostart=true
autorestart=unexpected
startsecs=1
startretries=3
exitcodes=0
stopsignal=QUIT
stopasgroup=false
killasgroup=false
stopwaitsecs=10
user=chrism
redirect_stderr=true
stdout_logfile=/a/path
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_events_enabled=false
stderr_logfile=/a/path
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_events_enabled=false
environment=A="1",B="2"
serverurl=AUTO
```

### `[eventlistener:x]`

```ini
[eventlistener:theeventlistenername]  # 配置示例, 详见官网
command=/bin/eventlistener
process_name=%(program_name)s_%(process_num)02d
numprocs=5
events=PROCESS_STATE
buffer_size=10
directory=/tmp
umask=022
priority=-1
autostart=true
autorestart=unexpected
startsecs=1
startretries=3
exitcodes=0
stopsignal=QUIT
stopwaitsecs=10
stopasgroup=false
killasgroup=false
user=chrism
redirect_stderr=false
stdout_logfile=/a/path
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_events_enabled=false
stderr_logfile=/a/path
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_events_enabled=false
environment=A="1",B="2"
serverurl=AUTO
```

### `[rpcinterface:x]`

```ini
[rpcinterface:another]  # 配置示例, 详见官网
supervisor.rpcinterface_factory = my.package:make_another_rpcinterface
retries = 1
```







# Subprocesses

### Process States

<img src="images\subprocess-transitions.png" alt="subprocess-transitions" style="zoom:67%;" />



# 更多

- Logging
- Events
- [Third Party Applications and Libraries](http://supervisord.org/plugins.html)







# 同类

- daemontools

  A [process control system by D.J. Bernstein](http://cr.yp.to/daemontools.html).

- launchd

  A [process control system used by Apple](http://en.wikipedia.org/wiki/Launchd) as process 1 under Mac OS X.

- runit

  A [process control system](http://smarden.org/runit/).

- Superlance

  A package which provides various event listener implementations that plug into Supervisor which can help monitor process memory usage and crash status: https://pypi.org/pypi/superlance/.