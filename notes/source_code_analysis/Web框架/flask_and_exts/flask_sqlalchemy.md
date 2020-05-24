# ==== flask-sqlalchemy ====

# 资源

## <用户指南>

http://www.pythondoc.com/flask-sqlalchemy/index.html 

官方用户指南的目录结构:

```
快速入门
    一个最小应用
    简单的关系
    启蒙之路
    引入上下文
配置
    配置键
    连接 URI 格式
    使用自定义的元数据和命名约定
声明模型
    简单示例
    一对多(one-to-many)关系
    多对多(many-to-many)关系
选择(Select),插入(Insert), 删除(Delete)
    插入记录
    删除记录
    查询记录
    在视图中查询
绑定多个数据库
    示例配置
    创建和删除表
    引用绑定(Binds)
信号支持
```



# 最小的用例

```python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost:3306/web_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return "<User %d %s %s>" % (self.id, self.username, self.email)


# 创建表
db.create_all()

name = "Flask"
query_obj = User.query.filter(User.username == name)
if not query_obj.first():  # 不存在
    user = User(username=name, email="example@example.com")
    # 增
    db.session.add(user)
db.session.commit()

# 查
users = User.query.all()
print(users)

```



# \_\_init__.py

```
models_committed          # 属性, flask 信号
before_models_committed   # 属性, flask 信号
SignallingSession
get_debug_queries
Pagination
BaseQuery
_QueryProperty
_record_queries
_EngineConnector
get_state
_SQLAlchemyState
SQLAlchemy
_BoundDeclarativeMeta
FSADeprecationWarning
```

## Pagination

- 内部使用的分页辅助类





## BaseQuery

- 继承自 sqlalchemy 的 Query,  增加 3 个方法:  

  ```
  get_or_404
  first_or_404
  paginate
  ```

- 返回一个 Pagination 对象

所有接口:

```
__init__
statement
subquery
cte
label
as_scalar
selectable
only_return_tuples
enable_eagerloads
with_labels
enable_assertions
whereclause
with_polymorphic
yield_per
get
correlate
autoflush
populate_existing
with_parent
add_entity
with_session
from_self
values
value
with_entities
add_columns
add_column
options
with_transformation
with_hint
with_statement_hint
execution_options
with_lockmode
with_for_update
params
filter
filter_by
order_by
group_by
having
union
union_all
intersect
intersect_all
except_
except_all
join
outerjoin
reset_joinpoint
select_from
select_entity_from
__getitem__
slice
limit
offset
distinct
prefix_with
suffix_with
all
from_statement
first
one_or_none
one
scalar
__iter__
__str__
column_descriptions
instances
merge_result
exists
count
delete
update
lazy_loaded_from
session
```



## SQLAlchemy -- 重点类

接口概览

```
__init__
metadata
create_scoped_session
create_session
make_declarative_base
init_app
apply_pool_defaults
apply_driver_hacks
engine
make_connector
get_engine
get_app
get_tables_for_bind
get_binds
_execute_for_all_tables
create_all
drop_all
reflect
__repr__
Model
Query
_engine_lock
app
session
use_native_unicode
```



_include_sqlalchemy  使导入更方便

```python
"""
This class also provides access to all the SQLAlchemy functions and classes
    from the :mod:`sqlalchemy` and :mod:`sqlalchemy.orm` modules.
"""
# 实现的源码是:
def _include_sqlalchemy(obj, cls):
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))
    # Note: obj.Table does not attempt to be a SQLAlchemy Table class.
    obj.Table = _make_table(obj)
    obj.relationship = _wrap_with_default_query_class(obj.relationship, cls)
    obj.relation = _wrap_with_default_query_class(obj.relation, cls)
    obj.dynamic_loader = _wrap_with_default_query_class(obj.dynamic_loader, cls)
    obj.event = event
```







# ==== sqlalchemy ====

# sqlalchemy 好文

SQLAlchemy模型使用   https://www.cnblogs.com/panwenbin-logs/p/5731265.html

> **见一个单独的笔记  `sqlalchemy.md` ,  将此链接上的内容复制了下来,  **
>
> **并且 Mysql 相关的代码已经过测试.**

# 脱离 flask app 的用例

- 参考廖雪峰教程:   https://www.liaoxuefeng.com/wiki/1016959663602400/1017803857459008 



## db.py

```python
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DB:

    def __init__(self, url, auto_commit=False, **kwargs):
        if '?charset' not in url:  # 解决一个中文bug
            url += '?charset=utf8'
        # 初始化数据库连接
        self.__engine = create_engine(url, **kwargs)
        # 创建 Session 类
        self.__session_factory = sessionmaker(bind=self.__engine, autocommit=auto_commit)
        self.session = self.__session_factory()
        self.Model = declarative_base(
            # cls=object,
            name='Model',
            # metadata=None,
            # metaclass=DeclarativeMeta
        )

        self._compact()
        _include_sqlalchemy(self)

    def _compact(self):
        self.session.create_all = self.create_all
        self.session.drop_all = self.drop_all

    def create_all(self):
        self.Model.metadata.create_all(self.__engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.__engine)


def _include_sqlalchemy(obj):
    """This function is from flask-sqlalchemy.
    It`s a convenient way to use `db.` to call the methods in sqlalchemy and sqlalchemy.orm
    """
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))

```

## db_model_test.py

```python
from sqlalchemy import Column, String, Integer
from db import DB

# url = 'mysql://root:123456@localhost:3306/web_flask'  # 需要 MySQLdb
url = 'mysql+pymysql://root:123456@localhost:3306/web_flask'  # 需要 pymysql
db = DB(url)


class Role(db.Model):
    __tablename__ = 'roles'  # 表名
    # 表结构
    id = Column(Integer, primary_key=True)
    role = Column(String(50), unique=True)

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.id, self.role)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return "<User %d %s %s>" % (self.id, self.username, self.email)


if __name__ == '__main__':
    # db.session.drop_all()
    # db.session.create_all()

    # role = Role(role='学生')
    # db.session.add(role)
    # db.session.commit()

    roles = db.session.query(Role).all()
    # 注: 没有实现 Role.query.xxx
    print(roles)

    db.session.close()
    
```







# === 模型定义示例 ===

```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from info import constants
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


# 用户收藏表，建立用户与其收藏新闻多对多的关系
tb_user_collection = db.Table(
    "info_user_collection",
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),  # 新闻编号
    db.Column("news_id", db.Integer, db.ForeignKey("info_news.id"), primary_key=True),  # 分类编号
    db.Column("create_time", db.DateTime, default=datetime.now)  # 收藏创建时间
)

tb_user_follows = db.Table(
    "info_user_fans",
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)  # 被关注人的id
)


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间, 默认为完成注册时的时间, 后面需要写代码更新这个时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 订单的状态
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN")

    # 当前用户收藏的所有新闻
    collection_news = db.relationship("News", secondary=tb_user_collection, lazy="dynamic")  # 用户收藏的新闻
    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    followers = db.relationship('User',
                                secondary=tb_user_follows,
                                primaryjoin=id == tb_user_follows.c.followed_id,
                                secondaryjoin=id == tb_user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')

    # 当前用户所发布的新闻
    news_list = db.relationship('News', backref='user', lazy='dynamic')

    # todo --------------- 密码处理 start ---------------
    @property
    def password(self):
        """
        不可用self.password方式取值
        """
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        """
        可以用 self.password = value 的方式设置值, 执行以下代码
        """
        self.password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        """
        可以用 self.check_password(password) 的方式校验密码
        """
        return check_password_hash(self.password_hash, password)
    # --------------- 密码处理 end ----------------

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
            "mobile": self.mobile,
            "gender": self.gender if self.gender else "MAN",
            "signature": self.signature if self.signature else "",
            "followers_count": self.followers.count(),
            "news_count": self.news_list.count()
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict


class News(BaseModel, db.Model):
    """新闻"""
    __tablename__ = "info_news"

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    category_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"))  # 当前新闻的作者id
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    # 当前新闻的所有评论
    comments = db.relationship("Comment", lazy="dynamic")

    def to_review_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "reason": self.reason if self.reason else ""
        }
        return resp_dict

    def to_basic_dict(self):
        """基础数据"""
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "index_image_url": self.index_image_url,
            "clicks": self.clicks,
        }
        return resp_dict

    def to_dict(self):
        """详细数据"""
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "comments_count": self.comments.count(),
            "clicks": self.clicks,
            "category": self.category.to_dict(),
            "index_image_url": self.index_image_url,
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict


class Comment(BaseModel, db.Model):
    """评论"""
    __tablename__ = "info_comment"

    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("info_news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("info_comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "news_id": self.news_id,
            "like_count": self.like_count
        }
        return resp_dict


class CommentLike(BaseModel, db.Model):
    """评论点赞"""
    __tablename__ = "info_comment_like"
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("info_comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True)  # 用户编号


class Category(BaseModel, db.Model):
    """新闻分类"""
    __tablename__ = "info_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    news_list = db.relationship('News', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict
```



