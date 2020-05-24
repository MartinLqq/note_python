# 蓝图&单元测试

目标

- 能够使用代码实现蓝图对项目进行模块化
- 能够说出断言的作用
- 能够说出实现单元测试步骤
- 能够说出单元测试所执行方法的定义规则



# 1 Blueprint

### 模块化

随着flask程序越来越复杂,  我们需要对程序进行模块化的处理,  之前学习过python的模块化管理,  于是针对一个简单的flask程序进行模块化处理

举例:

```
我们有一个博客程序, 前台界面需要的路由为: 首页, 列表, 详情等页面;
如果博主需要编辑博客, 要进入后台进行处理: 后台主页, 编辑, 创建, 发布博客.
在一个py文件中写入太多路由, 将来维护代码会非常麻烦,  此时,  就需要考虑模块化的处理方式,  将admin相关的路由写到一个admin.py文件中
```



​	-------------->   以后需要把模块化蓝图放到单独的package包中,  因为蓝图有自己的静态文件, 模板等  <-----------------



- 在flask程序中, 使用传统的模块化是行不通的, 会产生 `模块循环导入` 的问题
- flask 内置了一个模块化处理的类, 即 `Blueprint`



### Blueprint概念

Blueprint 是一个存储操作方法的容器，这些操作在这个Blueprint 被注册到一个应用之后就可以被调用，Flask 可以通过Blueprint来组织URL以及处理请求。

Flask使用Blueprint让应用实现模块化，在Flask中，Blueprint具有如下属性：

- 一个应用可以具有多个Blueprint
- 可以将一个Blueprint注册到任何一个未使用的URL下比如 “/”、“/sample”或者子域名
- 在一个应用中，一个模块可以注册多次
- Blueprint可以单独具有自己的模板、静态文件或者其它的通用操作方法，它并不是必须要实现应用的视图和函数的
- 在一个应用初始化时，就应该要注册需要使用的Blueprint

但是一个Blueprint并不是一个完整的应用，它不能独立于应用运行，而必须要注册到某一个应用中。



### 使用蓝图

蓝图/Blueprint对象用起来和一个应用/Flask对象差不多，最大的区别在于一个 蓝图对象没有办法独立运行，必须将它注册到一个应用对象上才能生效

使用蓝图可以分为 `三个步骤`:

- 1,  创建蓝图对象

```python
admin=Blueprint('admin',__name__)
```

- 2,  注册路由

```python
@admin.route('/')
def admin_home():
    return 'admin_home'
```

- 3,  注册蓝图对象

```python
app.register_blueprint(admin,url_prefix='/admin')
```

当这个应用启动后,  通过/admin/可以访问到蓝图中定义的视图函数



### 运行机制

- 蓝图保存了一组将来可以在应用对象上执行的操作，注册路由就是一种操作
- 当在应用对象上调用 route 装饰器注册路由时,  这个操作将修改对象的url_map路由表
- 然而，蓝图对象根本没有路由表，当我们在蓝图对象上调用route装饰器注册路由时, 它只是在内部的一个延迟操作记录列表defered_functions中添加了一个项
- 当执行应用对象的 register_blueprint() 方法时，应用对象将从蓝图对象的 defered_functions 列表中取出每一项，并以自身作为参数执行该匿名函数，即调用应用对象的 add_url_rule() 方法，这将真正的修改应用对象的路由表.


代码示例

- order.py

```python
# 0. 导入蓝图类
from flask import Blueprint

# 1. 初始化蓝图对象
order_blu = Blueprint('order', __name__)


# 订单列表
# 2. 使用蓝图去注册路由url
@order_blu.route('/order/list')
def order_list():
    return 'order_list'
```



- main.py

```python
from flask import Flask
from order import order_blu
from cart import cart_blu

app = Flask(__name__)

# 3. 把蓝图注册到app上
app.register_blueprint(order_blu)
app.register_blueprint(cart_blu)


@app.route('/')
def index():
    return 'index'


"""以下代码抽取到order.py中
# 订单列表
@app.route('/order/list')
def order_list():
    return 'order_list'

"""


@app.route('/user/info')
def user_info():
    return "user_info"


"""以下代码拷贝到cart模块里面
@app.route('/cart/list')
def cart_list():
    return "cart_list"
"""


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```



### 蓝图的url前缀

- 在应用对象上注册一个蓝图时，可以指定一个url_prefix关键字参数（这个参数默认是/）
- 在应用最终的路由表 url_map中，在蓝图上注册的路由URL自动被加上了这个前缀，这个可以保证在多个蓝图中使用相同的URL规则而不会最终引起冲突，只要在注册蓝图时将不同的蓝图挂接到不同的自路径即可
- url_for()

```
url_for('admin.index') # /admin/
```

访问url为  `http://127.0.0.1:5000/admin/`  ,  而不是 `http://127.0.0.1:5000`

### 注册静态路由

和应用对象不同，蓝图对象创建时不会默认注册静态目录的路由。需要我们在 创建时指定 static_folder 参数。

下面的示例将蓝图所在目录下的static_admin目录设置为静态目录

```python
admin = Blueprint("admin",__name__,static_folder='static_admin')
app.register_blueprint(admin,url_prefix='/admin')
```

现在就可以使用/admin/static_admin/ 访问static_admin目录下的静态文件了 定制静态目录URL规则 ：可以在创建蓝图对象时使用 static_url_path 来改变静态目录的路由。下面的示例将为 static_admin 文件夹的路由设置为 /lib

```python
admin = Blueprint("admin",__name__,static_folder='static_admin',static_url_path='/lib')
app.register_blueprint(admin,url_prefix='/admin')
```



### 设置模版目录

蓝图对象默认的模板目录为系统的模版目录，可以在创建蓝图对象时使用 template_folder 关键字参数设置模板目录

```
admin = Blueprint('admin',__name__,template_folder='my_templates')
```

> 注:如果在 templates 中存在和 my_templates 同名文件,则系统会优先使用 templates 中的文件 参考链接：[https://stackoverflow.com/questions/7974771/flask-blueprint-template-folder](https://stackoverflow.com/questions/7974771/flask-blueprint-template-folder)



# 2 单元测试

### 为什么要测试？

Web程序开发过程一般包括以下几个阶段：[需求分析，设计阶段，实现阶段，测试阶段]。

测试阶段通过人工或自动来运行测试某个系统的功能,  目的是检验其是否满足需求，并得出特定的结果，以达到弄清楚预期结果和实际结果之间的差别的最终目的。

#### 测试的分类

测试从软件开发过程可以分为：

- 单元测试
  - 对单独的代码块 (例如函数) 分别进行测试,  以保证它们的正确性
- 集成测试
  - 对大量的程序单元的协同工作情况做测试
- 系统测试
  - 同时对整个系统的正确性进行检查,  而不是针对独立的片段

在众多的测试中，与程序开发人员最密切的就是 `单元测试`，因为单元测试是由开发人员进行的，而其他测试都由专业的测试人员来完成。所以我们主要学习单元测试。



测试模型:       瀑布 双V  敏捷 



### 什么是单元测试？

当代码通过了编译，只说明语法正确，功能能否实现则不能保证。 因此，当我们的某些功能代码完成后，为了检验其是否满足程序的需求,  可以通过编写测试代码，模拟程序运行的过程，检验功能代码是否符合预期。

单元测试就是开发者编写一小段代码，检验目标代码的功能是否符合预期。通常情况下，单元测试主要面向一些功能单一的模块进行。

举个例子：一部手机有许多零部件组成，在正式组装一部手机前，手机内部的各个零部件，CPU、内存、电池、摄像头等，都要进行测试，这就是单元测试。

在Web开发过程中，单元测试实际上就是一些   `“断言”（assert）`  代码。

断言就是判断一个函数或对象的一个方法所产生的结果是否符合你期望的那个结果。 python中 `assert` 断言是声明布尔值为真的判定，如果表达式为假会发生异常。单元测试中，一般使用 assert 来断言结果。

#### 断言方法的使用

断言语句类似于：

```python
if not expression:    
    raise AssertionError
 AssertionError
```

**常用的断言方法**

```python
assertEqual     如果两个值相等，则pass
assertNotEqual  如果两个值不相等，则pass
assertTrue      判断bool值为True，则pass
assertFalse     判断bool值为False，则pass
assertIsNone    不存在，则pass
assertIsNotNone 存在，则pass
```

### 如何测试？

简单的测试用例：1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233，377，610，987，1597，2584，4181，6765，

```python
def fibo(x):
    if x == 0:
        resp = 0
    elif x == 1:
        resp = 1
    else:
        return fibo(x-1) + fibo(x-2)
    return resp
assert fibo(5) == 5
```



### 单元测试的基本写法

(1) **首先**，定义一个类，继承自 `unittest.TestCase`

```python
import unittest
class TestClass(unitest.TestCase):
    pass
```

(2) **其次**，在测试类中，定义两个测试方法

```python
import unittest
class TestClass(unittest.TestCase):

    # 该方法会首先执行，方法名为固定写法
    def setUp(self):
        pass

    # 该方法会在测试代码执行完后执行，方法名为固定写法
    def tearDown(self):
        pass
```

(3) **最后**，在测试类中，编写测试代码

```python
import unittest
class TestClass(unittest.TestCase):

    # 该方法会首先执行，相当于做测试前的准备工作
    def setUp(self):
        pass

    # 该方法会在测试代码执行完后执行，相当于做测试后的扫尾工作
    def tearDown(self):
        pass
    
    # 测试代码
    def test_app_exists(self):
        pass
```



### 登录测试

- 被测试的代码逻辑

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # 判断参数是否为空
    if not all([username, password]):
        result = {
            "errcode": -2,
            "errmsg": "params error"
        }
        return jsonify(result)

    # a = 1 / 0
    # 如果账号密码正确
    # 判断账号密码是否正确
    if username == 'itheima' and password == 'python':
        result = {
            "errcode": 0,
            "errmsg": "success"
        }
        return jsonify(result)
    else:
        result = {
            "errcode": -1,
            "errmsg": "wrong username or password"
        }
        return jsonify(result)
```



- 单元测试代码

```python
import json
import unittest
from demo1_login import app

class LoginTest(unittest.TestCase):
    """为登录逻辑编写测试案例"""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_username_password(self):
        """测试用户名与密码为空的情况[当参数不全的话，返回errcode=-2]"""
        response = app.test_client().post('/login', data={})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -2, '状态码返回错误')

        # TODO 测试用户名为空的情况

        # TODO 测试密码为空的情况

    def test_error_username_password(self):
        """测试用户名和密码错误的情况[当登录名和密码错误的时候，返回 errcode = -1]"""
        response = app.test_client().post('/login', data={"username": "aaaaa", "password": "12343"})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -1, '状态码返回错误')

        # TODO 测试用户名错误的情况

        # TODO 测试密码错误的情况

if __name__ == '__main__':
    unittest.main()
```



### 数据库测试

```python
#coding=utf-8
import unittest
from author_book import *

#自定义测试类，setUp方法和tearDown方法会分别在测试前后执行。以test_开头的函数就是具体的测试代码。
class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/test0'
        self.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #测试代码
    def test_append_data(self):
        au = Author(name='itcast')
        bk = Book(info='python')
        db.session.add_all([au,bk])
        db.session.commit()
        author = Author.query.filter_by(name='itcast').first()
        book = Book.query.filter_by(info='python').first()
        #断言数据存在
        self.assertIsNotNone(author)
        self.assertIsNotNone(book)
```