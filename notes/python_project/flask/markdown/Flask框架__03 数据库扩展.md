# Flask-SQLAlchemy 数据库扩展

# ORM

- **ORM** 全拼 `Object-Relation Mapping`.
- 中文意为 **对象-关系映射**.
- 主要实现模型对象到关系数据库数据的映射.
  - 比如：把数据库表中每条记录映射为一个模型对象

## ORM图解

![ORM](.\Flask框架__03_images\ORM.png)



## 优点 

- 只需要面向对象编程, 不需要面向数据库编写代码.
  - 对数据库的操作都转化成对类属性和方法的操作.
  - 不用编写各种数据库的`sql语句`.
- 实现了数据模型与数据库的解耦, 屏蔽了不同数据库操作上的差异.
  - 不在关注用的是`mysql`、`oracle`...等.
  - 通过简单的配置就可以轻松更换数据库, 而不需要修改代码.

## 缺点 

- 相比较直接使用SQL语句操作数据库,有性能损失.
- 根据对象的操作转换成SQL语句,根据查询的结果转化成对象, 在映射过程中有性能损失.



# 1 flask-sqlalchemy 安装及设置

- SQLALchemy 实际上是对数据库的抽象，让开发者不用直接和 SQL 语句打交道，而是通过 Python 对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升
- SQLAlchemy是一个关系型数据库框架，它提供了高层的 ORM 和底层的原生数据库的操作。flask-sqlalchemy 是一个简化了 SQLAlchemy 操作的flask扩展。
- 文档地址：[http://docs.jinkan.org/docs/flask-sqlalchemy](http://docs.jinkan.org/docs/flask-sqlalchemy)



## Ubuntu上安装

- 1--- 安装 flask-sqlalchemy

```
pip install flask-sqlalchemy
```

- 2--- 如果连接的是 mysql 数据库，需要安装 mysqldb

```
pip install flask-mysqldb
```



## Windows上安装 flask-mysqldb 注意

- 在 Windows上安装 flask-mysqldb,   需要先安装 mysqlclient,  否则安装失败:
  - 下载对应python解释器版本的 mysqlclient:   `https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient`
    - 如python3.6 下载:   mysqlclient‑1.3.13‑cp36‑cp36m‑win_amd64.whl
  - 安装 mysqlclient:  pip    install   mysqlclient‑1.3.13‑cp36‑cp36m‑win_amd64.whl
  - 安装 flask-mysqldb:  点击进入pycharm的pip搜索Flask-MySQLdb,  点击安装



## 数据库连接配置

- 在 Flask-SQLAlchemy 中，数据库使用URL指定，而且程序使用的数据库必须保存到Flask配置对象的 **SQLALCHEMY_DATABASE_URI**  键中

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'
```

- 其他设置：

```
# 动态追踪修改设置，如未设置只会提示警告, 不会报错
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 查询时会显示原始SQL语句, 有助于分析遗异常
app.config['SQLALCHEMY_ECHO'] = True
```

- 配置完成需要去 MySQL 中创建项目所使用的数据库

```
$ mysql -uroot -pmysql
$ create database test charset utf8;
```



- 其他配置

| 名字                        | 备注                                       |
| ------------------------- | ---------------------------------------- |
| SQLALCHEMY_DATABASE_URI   | 用于连接的数据库 URI 。例如:     sqlite:////tmp/test.db,   mysql://username:password@server/db |
| SQLALCHEMY_BINDS          | 一个映射 binds 到连接 URI 的字典。更多 binds 的信息见[*用 Binds 操作多个数据库*](http://docs.jinkan.org/docs/flask-sqlalchemy/binds.html#binds)。 |
| SQLALCHEMY_ECHO           | 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。(打印sql语句) |
| SQLALCHEMY_RECORD_QUERIES | 可以用于显式地禁用或启用查询记录。查询记录 在调试或测试模式自动启用。更多信息见get_debug_queries()。 |
| SQLALCHEMY_NATIVE_UNICODE | 可以用于显式禁用原生 unicode 支持。当使用 不合适的指定无编码的数据库默认值时，这对于 一些数据库适配器是必须的（比如 Ubuntu 上 某些版本的 PostgreSQL ）。 |
| SQLALCHEMY_POOL_SIZE      | 数据库连接池的大小。默认是引擎默认值（通常 是 5 ）              |
| SQLALCHEMY_POOL_TIMEOUT   | 设定连接池的连接超时时间。默认是 10 。                    |
| SQLALCHEMY_POOL_RECYCLE   | 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定 这个值为 2 小时。 |



**连接其他数据库**

完整连接 URI 列表请跳转到 SQLAlchemy 文档 ([Supported Databases](http://www.sqlalchemy.org/docs/core/engines.html)) 。这里给出一些 常见的连接字符串。

- Postgres:

```
postgresql://scott:tiger@localhost/mydatabase
```

- MySQL:

```
mysql://scott:tiger@localhost/mydatabase
```

- Oracle:

```
- oracle://scott:tiger@127.0.0.1:1521/sidname
```

- SQLite （注意开头的四个斜线）:

```
sqlite:////absolute/path/to/foo.db
```



## 常用 SQLAlchemy 字段类型

| 类型名          | python中类型         | 说明                            |
| ------------ | ----------------- | ----------------------------- |
| Integer      | int               | 普通整数，一般是32位                   |
| SmallInteger | int               | 取值范围小的整数，一般是16位               |
| BigInteger   | int或long          | 不限制精度的整数                      |
| Float        | float             | 浮点数                           |
| Numeric      | decimal.Decimal   | 普通整数，一般是32位                   |
| String       | str               | 变长字符串                         |
| Text         | str               | 变长字符串，对较长或不限长度的字符串做了优化        |
| Unicode      | unicode           | 变长Unicode字符串                  |
| UnicodeText  | unicode           | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool              | 布尔值                           |
| Date         | datetime.date     | 时间                            |
| Time         | datetime.datetime | 日期和时间                         |
| LargeBinary  | str               | 二进制文件                         |



## 常用 SQLAlchemy 列选项

| 选项名         | 说明                            |
| ----------- | ----------------------------- |
| primary_key | 如果为True，代表表的主键                |
| unique      | 如果为True，代表这列不允许出现重复的值         |
| index       | 如果为True，为这列创建索引，提高查询效率        |
| nullable    | 如果为True，允许有空值，如果为False，不允许有空值 |
| default     | 为这列定义默认值                      |



## 常用 SQLAlchemy 关系选项

| 选项名            | 说明                                  |
| -------------- | ----------------------------------- |
| backref        | 在关系的另一模型中添加 `反向引用`                  |
| primary join   | 明确指定两个模型之间使用的联结条件                   |
| uselist        | 如果为False，不使用列表，而使用标量值               |
| order_by       | 指定关系中记录的排序方式                        |
| secondary      | 指定 `多对多` 关系中 `关系表` 的名字              |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件 |



####    

# 2 数据库基本操作

- 在Flask-SQLAlchemy中，插入、修改、删除操作，均由数据库会话 **`session`** 管理。
  - 会话用 db.session 表示。在准备把数据写入数据库前，要先将数据添加到会话中然后调用 commit() 方法提交会话。
- 在 Flask-SQLAlchemy 中，查询操作是通过 **`query`** 对象操作数据。
  - 最基本的查询是返回表中所有数据，可以通过过滤器进行更精确的数据库查询。



## 定义模型类

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # 创建一个应用程序

# ———————————— 配置数据库 ————————————
# 添加MySQL数据库 到Flask配置对象中
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/my_flask_test'

# 是否追踪数据库的修改，如未设置会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 设置查询时 是否在控制台输出原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# ———————— 初始化 SQLAlchemy对象, 传入应用app ————————
db = SQLAlchemy(app)


@app.route('/')
def index():
    return '----index----'


# ———————— 定义一个模型, 继承自db.Model类 ————————
class Role(db.Model):

    # 指定该模型对应数据库中的表名
    # 如果不指定, 默认是 模型类名的小写 ---> role
    __tablename__ = "roles"

    # 定义字段(列---Column)
    id = db.Column(db.Integer, primary_key=True)  # 整数, 主键
    name = db.Column(db.String(64), unique=True)  # 字符串, 唯一

    # 定义__repr__方法, 用于测试查询时 显示当前对象的描述, 否则默认显示为对象
    def __repr__(self):
        return "Role %d %s" % (self.id, self.name)  # 自定义显示字符串


if __name__ == '__main__':

    role = Role(name="laoliu")
    db.session.add(role)
    db.session.commit()

    app.run(debug=True)


# todo —————— 在Pycharm终端中 运行ipython3， 导入当前文件， 运行以下代码： ——————

# 1 创建表
# db.drop_all()
# db.create_all()

# 2 创建一些用户
# admin = Role(name="laowang")
# guest = Role(name="老刘")

# 3 添加用户到数据库中
# db.session.add(admin)
# db.session.add(guest)       # db.session.add_all([admin, guest])

# 4 提交事务
# db.session.commit()
```



## 模型之间的关联

### 一对多 关联

如:  角色和用户的关系是一对多的关系，一个角色可以有多个用户，一个用户只能属于一个角色。

```python
class Role(db.Model):
    __tablename__ = 'roles'
    ...
    #关键代码
    us = db.relationship('User', backref='role', lazy='dynamic')
    ...

class User(db.Model):
    __tablename__ = 'users'
    ...
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```



`db.realtionship` 描述了Role和User的关系,  它可以有三个参数 : 

<1> 第一个参数为对应参照的类 `"User"`,  必须指定
<2> 第二个参数  `backref` 为第一个参数中的User申明新属性的方法, 使用方法:  如 User.query.first().role

---

​	请先看第三个参数的说明再看这里:
​		~  第二个参数 backref 中可以反向给 User 指定 lazy 的值:   
​		~ 直接将  `backref='role'`   改为 `db.backref=backref('role', lazy='dynamic')`



<3> 第三个参数  `lazy`  决定了什么时候SQLALchemy从数据库中加载数据: 

- 如果设置为子查询方式(subquery)，则会在加载完Role对象后，就立即加载与其关联的对象，这样会让总查询数量减少，但如果返回的条目数量很多，就会比较慢
  - 设置为 `subquery` 的话，role.users 返回所有数据 **列表**
- 另外, 也可以设置为动态加载(dynamic)，role.users 不会返回数据列表, 而是返回一个"查询对象".
  - 设置为 `dynamic` 的话，role.users 返回查询 **对象**，并没有做真正的查询，可以利用查询对象做其他逻辑，比如：先排序再返回结果
  - dynamic 可以优化性能



**代码验证**:   一个role对多个user

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/my_flask_test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


# 定义 Role 模型
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    # ———————— 关键代码 ————————
    # 给Role添加users属性, 以便可以用Role.users 访问User的数据
    # 在users属性中设置指向: "User",  反指向: bachref="role" 以便可以用User.role 访问Role的数据
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "Role %d %s" % (self.id, self.name)


# 定义 User 模型 (一个Role对象对应多个User对象)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    # ———————— 关键代码 ————————
    # 在users表中再定义一个 role_id 字段, 设置为外键 -- 记录一的一方的主键id, 即Role.id
    # 为了能够直接查询出一的一方的数据
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    def __repr__(self):
        return "User %s" % self.name


@app.route('/')
def index():
    return '----index----'


if __name__ == '__main__':

    # ———————————— 建表 加数据 ——————————————
    db.drop_all()
    db.create_all()

    ro1 = Role(name="管理员")
    ro2 = Role(name="用户")
    db.session.add_all([ro1, ro2])
    db.session.commit()

    user1 = User(name="布鲁斯", role_id=ro1.id)
    user2 = User(name="阿凡达", role_id=ro2.id)
    user3 = User(name="赵无极", role_id=ro2.id)
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    app.run(debug=True)


# todo ———————— 在终端ipython中导入本文件, 执行以下代码 ————————

# Role对User  ---->  一对多
# Role.query.all()      # [Role 2 用户, Role 1 管理员]

# User.query.all()      # [User 布鲁斯, User 阿凡达, User 赵无极]
# u = User.query.get(1)
# u.role                # Role 1 管理员
# u.role_id             # 1
# u.role.name           # '管理员'
```



### 多对多 关联

**实际开发场景**

- 学生网上选课(学生和课程)
- 老师与其授课的班级(老师和班级)
- 用户与其收藏的新闻(用户和新闻)
- 等等...



**场景示例**

< 需求分析 >

- 多个学生分别可以选修多个课程
- 需求：
  1. 查询某个学生选修了哪些课程
  2. 查询某个课程都有哪些学生选择

< 思路分析 >

- 可以通过分析得出
  - 用一张表来保存所有的学生数据
  - 用一张表来保存所有的课程数据
  - 用一张表来保存 student_id 和 course_id



(1) 学生表(Student)

| 主键(id) | 学生名(name) |
| ------ | --------- |
| 1      | 张三        |
| 2      | 李四        |
| 3      | 王五        |



(2) 选修课表(Course)

| 主键(id) | 课程名(name) |
| ------ | --------- |
| 1      | 物理        |
| 2      | 化学        |
| 3      | 生物        |



(3) 数据关联关系表(Student_Course)

| 主键(student.id) | 主键(course.id) |
| -------------- | ------------- |
| 1              | 2             |
| 1              | 3             |
| 2              | 2             |
| 3              | 1             |
| 3              | 2             |
| 3              | 3             |



**关键代码**

```python
registrations = db.Table('registrations',  
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),  
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))  
)  

class Course(db.Model):
    ...
    
class Student(db.Model):
    ...
    courses = db.relationship('Course',secondary=registrations,  
                                    backref='students',  
                                    lazy='dynamic')
```



**代码验证**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/my_flask_test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# todo 不使用模型, 创建一个单独的表 tb_Student_Course
# ————————————————————————— start ———————————————————————————
tb_Student_Course = db.Table(
    # 第一个参数: 指定表名
    "student_course",
    # 添加外键. student 就是 Student模型默认的表名
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
)
# —————————————————————————— end ——————————————————————————


#  使用模型表示 student 表
class Student(db.Model):
    """学生表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 添加courses属性, 指向Course, 以便可以通过student.courses获取课程
    # 添加反向引用backref, 给Course添加students属性, 指向Student
    # 使用secondary关联中间表tb_Student_Course
    courses = db.relationship("Course", backref="students", secondary=tb_Student_Course)

    def __repr__(self):
        return "Student %d %s" % (self.id, self.name)


#  使用模型表示 course 表
class Course(db.Model):
    """课程表"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "Course %d %s" % (self.id, self.name)


@app.route('/')
def index():
    return '----index----'


if __name__ == '__main__':

    db.drop_all()
    db.create_all()

    # 添加测试数据

    stu1 = Student(name='张三')
    stu2 = Student(name='李四')
    stu3 = Student(name='王五')

    cou1 = Course(name='物理')
    cou2 = Course(name='化学')
    cou3 = Course(name='生物')
	
    # ——————————————————————————— 在学生表中添加 多个课程 ———————————————————————————————
    # ——————————————————————————— 注意添加的方式 ———————————————————————————————
    stu1.courses = [cou2, cou3]
    stu2.courses = [cou2]
    stu3.courses = [cou1, cou2, cou3]  # 用列表方式给一个学生添加多个课程

    db.session.add_all([stu1, stu2, stu2])  # 使用会话管理, 给学生表添加多个学生
    db.session.add_all([cou1, cou2, cou3])

    db.session.commit()

    app.run(debug=True)


# todo —————————— 控制台 查询 ——————————
# 查询张三的课程
# Student.query.filter(Student.name=="张三").course
# ————> [Course 1 化学, Course 3 生物]

# 查询课程id为1的所有学生
# Course.query.get(1).students
# ————> [Student 1 张三, Student 3 王五, Student 2 李四]

# 查询 生物 对应的学生姓名
# Course.query.filter(Course.name=="生物").first().students
# ————> [Student 1 张三, Student 3 王五]
```





## 表的 创建与删除

创建表	db.create_all()
删除表	db.drop_all()



## 数据的 增

插入一条数据

```python
ro1 = Role(name='admin')
db.session.add(ro1)
db.session.commit()

# 再次插入一条数据
ro2 = Role(name='user')
db.session.add(ro2)
db.session.commit()
```



一次插入多条数据

```python
us1 = User(name='wang',email='wang@163.com',password='123456',role_id=ro1.id)
us2 = User(name='zhang',email='zhang@189.com',password='201512',role_id=ro2.id)
us3 = User(name='chen',email='chen@126.com',password='987654',role_id=ro2.id)
db.session.add_all([us1,us2,us3])
db.session.commit()
```





## 数据的 查询



### 模型类名.query.过滤器名(条件xx).执行器名(xx)



### 常用 SQLAlchemy 查询过滤器

| 过滤器      | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| filter()    | 模糊查询,  把过滤器添加到原查询上，返回一个新查询            |
| filter_by() | 精确查询,  把等值过滤器( 是 "=" 不是 "==")添加到原查询上，返回一个新查询 |
| limit()     | 使用指定的值限定原查询返回的结果                             |
| offset()    | 偏移原查询返回的结果，返回一个新查询                         |
| order_by()  | 根据指定条件对原查询结果进行排序，返回一个新查询             |
| group_by()  | 根据指定条件对原查询结果进行分组，返回一个新查询             |
|             |                                                              |
| endswith()  | 以什么结尾                                                   |
|             |                                                              |

#### 与过滤器一起使用的模块

- 逻辑与，需要导入 `and_` ，返回and_()条件满足的所有数据

```
from sqlalchemy import and_
User.query.filter(and_(User.name!='wang',User.email.endswith('163.com'))).all()
```

- 逻辑或，需要导入 `or_`

```
from sqlalchemy import or_
User.query.filter(or_(User.name!='wang',User.email.endswith('163.com'))).all()
```

- 逻辑非，返回名字不等于wang的所有数据

```
User.query.filter(User.name!='wang').all()
```

- `not_` 相当于取反

```
from sqlalchemy import not_
User.query.filter(not_(User.name=='chen')).all()
```



### 常用 SQLAlchemy 查询执行器

| 方法             | 说明                                 |
| -------------- | ---------------------------------- |
| all()          | 以列表形式返回查询到的所有 对象                   |
| first()        | 返回查询的第一个对象，如果未查到，返回None            |
| first_or_404() | 返回查询的第一个对象，如果未查到，返回404             |
| get()          | 参数为主键，如果主键不存在返回None                |
| get_or_404()   | 返回指定主键对应的行，如不存在，返回404              |
| count()        | 返回查询结果的数量                          |
| paginate()     | 分页查询.  返回一个Paginate对象，它包含指定范围内的结果. |

        paginate = User.query.filter(User.name == name).paginate()
        paginate.items  # 返回当前页数据
        paginate.pages  # 返回总页码
        paginate.page   # 返回当前页的页码


### 查询案例

```PYTHON
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_, and_, or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mysql@127.0.0.1:3306/my_flask_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return '----index----'


# 定义表模型 Role
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # todo 添加users属性, 设置指向与反指向
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return "Role %d %s" % (self.id, self.name)


# 定义表模型 User
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)

    # todo 在users表中再定义一个 role_id 字段, 设置为外键 -- 记录一的一方的主键id---Role.id
    # todo 为了能够直接查询出一的一方的数据
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))    # 外键引用 Role.id

    def __repr__(self):
        return "User %d %s" % (self.id, self.name)


if __name__ == '__main__':

    # todo ~~~~~~~~~~~ 添加测试数据 ~~~~~~~~~~~~

    # 删表, 建表
    db.drop_all()
    db.create_all()

    # 向 Role模型的role表 插入2条数据
    ro1 = Role(name='admin')
    ro2 = Role(name='user')
    db.session.add_all([ro1, ro2])
    db.session.commit()

    # 向 User模型的users表插入多条数据
    us1 = User(name='wang', email='wang@163.com', password='123456', role_id=ro1.id)
    us2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=ro2.id)
    us3 = User(name='chen', email='chen@126.com', password='987654', role_id=ro2.id)
    us4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=ro1.id)
    us5 = User(name='tang', email='tang@qq.com', password='158104', role_id=ro2.id)
    us6 = User(name='wu', email='wu@gmail.com', password='5623514', role_id=ro2.id)
    us7 = User(name='qian', email='qian@gmail.com', password='1543567', role_id=ro1.id)
    us8 = User(name='liu', email='liu@itheima.com', password='867322', role_id=ro1.id)
    us9 = User(name='li', email='li@163.com', password='4526342', role_id=ro2.id)
    us10 = User(name='sun', email='sun@163.com', password='235523', role_id=ro2.id)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    db.session.commit()

    app.run(debug=True)

    
    # todo ~~~~~~~~~~~ 在pycharm终端: 查询数据 ~~~~~~~~~~~~
    
    # (1) 简单查询
    # Role.query.all()  Role.query.get(1)  Role.query.get(2).users
    # User.query.all()  User.query.get(1)  User.query.get(1).role

    # (2) 过滤查询
    # 查询所有用户数据
        User.query.all()
    # 查询有多少个用户
        User.query.count()
    # 查询第1个用户
        User.query.get(1)
    # 查询id为4的用户[3种方式]
        User.query.get(4)
        User.query.filter_by(id=4).first()
        User.query.filter(User.id == 4).all()
    # 查询名字结尾字符为g的所有数据 [开始statswith / 包含contains]
        User.query.filter(User.name.endswith("g")).all()
    # 查询名字不等于wang的所有数据[2种方式]
        User.query.filter(User.name != "wang").all()
        User.query.filter(not_(User.name == "wang")).all()
    # 查询名字和邮箱都以li开头的所有数据[2种方式]
        User.query.filter(User.name.startswith('li'), User.name.startswith('li')).all()
        User.query.filter(and_(User.name.startswith('li'), User.name.startswith('li'))).all()
    # 查询password是`123456`或者`email`以`qq.com`结尾的所有数据
        User.query.filter(or_(User.password == "123456", User.email.endswith('qq.com'))).all()
    # 查询id为[1, 3, 5, 7, 9]的用户列表
        User.query.filter(User.id.in_([1, 3, 5, 7, 9])).all()
    # 查询name为liu的角色数据
        User.query.filter(User.name=="liu").first().role
        User.query.filter_by(name="liu").first().role
    # 查询所有用户数据，并以邮箱排序
        User.query.order_by(User.email.desc()).all()
    # 分页查询, 每页3个, 查询第2页的数据
        paginate = User.query.paginate(2, 3)  # 第1个参数代表查询第几页，第2个参数代表每页几个
        paginate.items  # 返回当前页数据
        paginate.pages  # 返回总页码
        paginate.page   # 返回当前页的页码
```



## 查询数据后删除

```PYTHON
user = User.query.first()
# 删除行
db.session.delete(user)
db.session.commit()
User.query.all()
```



## 更新数据

```PYTHON
user = User.query.first()
# 更新数据
user.name = 'dong'
db.session.commit()
User.query.first()
```



# 3 Pycharm断点调试



![pycharm调试01](.\Flask框架__03_images\pycharm调试01.png)



![Evaluate](.\Flask框架__03_images\Evaluate.png)



![给断点添加条件](.\Flask框架__03_images\给断点添加条件.png)





# 4 常见关系模板代码

## 一对多

- 示例场景：
  - 用户与其发布的帖子(用户表与帖子表)
  - 角色与所属于该角色的用户(角色表与多用户表)
- 示例代码

```python
class Role(db.Model):
    """角色表----一的一方"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    """用户表----多的一方"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
```



## 多对多

- 示例场景
  - 讲师与其上课的班级 (讲师表与班级表)
  - 用户与其收藏的新闻 (用户表与新闻表)
  - 学生与其选修的课程 (学生表与选修课程表)
- 示例代码

```python
tb_student_course = db.Table('tb_student_course',
                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                             )

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    courses = db.relationship('Course', secondary=tb_student_course,
                              backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
```



## 自关联一对多

- 示例场景
  - 评论与该评论的子评论(评论表)
  - 参考网易新闻
- 示例代码

```python
class Comment(db.Model):
    """评论"""
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    # 评论内容
    content = db.Column(db.Text, nullable=False)
    # 父评论id
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    # 父评论(也是评论模型)
    parent = db.relationship("Comment", remote_side=[id],
                             backref=db.backref('childs', lazy='dynamic'))

# 测试代码
if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    com1 = Comment(content='我是主评论1')
    com2 = Comment(content='我是主评论2')
    com11 = Comment(content='我是回复主评论1的子评论1')
    com11.parent = com1
    com12 = Comment(content='我是回复主评论1的子评论2')
    com12.parent = com1

    db.session.add_all([com1, com2, com11, com12])
    db.session.commit()
    app.run(debug=True)
```



## 自关联多对多

- 示例场景
  - 用户关注其他用户(用户表，中间表)
- 示例代码

```python
tb_user_follows = db.Table(
    "tb_user_follows",
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)  # 被关注人的id
)

class User(db.Model):
    """用户表"""
    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(32), unique=True, nullable=False)

    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    followers = db.relationship('User',
                                secondary=tb_user_follows,
                                primaryjoin=id == tb_user_follows.c.followed_id,
                                secondaryjoin=id == tb_user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')
```





# 5 数据库迁移

- 在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据。
- 更好的解决办法是 **使用数据库迁移框架**，它可以追踪数据库模式的变化，然后把变动应用到数据库中。
- 在Flask中可以使用 `Flask-Migrate`  扩展，来实现数据迁移。并且集成到Flask-Script中，所有操作通过命令就能完成。
- 为了导出数据库迁移命令，Flask-Migrate提供了一个MigrateCommand类，可以附加到flask-script的manager对象上。

## Flask-Migrate安装

首先要在虚拟环境中安装Flask-Migrate。

```python
pip install flask-migrate
```



## 实际操作顺序

- 1.python 文件名 db init
- 2.python 文件名 db migrate -m "版本名(注释)"
- 3.python 文件名 db upgrade 然后观察表结构
- 4.根据需求修改模型
- 5.python 文件名 db migrate -m "新版本名(注释)"
- 6.python 文件名 db upgrade 然后观察表结构
- 7.若返回版本,  则利用 python 文件 db history查看版本号
- 8.python 文件名 db downgrade(upgrade) 版本号




## 数据库迁移的 配置代码

> 注:  写入相应的配置代码,   就可以在命令行进行数据库的迁移

```python
#coding=utf-8
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = Flask(__name__)
manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/Flask_test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app,db) 

# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db',MigrateCommand)

# 定义模型Role
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    # repr()方法显示一个可读字符串，
    def __repr__(self):
        return 'Role:'.format(self.name)

# 定义用户
class User(db.Model):
    __talbe__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 设置外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:'.format(self.username)


if __name__ == '__main__':
    manager.run()
```



## 迁移命令总结

1 迁移初始化  (生成迁移所需要的文件夹--迁移仓库 migrations) 	

> ```
> python xxx.py db init
> ```

2 生成迁移版本文件

> ```
> python xxx.py db migrate -m "英文注释"
> ```

3 执行迁移命令 (往上迁移)

> ```
> python xxx.py db upgrade
> ```

```
自动创建迁移脚本有两个函数:
	upgrade()：函数把迁移中的改动应用到数据库中。
	downgrade()：函数则将改动删除。
自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。
对比不一定完全正确，有可能会遗漏一些细节，需要进行检查	
```

4 更新数据库

> ```
> python database.py db upgrade
> ```

5 返回以前的版本

可以根据history命令找到版本号,  然后传给downgrade命令:

> ```
> python app.py db history
>
> 输出格式：<base> ->  版本号 (head), initial migration
> ```

回滚到指定版本

> ```
> python app.py db downgrade 版本号
> ```

查看当前版本号:  python app.py db current

# 6 信号机制

## Flask信号机制

- Flask信号(signals, or event hooking)允许特定的发送端通知订阅者发生了什么（既然知道发生了什么，那我们可以根据自己业务需求实现自己的逻辑）。
- Flask提供了一些信号（核心信号）且其它的扩展提供更多的信号。
- 信号依赖于**Blinker**库。`pip install blinker`
- flask内置信号列表：[http://docs.jinkan.org/docs/flask/api.html#id17](http://docs.jinkan.org/docs/flask/api.html#id17)

```python
template_rendered = _signals.signal('template-rendered')
request_started = _signals.signal('request-started')
request_finished = _signals.signal('request-finished')
request_tearing_down = _signals.signal('request-tearing-down')
got_request_exception = _signals.signal('got-request-exception')
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')
appcontext_pushed = _signals.signal('appcontext-pushed')
appcontext_popped = _signals.signal('appcontext-popped')
message_flashed = _signals.signal('message-flashed')
```



### 信号应用场景

Flask-User 这个扩展中定义了名为 user_logged_in 的信号，当用户成功登入之后，这个信号会被发送。我们可以订阅该信号去追踪登录次数和登录IP：

```python
from flask import request
from flask_user.signals import user_logged_in

@user_logged_in.connect_via(app)
def track_logins(sender, user, **extra):
    user.login_count += 1
    user.last_login_ip = request.remote_addr
    db.session.add(user)
    db.session.commit()
```

## Flask-SQLAlchemy 信号支持

在 Flask-SQLAlchemy 模块中，0.10 版本开始支持信号，可以连接到信号来获取到底发生什么了的通知。存在于下面两个信号：

- models_committed
  - 这个信号在修改的模型提交到数据库时发出。发送者是发送修改的应用，模型 和 操作描述符 以 (model, operation) 形式作为元组，这样的元组列表传递给接受者的 changes 参数。
  - 该模型是发送到数据库的模型实例，当一个模型已经插入，操作是 'insert' ，而已删除是 'delete' ，如果更新了任何列，会是 'update' 。
- before_models_committed
  - 除了刚好在提交发送前发生，与 models_committed 完全相同。

```python
from flask_sqlalchemy import models_committed

# 给 models_committed 信号添加一个订阅者，即为当前 app
@models_committed.connect_via(app)
def models_committed(a, changes):
    print(a, changes)
```

> 对数据库进行增删改进行测试





