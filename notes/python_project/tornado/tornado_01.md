  

# Tornado

# ====介绍====

Tornado 全称 Tornado Web Server，是一个用 Python 语言写成的 Web 服务器兼 Web 应用框架。

优势

- 轻量级 web 框架，类似于另一个Python web 框架 Web.py，其拥有异步非阻塞 IO 的处理方式。
- 异步非阻塞 IO 处理方式
- 出色的抗负载能力。官方用 nginx 反向代理的方式部署 Tornado 和其它 Python web 应用框架进行对比，结果最大浏览量超过第二名近40%。
- 优异的处理性能，不依赖多进程/多线程，一定程度上解决 C10K 问题
- WSGI 全栈替代产品，推荐同时使用其 web 框架和 HTTP 服务器







### 安装

自动安装

```bash
$ pip install tornado
```

手动安装

```bash
$ tar xvzf tornado-xxx.tar.gz
$ cd tornado-xxx
$ python setup.py build
$ sudo python setup.py install
```

### 运行环境

Tornado 应该运行在**类 Unix 平台**，在线上部署时为了最佳的性能和扩展性，仅推荐 **Linux** 和 **BSD**（因为充分利用 Linux 的 epoll 工具和 BSD 的 kqueue 工具，是 Tornado 不依靠多进程/多线程而达到高性能的原因）。

对于 Mac OS X，虽然也是衍生自 BSD 并且支持 kqueue，但是其网络性能通常不太给力，因此仅推荐用于开发。

对于 Windows，Tornado官方没有提供配置支持，但是也可以运行起来，不过仅推荐在开发中使用。





# ====基础====

### hello tornado

```python
# coding:utf-8
# server.py

import tornado.web
import tornado.ioloop
# import tornado.httpserver


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应 http 的 get 请求方式"""
        self.write("Hello Itcast!")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    app.listen(8000)
    # app.listen() 的 本质:
    # http_server = tornado.httpserver.HTTPServer(app) 
    # http_server.listen(8000)
    
    tornado.ioloop.IOLoop.current().start()
```

启动 tornado：

```bash
$ python server.py
```



### 基本模块

##### tornado.web

##### tornado.ioloop

##### tornado.httpserver

##### tornado.options



1. **tornado.web.RequestHandler**
   - 封装了对应一个请求的所有信息和方法，write() 就是写响应信息的一个方法
   - 对应每一种 http 请求方式（get、post等），把对应的处理逻辑写进同名的成员方法中（如对应 get 请求方式，就将对应的处理逻辑写在 get() 方法中）
   - 当没有对应请求方式的成员方法时，会返回 “405: Method Not Allowed” 错误。 
2. **tornado.web.Application**
   - Tornado Web框架的核心应用类，是与服务器对接的接口，里面保存了路由信息表，其初始化接收的第一个参数就是一个路由信息映射元组的列表
   - listen() 方法用来创建一个 http 服务器实例，并绑定到给定端口（**注意：此时服务器并未开启监听**）。 
3. **tornado.httpserver**
   -  tornado 的 HTTP 服务器实现 
4. **tornado.ioloop**
   - tornado 的核心 io 循环模块，封装了 Linux 的 epoll 和 BSD 的 kqueue，tornado 高性能的基石。 
   - **IOLoop.current()**： 返回当前线程的 IOLoop 实例 
   -  **IOLoop.start()**：  启动 IOLoop 实例的 I/O 循环，同时服务器监听被打开

![ioloop_epoll](images\ioloop_epoll.png)

### 编写思路

1. 创建 web 应用实例对象，第一个初始化参数为路由映射列表 
2. 定义实现路由映射列表中的 handler 类 
3. 创建服务器实例，绑定服务器端口 
4. 启动当前线程的 IOLoop 



### 单进程与多进程

刚刚实现的都是**单进程**，可以通过命令来查看：

```bash
$ ps -ef | grep server.py
```

修改代码， **一次启动多个进程**

```python
# coding:utf-8
# server.py

import tornado.web
import tornado.ioloop
import tornado.httpserver 


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        self.write("Hello index!")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.bind(8000)  # 将服务器绑定到指定端口
    http_server.start(num_processes=0)  # 指定启动的进程数
    tornado.ioloop.IOLoop.current().start()
```



说明：

1. app.listen() 只能在 **单进程** 模式中使用
2. http_server.bind(port)：将服务器绑定到指定端口
3. http_server.start(num_processes=1)：指定开启几个进程：
   - 参数num_processes默认值为1，即默认仅开启一个进程
   - 如果num_processes为None或者<=0，则自动根据机器硬件的cpu核芯数创建同等数目的子进程
   - 如果num_processes>0，则创建num_processes个子进程。

4. http_server.listen(8000)  等同于：

   ```python
   http_server.bind(8000)
   http_server.start(1)
   ```



##### 多进程注意点

虽然 tornado 给我们提供了一次开启多个进程的方法，但是由于：

- 每个子进程都会从父进程中复制一份 IOLoop 实例，如果在创建子进程前我们的代码动了 IOLoop 实例，那么会影响到每一个子进程，势必会干扰到子进程 IOLoop 的工作；
- 所有进程是由一个命令一次开启的，也就无法做到在不停服务的情况下更新代码；
- 所有进程共享同一个端口，想要分别单独监控每一个进程就很困难。

不建议使用这种多进程的方式，而是 **手动开启多个进程，并且绑定不同的端口**。



### 配置 - tornado.options

tornado.options 模块 —— 全局参数定义、存储、转换 



##### tornado.options.define()

用来定义 options 选项变量的方法，定义的变量可以在全局的 tornado.options.options 中获取使用，传入参数：

- **name**  选项变量名，须保证全局唯一性
- **default**  选项变量的默认值，如不传默认为None；
- **type**  选项变量的类型，从命令行或配置文件导入参数的时候 tornado 会根据这个类型转换输入的值，可以是 str、float、int、datetime、timedelta 中的某个 
  - 转换不成功时会报错
  - 若未设置则根据 default 的值自动推断
  - 若 default 也未设置，那么不再进行转换 
  - 可以通过利用设置type类型字段来过滤不正确的输入 
- **multiple** 选项变量的值是否可以为多个，布尔类型，默认值为 False，如果 multiple 为 True，那么设置选项变量时值与值之间用英文逗号分隔，而选项变量则是一个list列表（若默认值和输入均未设置，则为空列表 []） 
- **help** 选项变量的帮助提示信息，在命令行启动 tornado 时，通过加入命令行参数 --help　可以查看所有选项变量的信息（注意，代码中需要加入 tornado.options.parse_command_line()） 



##### tornado.options.options

 全局的 options 对象，所有定义的选项变量都会作为该对象的属性。 



##### tornado.options.parse_command_line()

转换命令行参数，并将转换后的值对应的设置到全局 options 对象相关属性上。追加命令行参数的方式是 --myoption=myvalue

```python
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello Itcast!")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
```

开启程序：

```bash
$ python server.py --port=8000
```



##### tornado.options.parse_config_file(path)

 从配置文件导入 option， 配置文件的书写格式需要按照 python 的语法要求 ： 

```
# 文件: config (允许非 py 文件)
myoption = "myvalue"
port = 8000
lan_lst = ["python","c++","java","php","ios"]  # 命令行配置的列表是逗号分隔
```

修改前面代码:

```python
# 前面仍然需要: tornado.options.define(...)...
# tornado.options.parse_command_line()
tornado.options.parse_config_file('./config')
```

##### 日志

当我们在代码中调用 parse_command_line() 或者 parse_config_file() 的方法时，tornado 会默认为我们配置标准 logging 模块，即默认开启了日志功能，并向标准输出（屏幕）打印日志信息。

如果想关闭 tornado 默认的日志功能，可以在命令行中添加 --logging=none 或者在代码中执行如下操作:

```python
from tornado.options import options, parse_command_line
options.logging = None
parse_command_line()
```

##### 最好的配置方式

prase_config_file() 的缺点:

- 我们看到在使用 prase_config_file() 的时候，配置文件的书写格式仍需要按照 python 的语法要求，其优势是可以直接将配置文件的参数转换设置到全局对象tornado.options.options 中
- 然而，其不方便的地方在于 **需要** 在代码中调用tornado.options.define() 来定义选项，而且 **不支持** 字典类型，故而在实际应用中大都不使用这种方法。

通常的配置方式:

- 在使用配置文件的时候，通常会新建一个 python 文件（如 config.py），然后在里面直接定义 python 类型的变量（可以是字典类型）
- 在需要配置文件参数的地方，将 config.py 作为模块导入，并使用其中的变量参数。

定义 config.py

```python
# conding:utf-8

# Redis 配置
redis_options = {
    'redis_host': '127.0.0.1',
    'redis_port': 6379,
    'redis_pass': '',
}

# Tornado app 配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret': '0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies': False,
    'login_url': '/login',
    'debug': True,
}

# 日志
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')
```

使用 config.py

```python
# conding:utf-8
# server.py

import tornado.web
import config

# ...

if __name__ = "__main__":
    app = tornado.web.Application([], **config.settings)

    # ...
```



# ====深入====

- Application 设置
- debug 模式
- 路由设置扩展
- RequestHandler 的使用
  - 输入方法
  - 输出方法
  - 可重写接口



### Application

##### settings

**debug**，设置 tornado 是否工作在调试模式，默认为 False 即工作在生产模式。当设置 debug=True 后，tornado 会工作在调试/开发模式，在此种模式下，tornado 为方便我们开发而提供了几种特性：

- **自动重启**，tornado应用会监控源代码文件，当有改动保存后便会重启程序。也可单独通过 autoreload=True 设置；
- **取消缓存编译的模板**，可以单独通过 compiled_template_cache=False 来设置；
- **取消缓存静态文件 hash 值**，可以单独通过 static_hash_cache=False 来设置；
- **提供追踪信息**，当 RequestHandler 或者其子类抛出一个异常而未被捕获后，会生成一个包含追踪信息的页面，可以单独通过 serve_traceback=True 来设置。

```python
app = tornado.web.Application([], debug=True)
```



##### 路由映射

```python
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")


class IndexHandler(RequestHandler):
    def get(self):
        # 路由反解析
        python_url = self.reverse_url("python_url")
        self.write('<a href="%s">Hello</a>' %
                   python_url)

        
class HelloHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            # 二元元组
            (r"/", Indexhandler),
        
            # 三元元组, 传参数给 HelloHandler 的 initialize() 方法
            (r"/cpp", HelloHandler, {"subject":"c++"}),
        
            # 非元组, 而是 tornado.web.url()
            # name是给路由起名，可以通过调用RequestHandler.reverse_url(name)来获取该名对应的 url
            url(r"/python", HelloHandler, {"subject":"python"}, name="python_url")

        ],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

```





### 输入

 利用HTTP协议向服务器传参有几种途径？ 

1. 查询字符串（query string)，形如 key1=value1&key2=value2；
2. 请求体（body）中发送的数据，比如表单数据、json、xml；
3. 提取 uri 的特定部分，如 /blogs/2016/09/0001，可以在服务器端的路由中用正则表达式截取；
4. 在 http 报文的头（header）中增加自定义字段，如 X-XSRFToken=token



tornado 中为我们提供了哪些方法来获取请求的信息 ?

##### 1. 查询字符串参数

两种方式

**get_query_argument(name, default=_ARG_DEFAULT, strip=True)**

- 从请求的查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
- default为设值未传name参数时返回的默认值，如若default也未设置，则会抛出tornado.web.MissingArgumentError异常。
- strip表示是否过滤掉左右两边的空白字符，默认为过滤。

**get_query_arguments(name, strip=True)**

- 从请求的查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表 []。
- strip 同前

##### 2. 请求体表单参数

两种方式

**get_body_argument(name, default=_ARG_DEFAULT, strip=True)**

- 从请求体中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
- default与strip同前，不再赘述。

**get_body_arguments(name, strip=True)**

- 从请求体中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。
- strip同前

**说明**

- 对于请求体中的数据要求为字符串，且格式为表单编码格式（与url中的请求字符串格式相同），即key1=value1&key2=value2，HTTP报文头Header中的"Content-Type"为application/x-www-form-urlencoded 或 multipart/form-data。
- **无法通过这两个方法获取 json 或 xml 请求体数据**

##### 前两类方法的整合方法

两种方式

**get_argument(name, default=_ARG_DEFAULT, strip=True)**

- 从请求体和查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。

**get_arguments(name, strip=True)**

- 从请求体和查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。

**说明**

**这两个方法最常用**。

##### 用例

```python
# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")


class IndexHandler(RequestHandler):
    def post(self):
        query_arg = self.get_query_argument("a")
        query_args = self.get_query_arguments("a")
        body_arg = self.get_body_argument("a")
        body_args = self.get_body_arguments("a", strip=False)
        arg = self.get_argument("a")
        args = self.get_arguments("a")

        default_arg = self.get_argument("b", "hello")
        default_args = self.get_arguments("b")

        try:
            missing_arg = self.get_argument("c")
        except MissingArgumentError as e:
            missing_arg = "We catched the MissingArgumentError!"
            print e
        missing_args = self.get_arguments("c")

        rep = "query_arg:%s<br/>" % query_arg
        rep += "query_args:%s<br/>" % query_args 
        rep += "body_arg:%s<br/>"  % body_arg
        rep += "body_args:%s<br/>" % body_args
        rep += "arg:%s<br/>"  % arg
        rep += "args:%s<br/>" % args 
        rep += "default_arg:%s<br/>" % default_arg 
        rep += "default_args:%s<br/>" % default_args 
        rep += "missing_arg:%s<br/>" % missing_arg
        rep += "missing_args:%s<br/>" % missing_args

        self.write(rep)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

##### 2+ 请求体 json, xml

- **body** 请求体数据；

  ```
  json.loads(self.body or "{}")
  ```

##### 2+ 请求体 file

- **files**  用户上传的文件，为字典类型，型如：

  ```
  {
    "form_filename1":[<tornado.httputil.HTTPFile>, <tornado.httputil.HTTPFile>],
    "form_filename2":[<tornado.httputil.HTTPFile>,],
    ... 
  }
  tornado.httputil.HTTPFile
      - filename 文件的实际名字，与form_filename1不同，字典中的键名代表的是表单对应项的名字；
      - body 文件的数据实体；
      - content_type 文件的类型。 
      
  这三个对象属性可以像字典一样支持关键字索引，如 request.files["form_filename1"][0]["body"]
  ```





##### 3.请求头

**headers** 请求的协议头，是类字典型的对象，支持关键字索引的方式获取特定协议头信息，例如：request.headers["Content-Type"]



##### 4.正则提取 uri

- tornado 中对于路由映射也支持正则提取 uri，提取出来的参数会作为 RequestHandler 中对应请求方式的成员方法参数。
- 若在正则表达式中定义了名字，则参数按名传递；
- 若未定义名字，则参数按顺序传递。提取出来的参数会作为对应请求方式的成员方法的参数。 

```python
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")


class SubjectCityHandler(RequestHandler):
    def get(self, subject, city):
        self.write(("Subject: %s<br/>City: %s" % (subject, city)))

        
class SubjectDateHandler(RequestHandler):
    def get(self, date, subject):
        self.write(("Date: %s<br/>Subject: %s" % (date, subject)))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/sub-city/(.+)/([a-z]+)", SubjectCityHandler), # 无名方式
        (r"/sub-date/(?P<subject>.+)/(?P<date>\d+)", SubjectDateHandler), #　命名方式
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```





##### 请求的其他信息

RequestHandler.request 对象存储了关于请求的相关信息，具体属性有：

- method HTTP的请求方式，如GET或POST;
- host 被请求的主机名；
- **remote_ip** 客户端的IP地址；
- uri 请求的完整资源标示，包括路径和查询字符串；
- path 请求的路径部分；
- query 请求的查询字符串部分；
- version 使用的HTTP版本；



### 输出

##### 1. write()

```python
# write方法是写到缓冲区的，我们可以像写文件一样多次使用write方法不断追加响应内容，最终所有写到缓冲区的内容一起作为本次请求的响应输出。


class IndexHandler(RequestHandler):
    def get(self):
        self.write("hello!")
        self.write("hello again!")
        self.write("hello again and again!")
        self.write(json.dumps({}))
        # 可以不用手动去做json序列化. Better:
        self.write({})
        
# write 方法除了帮我们将字典转换为 json 字符串之外，还帮我们将 Content-Type 设置为application/json; charset=UTF-8
```

##### 2. set_header()

```python
class IndexHandler(RequestHandler):
    def get(self):
        self.write(json.dumps({}))
        self.set_header("Content-Type", "application/json; charset=UTF-8")
```



##### 3. def set_default_headers()

- 该方法会在进入 HTTP 处理方法前先被调用，可以重写此方法来预先设置默认的headers。
- 注意：在 HTTP 处理方法中使用 set_header() 方法会覆盖掉在set_default_headers() 方法中设置的同名 header。 

```python
class IndexHandler(RequestHandler):
    def set_default_headers(self):
        # 设置get与post方式的默认响应体格式为json
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("name", "Martin")
    
    def get(self):
        self.write(json.dumps({}))
```



##### 4. set_status()

set_status(status_code, reason=None)

为响应设置状态码。

##### 5. redirect()

 告知浏览器跳转到url。 redirect(url)

##### 6. send_error()

send_error(status_code=500, **kwargs)

- 抛出HTTP错误状态码status_code，默认为500，kwargs为可变命名参数。
- 使用 send_error 抛出错误后 tornado 会调用 write_error() 方法进行处理，并返回给浏览器处理后的错误页面。
- 注意：使用 send_error() 方法后就不要再向输出缓冲区写内容了！ 

##### 7. write_error()

用来处理 send_error 抛出的错误信息并返回给浏览器错误信息页面。可以重写此方法来定制自己的错误显示页面。 

```python
class IndexHandler(RequestHandler):
    def get(self):
        username = self.get_argument("username")
        if not username:
            self.send_error(400, a='a', b='b')
        else:
            self.write("主页")

    def write_error(self, status_code, **kwargs):
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>错误名：%s</p>" % kwargs["a"])
        self.write(u"<p>错误详情：%s</p>" % kwargs["b"])
```





### 接口与调用顺序

**在正常情况未抛出错误时，调用顺序为：**

1. set_defautl_headers()
2. initialize()
3. prepare()
4. HTTP 方法
5. on_finish()

**在有错误抛出时，调用顺序为：**

1. set_default_headers()
2. initialize()
3. prepare()
4. HTTP方法   (抛出错误)
5. set_default_headers()
6. write_error()
7. on_finish()

```python
class IndexHandler(RequestHandler):

    def initialize(self):
        print("调用了initialize()")

    def prepare(self):
        print("调用了prepare()")

    def set_default_headers(self):
        print("调用了set_default_headers()")

    def write_error(self, status_code, **kwargs):
        print("调用了write_error()")

    def get(self):
        print("调用了get()")

    def post(self):
        print("调用了post()")
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print("调用了on_finish()")
```





# ====模板====

- 静态文件配置
  - static_path
  - StaticFileHandler
- 模板使用
  - 变量与表达式
  - 控制语句
  - 函数
  - 块



### 静态文件

##### static_path

我们可以通过向 web.Application 类的构造函数传递一个名为 **static_path** 的参数来告诉 Tornado 从文件系统的一个特定位置提供静态文件，如：

```python
app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
)
```

在这里，我们设置了一个当前应用目录下名为 statics 的子目录作为 static_path 的参数。现在应用将以读取 statics 目录下的 filename.ext 来响应诸如 /**static**/filename.ext 的请求，并在响应的主体中返回。

##### StaticFileHandler

 可以通过 **tornado.web.StaticFileHandler** 来自由映射静态文件与其访问路径url。 

```python
from pathlib import Path

curr_path = Path(__file__).parent
app = tornado.web.Application(
    [
        (r'^/()$', StaticFileHandler, {"path": curr_path / "statics/html", "default_filename":"index.html"}),
        (r'^/view/(.*)$', StaticFileHandler, {"path":curr_path / "statics/html}),
    ],
    static_path = curr_path / "statics"
)
"""
现在，对于静态文件statics/html/index.html，可以通过三种方式进行访问：
    http://127.0.0.1/static/html/index.html
    http://127.0.0.1/
    http://127.0.0.1/view/index.html
"""
```

- **path** 用来指明提供静态文件的根路径，并在此目录中寻找在路由中用正则表达式提取的文件名。
- **default_filename** 用来指定访问路由中未指明文件名时，默认提供的文件。



### 使用模板

使用模板，需要仿照静态文件路径设置一样，向web.Application类的构造函数传递一个名为 **template_path** 的参数来告诉 Tornado 从文件系统的一个特定位置提供模板文件，如：

```python
curr_path = Path(__file__).parent

app = tornado.web.Application(
    [(r'/', IndexHandler)],
    static_path = curr_path / "statics",
    template_path = curr_path / "templates",
)
```

 **在handler中使用render()方法来渲染模板并返回给客户端**。 

```python
class IndexHandler(RequestHandler):
    def get(self):
        data = {}
        self.render("index.html", **data, more='more') # 渲染模板，并返回给客户端。


curr_path = Path(__file__).parent

app = tornado.web.Application(
    [
        (r'^/$', IndexHandler),
        (r'^/view/(.*)$', StaticFileHandler, {"path": curr_path / "statics/html"}),
    ],
    static_path = curr_path / "statics",
    template_path=curr_path / "templates",
)
```



### 模板语法

##### 1 变量与表达式

```
{{}} 内可以放 变量, 也可放 python 表达式
```



##### 2 控制语句

```
{% if page is None %} {% end %}
{% if len(entries) == 3 %} {% end %}

{% if ... %} ... {% elif ... %} ... {% else ... %} ... {% end %}
{% for ... in ... %} ... {% end %}
{% while ... %} ... {% end %}
```



##### 3 函数

**static_url()**

```
<link rel="stylesheet" href="{{ static_url("style.css") }}">

对应渲染结果:
<link rel="stylesheet" href="/static/style.css?v=ab12">
```

优点：

- static_url 函数创建了一个基于文件内容的 hash 值，并将其添加到 URL 末尾（查询字符串的参数 **v**）。这个hash 值确保浏览器总是加载一个文件的最新版而不是之前的缓存版本。无论是在你应用的开发阶段，还是在部署到生产环境使用时，都非常有用，因为你的用户不必再为了看到你的静态内容而清除浏览器缓存了。
- 另一个好处是你可以改变你应用URL的结构，而不需要改变模板中的代码。例如，可以通过设置**static_url_prefix**来更改Tornado的默认静态路径前缀/static。如果使用static_url而不是硬编码的话，代码不需要改变。

**转义**

tornado中默认开启了模板自动转义功能，防止网站受到恶意攻击。

我们可以通过raw语句来输出不被转义的原始格式，如：

```python
{% raw text %}
```

> 注意：在Firefox浏览器中会直接弹出alert窗口，而在Chrome浏览器中，需要set_header("X-XSS-Protection", 0)

若要关闭自动转义，一种方法是在 Application 构造函数中传递 **autoescape=None**，另一种方法是在每页模板中修改自动转义行为，添加如下语句：

```python
{% autoescape None %}
```

**escape()**

关闭自动转义后，可以使用 escape() 函数来对特定变量进行转义，如：

```python
{{ escape(text) }}
```

**自定义函数**

支持将 python 函数通过 self.render() 传给模板引擎,  然后在模板引擎中执行函数



##### 4 块

使用块来复用模板，块语法如下：

```python
{% block block_name %}
...
{% end %}
```

使用块

```
{% extends "base.html" %}

{% block block_name %}
    <div>此处重写了 block 的内容</div>
{% end %}
```



# ====后续见 [tornado_02.md](tornado_02.md)====

# 数据库

# 安全应用

# 异步与 Websocket