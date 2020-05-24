# Flask框架  - 视图与路由

- 安装虚拟环境
- 创建 Py2 和 Py3 版本的虚拟环境
- 使用 pip 命令安装指定版本 Flask 及其他扩展
- Flask 从对象中加载配置
- 带有参数的路由及视图函数
- url_for 函数的作用
- 自定义转换器的步骤
- 装饰器路由实现的几个关键的类
- HTTP 状态保持的原理
- Flask 各个上下文对象
- Flask-Script 扩展的作用





## 1 Flask介绍

### 1.1 Web应用程序访问流程

- 什么是Web应用程序 ?

Web应用程序是一种可以通过Web访问的应用程序.

一个Web应用程序是由完成特定任务的各种Web组件构成的,  并通过Web将服务展示给外界。在实际应用中，Web应用程序是由多个Servlet、JSP页面、HTML文件以及图像文件等组成。所有这些组件相互协调为用户提供一组完整的服务。

<img src=".\Flask框架__01_images\Web应用程序交互流程.png" alt="Web应用程序交互流程" style="zoom: 33%;" />

- 什么是Web框架？

协助开发者快速开发 Web 应用程序的一套功能代码

- 为什么要用Web框架？

> 让成熟，稳健的框架来处理一些基础的工作，比如安全性，数据流控制等,  以便程序开发人员可以把精力放在具体的业务逻辑上.

- 使用框架的优点: 

> 稳定性和可扩展性强

> 降低开发难度，提高开发效率

- 在 Python 中常用的 Web 框架有哪些 ?

> Flask  Django  Tornado



### 1.2 Flask框架

Flask 本身相当于一个内核,  其他几乎所有的功能都要用到第三方的扩展来实现.

Flask框架  ---->  Flask(内核) + 大量第三方扩展

Django框架  ---->  自身集成大量功能 + 第三方扩展

Tornado框架  ---->  非阻塞式服务器，运用了 `epoll` ,  每秒可以处理数以千计的连接，是实时 Web 服务的一个 理想框架。



#### **常用扩展**

-  Flask-SQLalchemy：操作数据库；
-  Flask-script：插入脚本；
-  Flask-migrate：管理迁移数据库；
-  Flask-Session：Session存储方式指定；
-  Flask-WTF：表单；
-  Flask-Mail：邮件；
-  Flask-Bable：提供国际化和本地化支持，翻译；
-  Flask-Login：认证用户状态；
-  Flask-OpenID：认证；
-  Flask-RESTful：开发REST API的工具；
-  Flask-Bootstrap：集成前端Twitter Bootstrap框架；
-  Flask-Moment：本地化日期和时间；
-  Flask-Admin：简单而可扩展的管理接口的框架

> 扩展列表：[http://flask.pocoo.org/extensions/](http://flask.pocoo.org/extensions/)

#### 文档

1. 中文文档（[http://docs.jinkan.org/docs/flask/](http://docs.jinkan.org/docs/flask/)）
2. 英文文档（[http://flask.pocoo.org/docs/0.11/](http://flask.pocoo.org/docs/0.11/)）



#### Flask 框架的 2 大核心

```
1 WSGI 工具箱 (后端方面)
	Werkzeug（路由模块）
2 模板引擎 (前端方面)
	Jinja2
```



## 2 虚拟环境

### 2.1 为什么要搭建虚拟环境?

​	不同项目要用到同一个包的不同版本时, 为了避免版本覆盖, 可以搭建独立的`python运行环境`, 使得单个项目的运行环境与其它项目互不影响.

**虚拟环境最终搭建的路径:**

- 所有的`虚拟环境`都位于`/home/`下的隐藏目录`.virtualenvs`下



### 2.2 如何搭建虚拟环境?

#### 1 安装虚拟环境

```python
# python3 安装虚拟环境
  sudo pip3 install virtualenv
  sudo pip3 install virtualenvwrapper

# python2 安装虚拟环境
  sudo pip install virtualenv
  sudo pip install virtualenvwrapper
```

#### 2 配置环境变量

```python

安装完虚拟环境后，如果提示找不到 mkvirtualenv 命令，须配置环境变量：

# 1、创建目录, 存放虚拟环境
  mkdir $HOME/.virtualenvs

# 2、默认会将virtualenvwrapper安装到/usr/local/bin目录下, 需要在用户的 ~/.bashrc 文件中增加如下配置:
  export WORKON_HOME=$HOME/.virtualenvs
  source /usr/local/bin/virtualenvwrapper.sh

# 3、运行
  source ~/.bashrc
```



##### *** 运行source ~/.bashrc可能出现的错误

**根据步骤，当运行source ./.bashrc报错:**

 ![img01](.\Flask框架__01_images\img01.png)

**错误原因**

```
	Ubuntu安装了 2.7 和 3.x 两个版本的 python, 在安装时使用的是 sudo pip3 install virtualenvwrapper
在运行时默认使用的是python2.x, 但在python2.x中不存在对应的模块。
```

**先看看virtualenvwrapper.sh文件的相关内容:**

![img02](.\Flask框架__01_images\img02.png)

```
	当不存在VIRTUALENVWRAPPER_PYTHON环境时, 会默认选择使用 which python, 需要配置 VIRTUALENVWRAPPER_PYTHON 环境来解决当前问题
```

**配置 VIRTUALENVWRAPPER_PYTHON 环境**

```python
# 以root权限打开 virtualenvwrapper.sh
  sudo vim /usr/local/bin/virtualenvwrapper.sh

# 可以紧接在which python那一句的后一行 增加环境变量:
  VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

# 再运行
  source ~/.bashrc
```



## 3 创建虚拟环境

```python
---------要创建虚拟环境, 必须先联网----------

在python3中，创建虚拟环境
  mkvirtualenv -p python3 虚拟环境名称		# -p 表示要指定python版本

在python2中，创建虚拟环境
  mkvirtualenv 虚拟环境名称
```




### 3.1 如何使用虚拟环境?

- 查看虚拟环境

```
workon 两次tab键
```

- 使用虚拟环境

```
workon 虚拟环境名称
```

- 退出虚拟环境

```
deactivate
```

- 删除虚拟环境

```
第一种: 通过命令删除
    先退出：deactivate
    再删除：rmvirtualenv 虚拟环境名称

第二种: 直接删除虚拟环境的目录
```



### 3.2 如何在虚拟环境中安装工具包?

#### 1 工具包安装的位置

- python2版本下：

```
~/.virtualenvs/py_flask/lib/python2.7/site-packages/
```

- python3版本下：

```
~/.virtualenvs/py3_flask/lib/python3.5/site-packages/
```

  


#### 2 安装flask-0.10.1包

```
pip3 install flask==0.10.1
```



#### 3 查看虚拟环境中安装的包

```python
# 查看 系统环境/虚拟环境 中安装的包
pip freeze
```

![img03](.\Flask框架__01_images\img03.png)



## 4 创建 Python 项目

打开 Pycharm，创建 `Pure Python` 类型的项目,  解释器为虚拟环境下的解释器

![选择Python解析器](.\Flask框架__01_images\选择Python解析器.png)



### 4.1 最简单的 Flask 应用程序

- 新建文件helloworld.py
- 导入 Flask 类

```python
from flask import Flask
```

Flask类接收一个参数 `__name__`，它会指向程序所在的包,  Flask 用这个参数决定程序的根目录，以便后面能够找到相对于程序根目录的资源文件位置。

```python
app = Flask(__name__)  # 根据Flask类 创建一个 WSGI 应用程序
```

#### \_\_name\_\_ 理解

----------------

![__name__理解](.\Flask框架__01_images\__name__理解.png)





- 装饰器的作用:    **将路由映射到视图函数** index

```python
@app.route('/')
def index():
    return 'Hello World'
```

- Flask应用程序实例的 run 方法 启动 WEB 服务器

```python
if __name__ == '__main__':
    app.run()
```

- 在程序运行过程中，程序实例中会使用 `url_map` 将 `装饰器路由 和 视图 的对应关系` 保存起来

```python
print(app.url_map)
默认会得到的结果:
    Map([<Rule '/' (HEAD, GET, OPTIONS) -> index>, <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>])
```



#### *** 解决 flask 端口被占用的问题

在编辑flask代码时，如果没有关闭flask的程序，默认的5000 端口一直被占用。 
再次运行的时候，会显示：

```python
socket.error: [Errno 48] Address already in use
```

**第一步:  根据端口查进程**

================ 第一种终端命令:  lsof  -i:5000================

================ 第二种终端命令:  netstat -apn | grep 5000 ================

**第二步: 杀死进程**

```python
sudo -9 kill (进程号PID)
```



### 4.2 相关配置参数

#### Flask 程序初始化参数

```python
"""
部分源代码
def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False):
"""
```

```python
app = Flask(__name__,  # 第一个参数指向程序所在的包, 决定静态文件从哪个位置开始找
            static_path='/static',  # 不再用, 源代码中把它赋值给了下面的 static_url_path
            static_url_path='/static',  # 默认值, 表示 静态文件访问地址
            static_folder='static',  # 默认值, 表示 静态文件存放的目录
            template_folder='templates'  # 默认值, 模板文件存放的目录
            )
```



- **import_name**
  - Flask程序所在的包(模块)，决定 Flask 在访问静态文件时查找的路径
  - 传 `__name__` 就可以
- static_path
  - 静态文件访问路径 (不推荐使用，使用 static_url_path 代替)
- **static_url_path**
  - 静态文件访问路径，默认为：`/ + static_folder`
- **static_folder**
  - 静态文件存储的文件夹，默认为 `static`
- **template_folder**
  - 模板文件存储的文件夹，默认为 `templates`




#### Flask 程序相关配置de加载方式

在 Flask 程序运行的时候，可以给 Flask 设置相关配置，比如：配置 Debug 模式，配置数据库连接地址等等，设置 Flask 配置有以下方式：

```python
# 1. 从配置类对象中加载 (常用, 重要)
  app.config.from_object()
    #a.
    app.config.from_object('yourapplication.default_config')
    #b.
    from yourapplication import default_config
    app.config.from_object(default_config)
    
# 2. 从配置文件中加载 (重要)
  app.config.from_pyfile()
    
# 3. 从环境变量中加载 (了解)
  app.config.from_envvar()
    
# from_envvar内部调用了from_pyfile, from_pyfile内部调用了 from_object. 可查源码
    
# + 注意: 一些常用的配置可以通过 app. 的形式设置(也可读取), 如:
 
        app.debug = True
        app.config['DEBUG'] = True
        app.run()
        # app.run(debug=True)
        
# + 注意: app.run()中可以传入调式模式的配置/端口号/主机ip,  即额外传入 debug=True, port=xxx, host=xxx
```



以下演练以设置应用程序的 DEBUG (调试模式) 为例，设置应用为调式模式后，可以实现以下功能：

> 1. 程序代码修改后可以自动重启服务器

> 2. 在服务器出现相关错误的时候可以直接将错误信息进行抛出到控制台打印



**第 1 种: 配置对象**

- 从配置对象中加载，创建配置的类，代码如下：

```python
# 配置对象，里面定义需要给 APP 添加的一系列配置
class Config(object):
    DEBUG = True

# 创建 Flask 类的对象,指向程序所在的包的名称
app = Flask(__name__)

# 从配置对象中加载配置
app.config.from_object(Config)
```

> 运行测试，在修改代码之后直接保存，会自动重启服务器



**第 2 种: 配置文件**

- 创建配置文件 `config.ini`，在配置文件中添加配置

<img src=".\Flask框架__01_images\创建配置文件.png" alt="创建配置文件" style="zoom: 50%;" />



- 使用代码加载配置

```python
# 创建 Flask 类的对象, 指向程序所在的包的名称
app = Flask(__name__)

# 从配置文件中加载配置
app.config.from_pyfile('config.ini')
```



**第 3 种: 环境变量**

将配置文件的路径存入环境变量中,  将环境变量名传给 app.config.from_envvar(variable_name)



#### 读取配置值

- app.config.get()
- 在视图函数中写 current_app.config.get()



#### app.run() 参数

- 可以指定运行的主机 `IP地址 host=0.0.0.0`，`端口 port=5000`，`是否开启调试模式 debug=True`

```python
app.run(host="0.0.0.0", port=5000, debug=True)
# 0.0.0.0 表示所有IP地址,  这会让操作系统监听所有公网 IP。
```



## 5 路由的基本定义

- 怎么定义路由(装饰器) ?

- 怎么指定访问方式 ?


### 5.1 指定路由地址

```python
# 指定访问路径为 demo1
@app.route('/demo1')
def demo1():
    return 'demo1'

访问url: 127.0.0.1:5000/demo1
```

### 5.2 给路由传参

有时需要将同一类 URL 映射到同一个视图函数处理，即  **动态处理 同一类 URL**.

比如：使用同一个视图函数来显示不同用户的个人信息。

```python
# 路由传参
@app.route('/user/<user_id>')
def user_info(user_id):  # 视图函数接收参数
    return 'hello %s' % user_id

访问url: 127.0.0.1:5000/user/22222
```

- 路由传递的参数默认当做 string 处理，也可以指定参数的类型

```python
# 路由传参 ---- 指定参数的类型
@app.route('/user/<int:user_id>')  # int后的 ":" 号之后不能写space
def user_info(user_id):
    return 'hello %d' % user_id
```

> 这里指定int，尖括号中的内容是动态的，在此暂时可以理解为只接受 **int 类型** 的值，否则访问不到
>
> 实际上 int 代表使用 IntegerConverter 去处理 url 传入的参数

### 5.3 methods指定请求方式

在 Flask 中，定义一个路由，默认的请求方式为：

- GET
- OPTIONS(自带)
- HEAD(自带)

如果想添加请求方试，那么可以如下指定：

```python
@app.route('/demo2', methods=['GET', 'POST'])
def demo2():
    # 直接从请求中取到请求方式并返回
    return request.method
```

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()
```



#### 请求方式

`GET`	 浏览器告知服务器：只 *获取* 页面上的信息

`POST`	 浏览器告诉服务器：想在 URL 上 *发布* 新信息。并且，服务器必须确保 数据已存储且仅存储一次。这是 HTML 表单通常发送数据到服务器的方法。

`PUT`	 修改服务器上的数据, 完整数据的推送.  类似 POST 但是服务器可能触发了存储过程多次，多次覆盖掉旧值。考虑到传输中连接可能会丢失，在 这种 情况下浏览器和服务器之间的系统可能安全地第二次接收请求，而 不破坏其它东西。因为 POST它只触发一次，所以用 POST 是不可能的。

`PATCH`	 修改服务器上的数据, 只推送修改的那一条数据

`DELETE`	 删除给定位置的信息。

`OPTIONS` 向服务器询问请求的方式和返回的数据格式

`HEAD`	 与GET类似, HEAD只需要响应头和状态码, 不要响应体,  在 Flask 中你完全无需 人工 干预，底层的 Werkzeug 库已经替你打点好了。



### 5.4 使用 PostMan 对请求进行测试

​	PostMan 是一款功能强大的**网页调试与发送网页 HTTP 请求的 Chrome 插件**，可以直接去对我们写出来的路由和视图函数进行调试，**作为后端程序员是必须要知道的一个工具**。



如果要测试 POST请求,  就要用**Chrome 浏览器插件** `PostMan`



### 5.5 视图常用逻辑

#### 返回JSON -- **jsonify({'a': 3, 'b': 4}, c=5, d=6)** 

- JSON有什么作用 ?

后端与前端通过 json 进行数据交换

- 怎么使用 flask.json ?

在使用 Flask 写一个接口时候需要给客户端返回 JSON 数据，在 Flask 中可以直接使用 **jsonify( json_dict )** 生成一个 JSON 的响应

```python
# 返回JSON
@app.route('/demo4')
def demo4():
    json_dict = {
        "user_id": 10,
        "user_name": "laowang"
    }
    return jsonify(json_dict)
# jsonify()第一个参数传对象, 如字典, 其余参数传关键字参数, 即形如 a=1
```

> 不推荐使用 json.dumps 转成 JSON 字符串直接返回，因为返回的数据要符合 HTTP 协议规范，如果是 JSON 需要指定 **content-type:application/json**

#### 标准响应方式

```python
return  响应体(json), 状态码,  响应头
```

![依次返回响应体 状态码 响应头](.\Flask框架__01_images\依次返回响应体 状态码 响应头.png)

#### 

#### 重定向 redirect() 和 **反向解析函数 url_for()**  

1 | 2 | 3

1  重定向到 **百度** 官网 ---- **redirect('url')**

```python
# 重定向到 url
@app.route('/demo')
def demo():
    return redirect('http://www.baidu.com')
```



2 重定向到自定义的视图函数

(1) 可以直接填写 路由url  ---- **redirect('/index')**

(2) 也可以使用 **反向解析函数 url_for()** 生成指定视图函数所对应的 url ----> **redirect ( url_for ( " 视图函数名 " ) )**

```python
@app.route('/demo1')
def demo1():
    return 'demo1'

# 重定向到自定义的视图函数
@app.route('/demo5')
def demo5():
    # 反向解析函数: url_for()
    return redirect(url_for('demo1'))  
```



3 重定向到带参数的视图函数 ----  **redirect ( url_for ( "视图函数名" ,  var=var ) )**

反向解析函数 **传参**

```python
# 路由传递参数
@app.route('/user/<int:user_id>')
def user_info(user_id):
    return 'hello %d' % user_id

# 重定向到带有参数的视图函数
@app.route('/demo5')
def demo5():
    # 使用 url_for 生成指定视图函数所对应的 url
    return redirect(url_for('user_info', user_id=100))
```

**url_for( ):**

- 取到指定视图函数所对应的路由URL,  并且可以携带参数:

  - 可以携带url路径参数,  如 上面的url_for('user_info', user_id=100) 组成的url为:  

    `http://127.0.0.1:5000/user_info/100`

  - 也可以携带查询字符串参数, 如 url_for("test", add_param=12306) 可能组成url为:  

    `http://127.0.0.1:5000/test?add_param=12306`



#### 自定义状态码

- 在 Flask 中，可以很方便的返回自定义状态码，以实现不符合 http 协议的状态码，例如：status code: 666
- **工作中经常会自定义状态码**

```python
@app.route('/demo6')
def demo6():
    # 第二个返回值返回一个状态码
    return '状态码为 666', 666
```



## 6 正则匹配路由

​	在 web 开发中，可能会出现限制用户访问规则的场景，这个时候就需要用到正则匹配，根据自己的规则去限定请求参数再进行访问

**具体实现步骤为：**

- 导入转换器基类：在 Flask 中，所有的路由的匹配规则都是使用转换器对象进行记录
- 自定义转换器：自定义类继承于转换器基类 BaseConverter
- 添加转换器到默认的转换器字典中
- 使用自定义转换器实现自定义匹配规则



### 6.1 自定义转换器

- 1 导入转换器基类：在 Flask 中，所有的路由的匹配规则都是使用转换器对象进行记录

  ```python
  from werkzeug.routing import BaseConverter
  ```

- 2 自定义转换器：自定义类继承于转换器基类

  ```python
  # 自定义正则转换器
  # 1 定义一个类, 继承自 BaseConverter 父类
  class RegexConverter(BaseConverter):
      # 2 重写__init__方法, 传入 url_map 和 不定长参数*args
      def __init__(self, url_map, *args):
          super(RegexConverter, self).__init__(url_map)   # 3 调用父类的__init__(url_map)方法
          self.regex = args[0]   # 4 将接受的第1个参数当作匹配规则进行保存
  ```

#### app.url_map

  **存储 url 与 视图函数 的映射**



- 3 添加转换器到默认的转换器字典中,    `app.url_map.converters["key_name"] = 自定义转换器类名`

  ```python
  app = Flask(__name__)

  # 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: re
  app.url_map.converters['re'] = RegexConverter
  ```

- 4 使用自定义转换器实现自定义匹配规则

  ```python
  @app.route('/user/<re("[0-9]{3,6}"):user_id>')
  def user_info(user_id):
      return "user_id 为 %s" % user_id
  ```

>如果访问的url不符合规则，会提示找不到页面  Not Found



### 6.2 自定义转换器类的方法实现

​	继承于自定义转换器之后，还可以实现 `to_python` 和 `to_url` 这两个函数去对匹配参数做进一步处理：

#### to_python

- 处理 经过路由匹配之后 的参数
- 该函数参数中的 value 值代表匹配到的值，可输出进行查看
- 匹配完成之后，对匹配到的参数作最后一步处理再返回，比如：转成 int 类型的值再返回：

```python
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # 将接受的第1个参数当作匹配规则进行保存
        self.regex = args[0]

    def to_python(self, value):
        # 转成 int 类型的值再返回
        return int(value)
```

> 运行测试，在视图函数中可以查看参数的类型，由之前默认的 str 已变成 int 类型的值



**———————— Test_code ————————**

```python
from flask import Flask, url_for
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):   # url_map, regex
        super(MyConverter, self).__init__(url_map)  # 重写父类方法
        self.regex = regex


class ListConverter(BaseConverter):
    # 匹配url中参数必须为: 数字, 数字之间以','分隔
    regex = "([\\d]+,?)+\\d$"

    # ——————————————— in converter of demo2: to_python() ——————————————————
    def to_python(self, value):
        """todo 当匹配到参数之后，对参数做进一步处理之后，再返回给视图函数中"""
        # return value
        return value.split(',')


app = Flask(__name__)

# todo 将 自定义的转换器 添加到 默认的转换器列表中
app.url_map.converters['my_re'] = MyConverter
app.url_map.converters['more_id'] = MyListConverter


# ———————————————— demo1: re ————————————————
# url:  http://127.0.0.1:5000/users/12    response: Not Found
# url:  http://127.0.0.1:5000/users/123   response: user_id=123
@app.route('/user/<my_re("[0-9]{3,6}"):user_id>')
def demo1(user_id):
    return 'in demo1, user_id=%s' % user_id


# ———————————————— demo2: list ————————————————
# url:  http://127.0.0.1:5000/users/11,22,33    response: user_ids=['11', '22', '33']
@app.route('/users/<more_id:user_ids>')
def demo2(user_ids):
    return "in demo2, user_ids=%s" % user_ids


if __name__ == '__main__':
    app.run(debug=True)
```





#### to_url

- 路由匹配之前 处理url_for中传入的参数
- 在使用 url_for 去获取视图函数所对应的 url 的时候，会调用此方法对 url_for 后面传入的视图函数参数做进一步处理
- 具体可参见 Flask 的 app.py 中写的示例代码：ListConverter


**———————— Test_code ————————**


```python
from flask import Flask, url_for
from werkzeug.routing import BaseConverter
from werkzeug.utils import redirect


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex


class ListConverter(BaseConverter):
    # 匹配url中参数必须为: 数字, 数字之间以','分隔
    regex = "([\\d]+,?)+\\d$"

    # ——————————————— in converter of demo2: to_python() ——————————————————
    def to_python(self, value):
        """当匹配到参数之后，对参数做进一步处理之后，再返回给视图函数中"""
        # return value
        return value.split(',')

    # todo——————————— demo2对应增加 to_url(), 将[列表]参数转为 以','分隔的字符串 —————————————
    def to_url(self, value):
        """使用url_for()的时候，对视图函数传的参数进行处理，处理完毕之后以便能够进行路由匹配"""
        # return value
        # return "123"
        ret = ",".join(str(i) for i in value)
        return ret


app = Flask(__name__)
app.url_map.converters['my_re'] = RegexConverter
app.url_map.converters['more_id'] = ListConverter


# ———————————————— demo1: re ————————————————
# url:  http://127.0.0.1:5000/users/12    response: Not Found
# url:  http://127.0.0.1:5000/users/123   response: user_id=123
@app.route('/user/<my_re("[0-9]{3,6}"):user_id>')
def demo1(user_id):
    return 'in demo1, user_id=%s' % user_id


# ———————————————— demo2: list ————————————————
#  url:  http://127.0.0.1:5000/users/11,22,33    response: user_ids=['11', '22', '33']
@app.route('/users/<more_id:user_ids>')
def demo2(user_ids):
    return "in demo2, user_ids=%s" % user_ids


# todo ———————————————— demo3 ————————————————
# url:  http://127.0.0.1:5000/demo3    response: in demo2, user_ids=['11', '22', '33']
@app.route('/demo3')
def demo3():
    # todo 从demo3重定向到demo2, 并传入 user_ids 的 [列表]
    return redirect(url_for('demo2', user_ids=[11, 22, 33]))


if __name__ == '__main__':
    app.run(debug=True)
```




### 6.3 内置转换器

```python
# werkzeug\routing.py

# flask 内置的转换器有 6 种:  
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
```

> 系统自带的转换器具体使用方式在每种转换器的注释代码中有写，可以留意每种转换器初始化的参数。



## 7 异常捕获

### 7.1 HTTP 异常主动抛出

- abort 方法
  - 抛出一个给定状态代码的 HTTPException 或者 指定响应，例如想要用一个页面未找到异常来终止请求，你可以调用 abort(404)。
- 参数：
  - code – HTTP的错误状态码

```python
# abort(404)
abort(500)
```

> 抛出状态码的话，**只能抛出 HTTP 协议的错误状态码**

### 7.2 捕获错误

- errorhandler 装饰器
  - 注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
- 参数：
  - code_or_exception – HTTP的错误状态码或指定异常
- 例如统一处理状态码为500的错误给用户友好的提示：

```python
@app.errorhandler(500)
def internal_server_error(e):
    return '服务器搬家了'
```

- 捕获指定异常

```python
@app.errorhandler(ZeroDivisionError)
def zero_division_error(e):
    return '除数不能为0'
```



**———————— Test_code ————————**

```python
from flask import Flask
from werkzeug.exceptions import abort

app = Flask(__name__)


@app.route('/demo1')
def demo1():

    # 1 主动抛出一个状态码404 异常
    # abort(404)

    # 2 主动抛出一个除0 异常
    a = 0
    b = 1 / a

    # 遇到异常, 不会执行到 return 这一句
    return 'Hello World'


# ——————————— 捕获指定状态码的异常, 如: 404 ———————————
@app.errorhandler(404)      # todo 点进去看 app.errorhandler 的源码, 以及使用案例
def page_not_found(error):
    html = """<h2 style="color: skyblue;">咦, 页面怎么不见了?</h2><br />"""
    # return error  # 默认的那一句
    return html, 404


# ——————————— 捕获指定类型的异常, 如: 除零错误 ———————————
@app.errorhandler(ZeroDivisionError)
def zero_division_error(error):
    return "除数不能为 0 !"


if __name__ == '__main__':
    app.run(debug=True)
```



## 8 请求钩子

### 8.1 C/S交互的准备或扫尾工作

在客户端和服务器交互的过程中，有些准备工作或扫尾工作需要处理，比如：

```
- 在请求开始时，建立数据库连接；
- 在请求开始时，根据需求进行权限校验；
- 在请求结束时，指定数据的交互格式；
```



### 8.2 4种请求钩子

为了让每个视图函数避免编写重复功能的代码，Flask提供了通用设施的功能，即 **请求钩子**。

请求钩子是**通过装饰器的形式实现**，Flask支持如下 **四种请求钩子**：

- before_first_request
  - 在处理第一个请求前执行
- before_request
  - 在每次请求前执行
  - 如果在被修饰的函数中 返回了一个响应 (return "str")，视图函数将不再被调用, 请求当前服务器时 浏览器显示的一直只会是 "str"
- after_request
  - 如果没有抛出错误，在每次请求后执行
  - 接受一个参数：视图函数作出的响应
  - 在此函数中可以对响应值在返回之前做最后一步修改处理
  - 需要将参数中的响应在此参数中继续进行 return
- teardown_request
  - 在每次请求后执行
  - 接受一个参数：错误信息(exc)，如果没有相关错误抛出时 exc 为 None

### 8.3 代码测试

```python
from flask import Flask
from flask import abort

app = Flask(__name__)


# 在第一次请求之前调用，可以在此方法内部做一些初始化操作
@app.before_first_request
def before_first_request():
    print("before_first_request")


# 在每一次请求之前调用，这时候已经有请求了，可能在这个方法里面做请求的校验
# 如果请求的校验不成功，可以直接在此方法中进行响应，直接return之后那么就不会执行视图函数
@app.before_request
def before_request():
    print("before_request")
    # if 请求不符合条件:
    #     return "laowang"


# 在执行完视图函数之后会调用，并且会把视图函数所生成的响应传入,可以在此方法中对响应做最后一步统一的处理
@app.after_request
def after_request(response):
    print('@app.after_request. response=%s' % response)
    return response


# 每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息
@app.teardown_request
def teardown_request(e):
    if exc is not None:
        print('Error occured: %s' % exc)
    print('@app.teardown_request. exc=%s' % exc)


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    app.run(debug=True)
```



## 9 装饰器路由具体实现梳理

### 9.1 flask路由实现代码结构

<img src=".\Flask框架__01_images\Flask路由实现代码结构.png" alt="Flask路由实现代码结构" style="zoom: 50%;" />

![装饰器路由的实现](.\Flask框架__01_images\装饰器路由的实现.png)



### 9.2 Flask两大核心：Werkzeug 和 Jinja2

```
- Werkzeug实现路由、调试和Web服务器网关接口
- Jinja2实现了模板。
```

​	Werkzeug是一个遵循WSGI协议的python函数库

```
- 其内部实现了很多Web框架底层的东西，比如request和response对象；
- 与WSGI规范的兼容；支持Unicode；
- 支持基本的会话管理和签名Cookie；
- 集成URL请求路由等。
```

​	Werkzeug 库的 routing 模块负责实现 URL 解析。不同的 URL 对应不同的视图函数，routing 模块会对请求信息的 URL 进行解析，匹配到 URL 对应的视图函数，执行该函数以此生成一个响应信息。

routing 模块内部有：

- Rule 类
  - 用来构造不同的 URL 模式的对象，路由 URL 规则
  - 描述 视图函数与路由 URL 之间的映射关系
- Map 类
  - 存储 所有的 URL 规则 和 一些配置参数
- BaseConverter 的子类
  - 负责定义 URL 的匹配规则
- MapAdapter 类
  - 负责协调 Rule 做具体的匹配的工作




## 10  request 对象

request 就是flask中代表当前请求的 request 对象，其中一个请求上下文变量(理解成全局变量，在视图函数中直接使用可以取到当前本次请求)

### 10.1 常用属性

| 属性              | 说明                                       | 类型             |
| --------------- | ---------------------------------------- | -------------- |
| request.data    | POST/GET请求.  记录请求的数据，并转换为字符串             | *              |
| request.json    | POST/GET请求.  记录请求的数据，相当于json.loads(request.data) | 字典             |
| request.form    | POST请求. 记录请求中的表单数据                       | MultiDict (字典) |
| request.args    | GET请求. 记录请求中的查询参数 (URL中 "?" 后的参数)        | MultiDict (字典) |
| request.headers | 记录请求中的报文头                                | EnvironHeaders |
| request.cookies | 记录请求中的cookie信息                           | Dict (字典)      |
| request.method  | 记录请求使用的HTTP方法                            | GET/POST       |
| request.url     | 记录请求的URL地址                               | string         |
| request.files   | POST请求. 记录请求上传的文件                        | *              |



### 10.2 部分示例

```python
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return '----index----'

# 使用 PostMan 模拟浏览器发出请求, 在路由函数中使用request处理 GET 和 POST 请求
# ———————————— 接收浏览器上传文件 - POST请求 ————————————
# 1 给路由指定参数 methods=列表
@app.route("/recv_file", methods=["POST", "GET"])
def recv_file():
    if request.method == "POST":

        # 2 根据key--image01 获取文件
        file = request.files.get("image01")
        # 3 指定路径及名称， 另存文件
        file.save("client_post_img.jpg")
        # 4 返回 response
        return "post ok"
    # GET请求时会执行:
    return "now get, please post..."

# ———————————— 接收浏览器提交表单数据 - POST请求 ————————————
# 1 给路由指定参数 methods=列表
@app.route("/recv_form_data", methods=["POST", "GET"])
def recv_form_data():
    if request.method == "POST":

        # 获取浏览器提交的表单 --- 表单对象: ImmutableMultiDict字典
        form_dict = request.form

        # 表单字典取值
        # name = form_dict["name"]
        name = form_dict.get("name")
        age = form_dict.get("age")
        print(request.url)
        return "post ok"
    return "now get, please post..."


# ———————————— 获取浏览器请求的url中的键值对(URL中 "?" 后的参数) - GET请求 ————————————
@app.route("/recv_args", methods=["POST", "GET"])
def recv_args():
    if request.method == "GET":
        args_ = request.args
        name = args_.get("name")
        age = args_.get("age")
        # 顺便看看request.headers能获取到什么
        # print(request.headers)
        print(request.headers.get("User-Agent"))
        return "Are you sure to get: (%s, %s) ???" % (name, age)
    return "now POST, please GET..."


if __name__ == '__main__':
    app.run(debug=True, host="192.168.18.50")
```



## 11 http 状态保持

### 11.1 什么是 无状态 ?

- 因为 http 是一种无状态协议，浏览器请求服务器是无状态的。
- **无状态**：指一次用户请求时，浏览器、服务器无法知道之前这个用户做过什么，每次请求都是一次新的请求。 每次请求都是独立的.
- **无状态原因**：浏览器与服务器是使用 socket 套接字进行通信的，服务器将请求结果返回给浏览器之后，会关闭当前的 socket 连接，而且服务器也会在处理页面完毕之后销毁页面对象。
- 有时需要保持下来用户浏览的状态，比如用户是否登录过，浏览过哪些商品等




### 11.2 实现状态保持主要 2 种方式

- 在 `客户端` 存储信息使用 `Cookie`
- 在 `服务器端` 存储信息使用 `Session`





> **无状态协议**：
>
> 1. 协议对于事务处理没有记忆能力
> 2. 对同一个 url 请求没有上下文关系
> 3. 每次的请求都是独立的，它的执行情况和结果与前面的请求和之后的请求是无直接关系的，它不会受前面的请求应答情况直接影响，也不会直接影响后面的请求应答情况
> 4. 服务器中没有保存客户端的状态，客户端必须每次带上自己的状态去请求服务器



## 12 Cookie

### 12.1 什么是 Cookie ?

- **Cookie**：指某些网站为了辨别用户身份、进行会话跟踪而储存在用户本地的数据（通常经过加密）。Cookie最早是网景公司的前雇员Lou Montulli在1993年3月发明。



### *12.2 在 C/S 中 Cookie 的交互流程 

- Cookie是由服务器端生成，发送给客户端浏览器，浏览器会将Cookie的key/value保存，下次请求同一网站时就发送该Cookie给服务器（前提是浏览器设置为启用cookie）。Cookie的key/value可以由服务器端自己定义。

![cookie](.\Flask框架__01_images\cookie.png)



#### Cookie 的应用

- 最典型的应用是 **判定注册用户是否已经登录网站**，用户可能会得到提示，是否在下一次进入此网站时保留用户信息以便简化登录手续，这些都是Cookie的功用。
- **网站的广告推送**，经常遇到访问某个网站时，会弹出小窗口，展示我们曾经在购物网站上看过的商品信息。
- **购物车**，用户可能会在一段时间内在同一家网站的不同页面中选择不同的商品，这些信息都会写入Cookie，以便在最后付款时提取信息。



- **提示**：
  
  - Cookie是存储在浏览器中的一段纯文本信息，建议不要存储敏感信息如密码，因为电脑上的浏览器可能被其它人使用
  - Cookie基于域名安全，**不同域名的Cookie是不能互相访问的**,  不同域名间不能相互获取给用户浏览器设置的cookie
    - 如访问gitee.com时向浏览器中写了Cookie信息，使用同一浏览器访问baidu.com时，baidu.com无法访问到gitee.com写的Cookie信息
    - 浏览器的**同源策略**,  只能访问自己域名范围内的 Cookie
- 当浏览器请求某网站时，会将本网站下所有Cookie信息提交给服务器，所以在request中可以读取Cookie信息
  
  

### 12.3 设置, 获取, 删除 Cookie 

```python
from flask import Flask, make_response

app = Flask(__name__)


@app.route('/login')
def login():

    # 假设账号密码验证通过

    # ——————————创建响应对象 传入将要返回字符串——————————
    response = make_response('login success !')

    # ——————————使用响应对象 设置cookie——————————
    response.set_cookie("user_id", "1")
    response.set_cookie("user_name", "John")

    # ——————————或直接向headers添加cookie——————————
    response.headers['Set-Cookie'] = "user_id2=2; user_name2=Jack"

    # ——————————set_cookie()方法可以同时指定最大保留时间——————————
    response.set_cookie("user_phone", "110", max_age=3600)

    return response


@app.route("/logout")
def logout():

    # ——————————创建响应对象——————————
    response = make_response("logout....")

    # ——————————删除 cookie——————————
    response.delete_cookie("user_id")
    response.delete_cookie("user_name")

    return response


if __name__ == '__main__':
    app.run(debug=True)
```





## 13 Session

### 13.1 什么是 Session ?

- 对于敏感、重要的信息，需要存储在服务器端，不能存储在浏览器中，如用户名、余额、等级、验证码等信息
- 在服务器端进行状态保持的方案就是`Session`
- **Session依赖于Cookie**




### 13.2 在 C/S 中 Session 的交互流程

![session](.\Flask框架__01_images\session.png)



session 和 session_id (sid) 都是服务器上生成的




### 13.3 设置, 获取, 删除 session

session: 请求上下文对象，用于处理http请求中的一些数据内容

```python
@app.route('/index1')
def index1():
    session['username'] = 'Jerry'
    return redirect(url_for('index'))
@app.route('/')
def index():
    return session.get('username')
```



> **需要设置    secret_key:  app.secret_key = 'bulabulabula' **
>
> secret_key的作用：
>
> [https://segmentfault.com/q/1010000007295395](https://segmentfault.com/q/1010000007295395)
>
> -  SECRET_KEY 的作用主要是提供一个值做各种 HASH, 用于加密用户信息
> -  考虑到安全性, SECRET_KEY **不建议**存储在程序中. 最好的方法是存储在系统环境变量中, 通过 `os.getenv(key, default=None)` 获得. 



**———————— Test_code ————————**

```python
from flask import Flask, session

app = Flask(__name__)


# todo ——————————使用session,必须配置 secret_key——————————
# 用于加密用户信息
# app.secret_key = "aaafagagadg"
app.config["SECRET_KEY"] = "aaafagagadg"


@app.route('/')
def index():
	# 用户访问网站页面, 需要获取 session 来判断用户是否已经登录
    # ——————————先 获取 session——————————
    user_id = session.get("user_id", "")
    user_name = session.get("user_name", "")
    
    # 判断是否获取到对应的session, 以判断用户是否已经登录
    pass
	# 如果没有登录, 转到登录界面
    pass
    
    # 测试: 返回用户名和id, 看session是否与设置的键值对一致
    return 'user_id: %s, user_name: %s' % (user_id, user_name)


@app.route("/login")
def login():
    
    # 假装登录校验成功

    # ——————————设置 session——————————
    session['user_id'] = "1"
    session['username'] = "john"
	
    # 登录成功, 且设置好session后, 返回相应页面, 如网站主页
    return "success"


@app.route('/logout')
def logout():
	
    # 假设用户点击了退出登录, 就无需状态保持
    
    # ——————————删除 session——————————
    session.pop("user_id", None)  # 没有了user_id键值对时就删除 None, 避免报错
    session.pop("user_name", None)
    
    # 之后用户如果直接访问页面就再跳转到登录界面
    
    return 'logout....'


if __name__ == '__main__':
    app.run(debug=True)
```



## 14 flask中的上下文

### 14.1 什么是上下文 ?

上下文：相当于一个容器，保存了 Flask 程序运行过程中的一些信息。

Flask中有两种上下文，请求上下文和应用上下文



### 14.2 请求上下文(request context)

思考：在视图函数中，如何取到当前请求的相关数据？比如：url，method，cookie等等

在 flask 中，可以直接在视图函数中使用 **request** 这个对象进行获取相关数据，而 **request** 就是请求上下文的对象，保存了当前本次请求的相关数据，请求上下文对象有：>>>>>>>>>  request、session  <<<<<<<<<<<

#### request

- 封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。
- 注意在视图函数中我们把 request 当作全局变量使用。事实上，request 不可能是全局变量。试想，在多线程服务器中，多个线程同时处理不同客户端发送的不同请求时，每个线程看到的 request 对象必然不同。Falsk 使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程。

#### session

- 用来记录请求会话中的信息，针对的是用户信息。举例：session['name'] = user.id，可以记录用户信息。还可以通过session.get('name')获取用户信息。



请求上下文对象request 和 session 只能在**视图函数内** (接收到请求后) 使用,  

[ 再理解 上下文 ]:

	- 相当于一个容器，保存了 Flask 程序运行过程中的一些信息 ;
	​	- 如果上文没有执行, 就不能读/取下文的信息;  
	​	- 先有上文 才有下文 ;

​	如: 路由URL需要是 request 的上文,  request是下文,  上文需要先执行, print(request.method) 这一句如果放在视图函数外面, 就会报错 --> 下文不能先执行;



### 14.3 应用上下文(application context)

#### 只有在应用运行起来之后,  才能使用 应用上下文对象

它的字面意思是 应用上下文，但它不是一直存在的，它只是request context 中的一个对 app 的代理(人)，所谓local proxy。它的作用主要是帮助 request 获取当前的应用，它是伴 request 而生，随 request 而灭的。

应用上下文对象有：>>>>>>>>>  current_app，g  <<<<<<<<<<<

#### current_app

应用程序上下文,用于存储应用程序中的变量，可以通过current_app.name打印当前app的名称，也可以在current_app中存储一些变量，例如：

- 应用的启动脚本是哪个文件，启动时指定了哪些参数
- 加载了哪些配置文件，导入了哪些配置
- 连了哪个数据库
- 有哪些public的工具类、常量
- 应用跑再哪个机器上，IP多少，内存多大

```python
current_app.name
current_app.test_value='value'
bool = current_app.config.get('DEBUG')
```

**———————— Test_code ————————**

```python
# 请求上下文对象
from flask import request
from flask import session


# 应用上下文对象
from flask import current_app
from flask import g


from flask import Flask
app = Flask(__name__)

# todo 这句打印代码放在这里（请求上下文的外面）会报错：
# RuntimeError: working outside of request context
# print(request.method)


@app.route('/')
def index():
    return 'Hello World'


# ——————————请求上下文对象： request——————————
@app.route('/demo1')
def demo1():

    return "浏览器的请求方式为----%s" % request.method


# ——————————应用上下文对象： current_app——————————
@app.route('/demo2')
def demo2():
    is_debug = current_app.config["DEBUG"]
    # is_debug = current_app.config.get("DEBUG")

    app_name = current_app.name

    return str(is_debug) + "---" + app_name


# todo 这句打印代码放在这里（上下文的外面）会报错：
# RuntimeError: working outside of application context
# print(current_app.name)
if __name__ == '__main__':
    app.run(debug=True)

    # 不会运行到下面一句
    print(current_app.name)
```



#### g 变量

g 作为 flask 程序全局的一个临时变量,  充当者中间媒介的作用, 我们可以通过它传递一些数据，g 保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别

g 作为处理请求时用作临时存储的对象, 每次请求都会重设这个变量

```python
g.name='abc'
```

> 注意：不同的请求，会有不同的全局变量



#### 两者区别：

- 请求上下文：保存了客户端和服务器交互的数据
- 应用上下文：flask 应用程序运行过程中，保存的一些配置信息，比如程序名、数据库连接、应用信息等

> 上下文中的对象只能在指定上下文中使用，超出范围不能使用 请求上下文和应用上下文原理实现：[https://segmentfault.com/a/1190000004223296](https://segmentfault.com/a/1190000004223296)





## 15 Flask-Script 扩展

### 15.1 Flask-Script 的作用 ?

<1>  配置Flask服务器能以命令行方式传入参数来启动

<2>  为当前应用程序添加脚本命令,  像 ipython 的 shell,  输入一行命令就有对应输出



通过使用Flask-Script扩展，我们可以在Flask服务器启动的时候，通过命令行的方式传入参数。而不仅仅通过app.run()方法中传参，比如我们可以通过：

```python
python hello.py runserver -host ip地址
```

以上命令告诉服务器在哪个网络接口监听来自客户端的连接。默认情况下，服务器只监听来自服务器所在的计算机发起的连接，即localhost连接。

我们可以通过 `python hello.py runserver --help` 来查看参数。



### 15.2 代码实现

- 在虚拟环境下 安装 Flask-Script 扩展

```python
# 可以打开 pycharm 中的终端来输入命令 (pycharm自动切换到了在当前程序所在的虚拟环境下)
pip install flask-script
```



- 在应用程序中 集成 Flask-Script

```python
from flask import Flask

# 从 flask_script 中导入 Manager
from flask_script import Manager

app = Flask(__name__)

# todo ———1——— 把 Manager 类和应用程序实例进行关联
# 创建 manager 对象
manager = Manager(app)


@app.route('/demo1')
def demo1():
    return "Tips: 我们可以在终端输入 python hello.py runserver --help 来查看参数。"


if __name__ == '__main__':
    # app.run(debug=True)
    # todo ———2——— 现在通过 manager对象 开启服务
    manager.run()  # 因为可以直接通过命令行输入参数, 就不用传参, 如在命令行开启debug增加 -d 选项
```



**—————————— 拓  展  —————————— **

在应用程序中 集成 Flask-Script 之后， 在 pycharm 中 默认不能直接右键点播放按钮运行， 但是可以通过以下配置实现：

![配置pycharm实现右键运行服务器等同于命令行运行服务器](.\Flask框架__01_images\配置pycharm实现右键运行服务器等同于命令行运行服务器.png)



Flask-Script 还可以为当前应用程序添加脚本命令，后续项目中会使用到.

##### 

##### 

######  

