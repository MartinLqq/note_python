

# 源码分析基本流程

```
基本介绍
资源
使用方法
代码结构
对外接口
细节
扩展内容 (如: 类似模块, ...)
```



# records 库源码分析

文档

- 你的第一份Python库源码阅读：records库:  https://www.jianshu.com/p/b730aaf1b826



## 基本介绍

- records 属于 **kennethreitz** 的 for Humans™ 系列
- records 是一个对python中关系型数据库查询的封装，简化了在python中进行数据库查询的操作 
- records 使用原生sql去操作大多数的关系型数据库（Postgresql, MySQL, SQLite, Oracle和 MS-SQL），并且支持多种格式输出，如csv、excel、json等

- github链接为：[https://github.com/kennethreitz/records](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fkennethreitz%2Frecords)，

- 代码 500+ 行，如果是第一次尝试阅读python开源项目，这是一个很好的选择。

- 作者Kennethreitz是requests的作者，python领域的大牛人物之一，关于他还有一个励志的故事：[Kenneth Reitz的逆袭之路 ](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.sohu.com%2Fa%2F216138451_737973)



## 使用方法

records库的使用非常简单且人性化，定义数据库连接串和sql语句，然后将返回值作为rows打印出来，或者输出为文件，没有复杂的orm逻辑，实现逻辑很清晰

```python
import records

db = records.Database('postgres://...')
rows = db.query('select * from active_users')    # or db.query_file('sqls/active-users.sql')

>>> rows[0]
<Record {"username": "model-t", "active": true, "name": "Henry Ford", "user_email": "model-t@gmail.com"}>
```



## 依赖库

直接依赖:

- sqlalchemy:  ORM框架
- pytest:  单元测试库
- tablib:  用于导出xls、csv、yaml等格式
- docopt:  根据文档描述自动生成解析器, 可以非常容易的为python程序创建命令行界面，用于很多库的命令行指引

间接依赖:

- psycopg2:  操作PostgreSQL数据库,  sqlalchemy 依赖 psycopg2



## 代码结构

### Database

封装基本数据库操作，主要使用 query 方法，调用 SQLAlchemy 的方法，获取结果后调用 Record 类获得 Record 生成器，再调用 RecordCollection 获得所有的结果.

#### 初始化

```python
"""
1. 数据库 URL: db_url, 默认从环境变量中读取
2. kwargs 关键字参数全部交给 sqlalchemy 的 create_engine 方法
3. 调用 sqlalchemy 的 create_engine 创建数据库引擎对象
4. 设置自己的标志位: self.open, 用处有2: (1) __repr__方法中返回当前Database状态; (2) get_connection方法中确保close()方法没有被执行过
"""

class Database:
    # ...
	def __init__(self, db_url=None, **kwargs):
        # If no db_url was provided, fallback to $DATABASE_URL.
        self.db_url = db_url or DATABASE_URL

        if not self.db_url:
            raise ValueError('You must provide a db_url.')

        # Create an engine.
        self._engine = create_engine(self.db_url, **kwargs)
        self.open = True
```



#### get_table_names 方法

```python
"""
1. inspect(engine对象)  获取 sqlalchemy.engine.reflection.py::Inspector 对象
2. 调用 Inspector 对象的 get_table_names() 方法
"""

class Database:
    # ...
	def get_table_names(self, internal=False):
        """Returns a list of table names for the connected database."""

        # Setup SQLAlchemy for Database inspection.
        return inspect(self._engine).get_table_names()
```

#### get_connection 方法

```python
"""
将 sqlalchemy.engine.Connection 对象交给自定义的 Connection 对象进行管理,
返回 自定义的 Connection 对象
"""

class Database:
    # ...
	def get_connection(self):
        """Get a connection to this Database. Connections are retrieved from a
        pool.
        """
        if not self.open:
            raise exc.ResourceClosedError('Database closed.')

        return Connection(self._engine.connect())
```



#### transaction 方法

```python
"""
1. 使用 @contextmanager 装饰器实现上下文管理器,  控制 连接的开启，事务的开启、提交、异常时回滚，连接的关闭。
"""

class Database:
    # ...
	@contextmanager
    def transaction(self):
        """A context manager for executing a transaction on this Database."""

        conn = self.get_connection()
        tx = conn.transaction()
        try:
            yield conn
            tx.commit()
        except:
            tx.rollback()
        finally:
            conn.close()
```



#### query、bulk_query

```python
"""
1. 传入 sql 语句 和 其他参数
2. 使用 with 上下文创建一个自定义 Connection 对象, 并调用其 query 方法, 返回结果 (RecordCollection对象)
3. 实际会调用 sqlalchemy.engine.Connection 的 execute()方法
"""

class Database:
    # ...
	def query(self, query, fetchall=False, **params):
        """Executes the given SQL query against the Database. Parameters can,
        optionally, be provided. Returns a RecordCollection, which can be
        iterated over to get result rows as dictionaries.
        """
        with self.get_connection() as conn:
            return conn.query(query, fetchall, **params)
```

#### query_file、bulk_query_file

```python
"""
Bulk insert or update
用法参考 sqlalchemy.engine.Connection 的 execute()方法 docstring
"""
# execute 的 docstring:
 			conn.execute(
                 "INSERT INTO table (id, value) VALUES (?, ?)",
                 (1, "v1"), (2, "v2")
             )

             conn.execute(
                 "INSERT INTO table (id, value) VALUES (?, ?)",
                 1, "v1"
             )
```





### RecordCollection 

- RecordCollection 用于管理结果集,  即一个列表
- Record 用于管理一列数据,  即列表的一个元素

```python
db = records.Database(db_url='mysql+pymysql://root:123456@localhost/poem')
print(db.get_table_names())
rows = db.query('select * from poem_collections')
print(rows)  # <RecordCollection size=0 pending=True>
print(rows[0])  # <Record {"id": 1, "name": "Martin"}>
```

#### 接口

```
__repr__()
__iter__()
next()
__next__()
__getitem__()  # rows[0] 时调用,  不同于 Record, 此处索引是整数索引
__len__()
export()  # 间接调用 tablib.Dataset 的 export() 方法
dataset: property属性  # 主要为了 export() 使用， 将一列数据导出为 json/csv/txt 等格式
all()
as_dict()
first()
one()
scalar()  # Returns the first column of the first row, or `default
```



#### 解析

##### `__iter__()`

部分方法和 Record 类相同，但 RecordCollection 实现了 first 方法，获取第一个 row，如果不存在，则默认 default 为none,   如果 defalut 本身就是实例或者 exception 的子类，直接抛出异常，另外，实现了一次实例化后多次查询时的缓存。

```python
class RecordCollection:
	# ...
	def __iter__(self):
        """Iterate over all rows, consuming the underlying generator
        only when necessary."""
        i = 0
        while True:
            # Other code may have iterated between yields,
            # so always check the cache.
            if i < len(self):
                yield self[i]
            else:
                # Throws StopIteration when done.
                # Prevent StopIteration bubbling from generator, following https://www.python.org/dev/peps/pep-0479/
                try:
                    yield next(self)
                except StopIteration:
                    return
            i += 1
```



##### `__getitem__()`

```python
class RecordCollection:
	# ...
	def __getitem__(self, key):
        is_int = isinstance(key, int)

        # Convert RecordCollection[1] into slice.
        if is_int:
            key = slice(key, key + 1)

        while len(self) < key.stop or key.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all_rows[key]
        if is_int:   # 类似: rows[0]
            return rows[0]
        else:  # 类似: rows[:3]
            return RecordCollection(iter(rows))
```





### Record

接收 database 查询后的 keys 和 rows，初始化时，检测是否长度一致，然后对其包装，使其:

- 支持迭代
- 支持直接 to_dict 转为 dict 对象
- 支持直接 export 导出

```kotlin
除了基本的[0]索引形式，Record方法使其支持字符串查询，属性查询，支持 get 属性查询

1)支持以字符串的形式索引查找
if key in self.keys():
   i = self.keys().index(key)
   return self.values()[i]

2)支持以属性的形式查询
try:
     return self[key]
except KeyError as e:
     raise AttributeError(e)

3）支持get查询：
try:
    return self[key]
except KeyError:
    return default

4）通过 tablib 库，实现 dataset 属性：转为各种格式输出（json/txt/csv）
@property
def dataset(self):
        data = tablib.Dataset()
        data.headers = self.keys()
        row = _reduce_datetimes(self.values())
        data.append(row)
        return data
```



#### 接口

```
keys()    # 返回一列数据对应的 列名 列表
values()  # 返回一列数据对应的 值 列表
__repr__()
__getitem__()  # row['row_name'] 时调用,  不同于 RecordCollection, 此处索引是字符串索引
__getattr__()  # row.row_name 时调用
__dir__()      # 将所有的 row_name数据 加入到 原__dir__ 返回的字典中
get()          # row.get('row_name') 时调用
as_dict()      # 返回一列数据的 字典 或 有序字典
dataset: property属性  # 主要为了 export() 使用， 将一列数据导出为 json/csv/txt 等格式
export()       # 间接调用 tablib.Dataset 的 export() 方法
```





### 全局变量和方法

#### _reduce_datetimes()

```tsx
_reduce_datetimes方法，在tablib转为json等格式输出时，转化 row 中的时间字段。

row = list(row)
for i in range(len(row)):
     if hasattr(row[i], 'isoformat'):
          row[i] = row[i].isoformat()
return tuple(row)
```

#### cli

```
cli主方法，通过 docopt 获取命令行输入的参数，做合法检测等

arguments = docopt(cli_docs)
# Create the Database.
db = Database(arguments['--url'])
query = arguments['<query>']
params = arguments['<params>']
```





### 基础概念

```rust
1）获取系统环境变量，records中，初始化时传入数据库url，如果没传，才去找系统变量中的url

self.db_url = db_url or DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
'''
os.environ    获取系统环境变量
参考文档：http://blog.csdn.net/junweifan/article/details/7615591
'''

2）限制class的属性
__slots__ = ('_keys', '_values')

3）变量和方法名汇总
"""
        变量:
        1.  前带_的变量:  标明是一个私有变量, 只用于标明, 外部类还是可以访问到这个变量
        2.  前带两个_ , 后带两个_ 的变量:  标明是内置变量,
        3.  大写加下划线的变量:  标明是 不会发生改变的全局变量
        函数:
        1. 前带_的变量: 标明是一个私有函数, 只用于标明,
        2.  前带两个_ ,后带两个_ 的函数:  标明是特殊函数

        参考文章：
        http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820042500060e2921830a4adf94fb31bcea8d6f5c000
        http://blog.163.com/zhulp0372@yeah/blog/static/11589447920132541933516/
        http://blog.csdn.net/debugm/article/details/8179482
"""

4）repr和str的区别
http://www.cnpythoner.com/post/251.html

5) __getitem__和__setitem__为特殊方法，做重新定义
用于实现某些get的属性的校验需求, 参考示例：http://www.jb51.net/article/87447.htm
此处用于判断：key是int型还是string型，不同的get逻辑
print(row[1])
print(row["name"])

6) 重载 __getattr__ 和 __setattr__
来拦截对成员的访问，需要注意的是 __getattr__ 只有在访问不存在的成员时才会被调用
参考示例：http://www.360doc.com/content/14/0322/02/9482_362601063.shtml
print(row.name) //获取属性，仍然调用__getitem__

7) OrderedDict
"""  OrderedDict提供了一个有序的字典结构,记录了每个键值对添加的顺序,
如果初始化的时候同时传入多个参数，它们的顺序是随机的，不会按照位置顺序存储。"""
return OrderedDict(items) if ordered else dict(items)

8) @property装饰器
负责把dataset方法变成属性调用

9) __next__和__iter__
构造迭代器
```



