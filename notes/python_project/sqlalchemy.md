# sqlalchemy Engine

![../_images/sqla_engine_arch.png](https://docs.sqlalchemy.org/en/13/_images/sqla_engine_arch.png)

https://docs.sqlalchemy.org/en/13/core/engines.html



## Database Urls

The [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) function produces an [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) object based on a URL. These URLs follow [RFC-1738](http://rfc.net/rfc1738.html), and usually can include username, password, hostname, database name as well as optional keyword arguments for additional configuration. In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. The typical form of a database URL is:

```
dialect+driver://username:password@host:port/database
```

Dialect names include the identifying name of the SQLAlchemy dialect, a name such as `sqlite`, `mysql`, `postgresql`, `oracle`, or `mssql`. The drivername is the name of the DBAPI to be used to connect to the database using all lowercase letters. If not specified, a “default” DBAPI will be imported if available - this default is typically the most widely known driver available for that backend.

As the URL is like any other URL, special characters such as those that may be used in the password need to be URL encoded. Below is an example of a URL that includes the password `"kx%jj5/g"`:

```
postgresql+pg8000://dbuser:kx%25jj5%2Fg@pghost10/appdb
```

The encoding for the above password can be generated using `urllib`:

```
>>> import urllib.parse
>>> urllib.parse.quote_plus("kx%jj5/g")
'kx%25jj5%2Fg'
```

Examples for common connection styles follow below. For a full index of detailed information on all included dialects as well as links to third-party dialects, see [Dialects](https://docs.sqlalchemy.org/en/13/dialects/index.html).

### PostgreSQL

The PostgreSQL dialect uses psycopg2 as the default DBAPI. pg8000 is also available as a pure-Python substitute:

```
# default
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')

# psycopg2
engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

# pg8000
engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')
```

More notes on connecting to PostgreSQL at [PostgreSQL](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html).

### MySQL

The MySQL dialect uses mysql-python as the default DBAPI. There are many MySQL DBAPIs available, including MySQL-connector-python and OurSQL:

```
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')

# mysqlclient (a maintained fork of MySQL-Python)
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

# PyMySQL
engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
```

More notes on connecting to MySQL at [MySQL](https://docs.sqlalchemy.org/en/13/dialects/mysql.html).

### Oracle

The Oracle dialect uses cx_oracle as the default DBAPI:

```
engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')

engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')
```

More notes on connecting to Oracle at [Oracle](https://docs.sqlalchemy.org/en/13/dialects/oracle.html).

### Microsoft SQL Server

The SQL Server dialect uses pyodbc as the default DBAPI. pymssql is also available:

```
# pyodbc
engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')

# pymssql
engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
```

More notes on connecting to SQL Server at [Microsoft SQL Server](https://docs.sqlalchemy.org/en/13/dialects/mssql.html).

### SQLite

SQLite connects to file-based databases, using the Python built-in module `sqlite3` by default.

As SQLite connects to local files, the URL format is slightly different. The “file” portion of the URL is the filename of the database. For a relative file path, this requires three slashes:

```
# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine('sqlite:///foo.db')
```

And for an absolute file path, the three slashes are followed by the absolute path:

```
# Unix/Mac - 4 initial slashes in total
engine = create_engine('sqlite:////absolute/path/to/foo.db')

# Windows
engine = create_engine('sqlite:///C:\\path\\to\\foo.db')

# Windows alternative using raw string
engine = create_engine(r'sqlite:///C:\path\to\foo.db')
```

To use a SQLite `:memory:` database, specify an empty URL:

```
engine = create_engine('sqlite://')
```

More notes on connecting to SQLite at [SQLite](https://docs.sqlalchemy.org/en/13/dialects/sqlite.html).

### Others

See [Dialects](https://docs.sqlalchemy.org/en/13/dialects/index.html), the top-level page for all additional dialect documentation.



## Engine Creation API

- `sqlalchemy.``create_engine`(**args*, ***kwargs*)

  Create a new [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) instance.The standard calling form is to send the URL as the first positional argument, usually a string that indicates database dialect and connection arguments:`engine = create_engine("postgresql://scott:tiger@localhost/test")`Additional keyword arguments may then follow it which establish various options on the resulting [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) and its underlying [`Dialect`](https://docs.sqlalchemy.org/en/13/core/internals.html#sqlalchemy.engine.interfaces.Dialect) and [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool) constructs:`engine = create_engine("mysql://scott:tiger@hostname/dbname",                             encoding='latin1', echo=True)`The string form of the URL is `dialect[+driver]://user:password@host/dbname[?key=value..]`, where `dialect` is a database name such as `mysql`, `oracle`, `postgresql`, etc., and `driver` the name of a DBAPI, such as `psycopg2`, `pyodbc`, `cx_oracle`, etc. Alternatively, the URL can be an instance of [`URL`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.engine.url.URL).`**kwargs` takes a wide variety of options which are routed towards their appropriate components. Arguments may be specific to the [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine), the underlying [`Dialect`](https://docs.sqlalchemy.org/en/13/core/internals.html#sqlalchemy.engine.interfaces.Dialect), as well as the [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool). Specific dialects also accept keyword arguments that are unique to that dialect. Here, we describe the parameters that are common to most [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) usage.Once established, the newly resulting [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) will request a connection from the underlying [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool) once [`Engine.connect()`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.connect) is called, or a method which depends on it such as [`Engine.execute()`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.execute) is invoked. The [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool) in turn will establish the first actual DBAPI connection when this request is received. The [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) call itself does **not** establish any actual DBAPI connections directly.See also[Engine Configuration](https://docs.sqlalchemy.org/en/13/core/engines.html#)[Dialects](https://docs.sqlalchemy.org/en/13/dialects/index.html)[Working with Engines and Connections](https://docs.sqlalchemy.org/en/13/core/connections.html)Parameters**case_sensitive=True** – if False, result column names will match in a case-insensitive fashion, that is, `row['SomeColumn']`.**connect_args** – a dictionary of options which will be passed directly to the DBAPI’s `connect()` method as additional keyword arguments. See the example at [Custom DBAPI connect() arguments](https://docs.sqlalchemy.org/en/13/core/engines.html#custom-dbapi-args).**convert_unicode=False** –if set to True, causes all [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) datatypes to act as though the [`String.convert_unicode`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String.params.convert_unicode) flag has been set to `True`, regardless of a setting of `False` on an individual [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) type. This has the effect of causing all [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) -based columns to accommodate Python Unicode objects directly as though the datatype were the [`Unicode`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Unicode) type.*Deprecated since version 1.3:* The [`create_engine.convert_unicode`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.convert_unicode) parameter is deprecated and will be removed in a future release. All modern DBAPIs now support Python Unicode directly and this parameter is unnecessary.**creator** – a callable which returns a DBAPI connection. This creation function will be passed to the underlying connection pool and will be used to create all new database connections. Usage of this function causes connection parameters specified in the URL argument to be bypassed.**echo=False** –if True, the Engine will log all statements as well as a `repr()` of their parameter lists to the default log handler, which defaults to `sys.stdout` for output. If set to the string `"debug"`, result rows will be printed to the standard output as well. The `echo` attribute of `Engine` can be modified at any time to turn logging on and off; direct control of logging is also available using the standard Python `logging` module.See also[Configuring Logging](https://docs.sqlalchemy.org/en/13/core/engines.html#dbengine-logging) - further detail on how to configure logging.**echo_pool=False** –if True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler, which defaults to `sys.stdout` for output. If set to the string `"debug"`, the logging will include pool checkouts and checkins. Direct control of logging is also available using the standard Python `logging` module.See also[Configuring Logging](https://docs.sqlalchemy.org/en/13/core/engines.html#dbengine-logging) - further detail on how to configure logging.**empty_in_strategy** –The SQL compilation strategy to use when rendering an IN or NOT IN expression for [`ColumnOperators.in_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_) where the right-hand side is an empty set. This is a string value that may be one of `static`, `dynamic`, or `dynamic_warn`. The `static` strategy is the default, and an IN comparison to an empty set will generate a simple false expression “1 != 1”. The `dynamic` strategy behaves like that of SQLAlchemy 1.1 and earlier, emitting a false expression of the form “expr != expr”, which has the effect of evaluting to NULL in the case of a null expression. `dynamic_warn` is the same as `dynamic`, however also emits a warning when an empty set is encountered; this because the “dynamic” comparison is typically poorly performing on most databases.*New in version 1.2:* Added the `empty_in_strategy` setting and additionally defaulted the behavior for empty-set IN comparisons to a static boolean expression.**encoding** –Defaults to `utf-8`. This is the string encoding used by SQLAlchemy for string encode/decode operations which occur within SQLAlchemy, **outside of the DBAPI.** Most modern DBAPIs feature some degree of direct support for Python `unicode` objects, what you see in Python 2 as a string of the form `u'some string'`. For those scenarios where the DBAPI is detected as not supporting a Python `unicode` object, this encoding is used to determine the source/destination encoding. It is **not used** for those cases where the DBAPI handles unicode directly.To properly configure a system to accommodate Python `unicode` objects, the DBAPI should be configured to handle unicode to the greatest degree as is appropriate - see the notes on unicode pertaining to the specific target database in use at [Dialects](https://docs.sqlalchemy.org/en/13/dialects/index.html).Areas where string encoding may need to be accommodated outside of the DBAPI include zero or more of:the values passed to bound parameters, corresponding to the [`Unicode`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Unicode) type or the [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) type when `convert_unicode` is `True`;the values returned in result set columns corresponding to the [`Unicode`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Unicode) type or the [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) type when `convert_unicode` is `True`;the string SQL statement passed to the DBAPI’s `cursor.execute()` method;the string names of the keys in the bound parameter dictionary passed to the DBAPI’s `cursor.execute()` as well as `cursor.setinputsizes()` methods;the string column names retrieved from the DBAPI’s `cursor.description` attribute.When using Python 3, the DBAPI is required to support *all* of the above values as Python `unicode` objects, which in Python 3 are just known as `str`. In Python 2, the DBAPI does not specify unicode behavior at all, so SQLAlchemy must make decisions for each of the above values on a per-DBAPI basis - implementations are completely inconsistent in their behavior.**execution_options** – Dictionary execution options which will be applied to all connections. See [`execution_options()`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection.execution_options)**implicit_returning=True** – When `True`, a RETURNING- compatible construct, if available, will be used to fetch newly generated primary key values when a single row INSERT statement is emitted with no existing returning() clause. This applies to those backends which support RETURNING or a compatible construct, including PostgreSQL, Firebird, Oracle, Microsoft SQL Server. Set this to `False` to disable the automatic usage of RETURNING.**isolation_level** –this string parameter is interpreted by various dialects in order to affect the transaction isolation level of the database connection. The parameter essentially accepts some subset of these string arguments: `"SERIALIZABLE"`, `"REPEATABLE_READ"`, `"READ_COMMITTED"`, `"READ_UNCOMMITTED"` and `"AUTOCOMMIT"`. Behavior here varies per backend, and individual dialects should be consulted directly.Note that the isolation level can also be set on a per-[`Connection`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection) basis as well, using the[`Connection.execution_options.isolation_level`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) feature.See also[`Connection.default_isolation_level`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection.default_isolation_level) - view default level[`Connection.execution_options.isolation_level`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection.execution_options.params.isolation_level) - set per [`Connection`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Connection) isolation level[SQLite Transaction Isolation](https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#sqlite-isolation-level)[PostgreSQL Transaction Isolation](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#postgresql-isolation-level)[MySQL Transaction Isolation](https://docs.sqlalchemy.org/en/13/dialects/mysql.html#mysql-isolation-level)[Setting Transaction Isolation Levels](https://docs.sqlalchemy.org/en/13/orm/session_transaction.html#session-transaction-isolation) - for the ORM**label_length=None** – optional integer value which limits the size of dynamically generated column labels to that many characters. If less than 6, labels are generated as “_(counter)”. If `None`, the value of `dialect.max_identifier_length` is used instead.**listeners** – A list of one or more [`PoolListener`](https://docs.sqlalchemy.org/en/13/core/interfaces.html#sqlalchemy.interfaces.PoolListener) objects which will receive connection pool events.**logging_name** – String identifier which will be used within the “name” field of logging records generated within the “sqlalchemy.engine” logger. Defaults to a hexstring of the object’s id.**max_overflow=10** – the number of connections to allow in connection pool “overflow”, that is connections that can be opened above and beyond the pool_size setting, which defaults to five. this is only used with [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool).**module=None** – reference to a Python module object (the module itself, not its string name). Specifies an alternate DBAPI module to be used by the engine’s dialect. Each sub-dialect references a specific DBAPI which will be imported before first connect. This parameter causes the import to be bypassed, and the given module to be used instead. Can be used for testing of DBAPIs as well as to inject “mock” DBAPI implementations into the [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine).**paramstyle=None** – The [paramstyle](http://legacy.python.org/dev/peps/pep-0249/#paramstyle) to use when rendering bound parameters. This style defaults to the one recommended by the DBAPI itself, which is retrieved from the `.paramstyle` attribute of the DBAPI. However, most DBAPIs accept more than one paramstyle, and in particular it may be desirable to change a “named” paramstyle into a “positional” one, or vice versa. When this attribute is passed, it should be one of the values`"qmark"`, `"numeric"`, `"named"`, `"format"` or `"pyformat"`, and should correspond to a parameter style known to be supported by the DBAPI in use.**pool=None** – an already-constructed instance of [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool), such as a [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool) instance. If non-None, this pool will be used directly as the underlying connection pool for the engine, bypassing whatever connection parameters are present in the URL argument. For information on constructing connection pools manually, see [Connection Pooling](https://docs.sqlalchemy.org/en/13/core/pooling.html).**poolclass=None** – a [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool) subclass, which will be used to create a connection pool instance using the connection parameters given in the URL. Note this differs from `pool` in that you don’t actually instantiate the pool in this case, you just indicate what type of pool to be used.**pool_logging_name** – String identifier which will be used within the “name” field of logging records generated within the “sqlalchemy.pool” logger. Defaults to a hexstring of the object’s id.**pool_pre_ping** –boolean, if True will enable the connection pool “pre-ping” feature that tests connections for liveness upon each checkout.*New in version 1.2.*See also[Disconnect Handling - Pessimistic](https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects-pessimistic)**pool_size=5** – the number of connections to keep open inside the connection pool. This used with [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool) as well as [`SingletonThreadPool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.SingletonThreadPool). With [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool), a `pool_size` setting of 0 indicates no limit; to disable pooling, set `poolclass` to [`NullPool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.NullPool)instead.**pool_recycle=-1** –this setting causes the pool to recycle connections after the given number of seconds has passed. It defaults to -1, or no timeout. For example, setting to 3600 means connections will be recycled after one hour. Note that MySQL in particular will disconnect automatically if no activity is detected on a connection for eight hours (although this is configurable with the MySQLDB connection itself and the server configuration as well).See also[Setting Pool Recycle](https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-setting-recycle)**pool_reset_on_return='rollback'** –set the [`Pool.reset_on_return`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool.params.reset_on_return) parameter of the underlying [`Pool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool) object, which can be set to the values `"rollback"`, `"commit"`, or `None`.See also[`Pool.reset_on_return`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.Pool.params.reset_on_return)**pool_timeout=30** – number of seconds to wait before giving up on getting a connection from the pool. This is only used with [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool).**pool_use_lifo=False** –use LIFO (last-in-first-out) when retrieving connections from [`QueuePool`](https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool) instead of FIFO (first-in-first-out). Using LIFO, a server-side timeout scheme can reduce the number of connections used during non- peak periods of use. When planning for server-side timeouts, ensure that a recycle or pre-ping strategy is in use to gracefully handle stale connections.*New in version 1.3.*See also[Using FIFO vs. LIFO](https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-use-lifo)[Dealing with Disconnects](https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects)**plugins** –string list of plugin names to load. See [`CreateEnginePlugin`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.CreateEnginePlugin) for background.*New in version 1.2.3.***strategy='plain'** –selects alternate engine implementations. Currently available are:the `threadlocal` strategy, which is described in [Using the Threadlocal Execution Strategy](https://docs.sqlalchemy.org/en/13/core/connections.html#threadlocal-strategy);the `mock` strategy, which dispatches all statement execution to a function passed as the argument `executor`. See [example in the FAQ](http://docs.sqlalchemy.org/en/latest/faq/metadata_schema.html#how-can-i-get-the-create-table-drop-table-output-as-a-string).**executor=None** – a function taking arguments `(sql, *multiparams, **params)`, to which the `mock` strategy will dispatch all statement execution. Used only by `strategy='mock'`.



## Working with Engines and Connections

https://docs.sqlalchemy.org/en/13/core/connections.html



# sqlalchemy基本使用

http://www.mamicode.com/info-detail-2154073.html

数据库的操作

```
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Users,Person,Hobby
engine = create_engine(
         "mysql+pymysql://root:123@localhost:3306/ok1?charset=utf8",
         max_overflow=0,  # 超过连接池大小外最多创建的连接
         pool_size=5,  # 连接池大小
         pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
         pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)
Session = sessionmaker(bind=engine)
# ====== 每次执行数据库操作时，都需要创建一个session，申请一个连接 ======
session = Session()

# ############# 执行ORM操作 #############
# obj1 = Users(name="xxx")
# obj2 = Users(name="yyy")
# session.add(obj1)
# session.add(obj2)
# 增加多个项目，用add_all
# session.add_all([
#         Users(name="aaa"),
#         Users(name="bbb")
# ])
# 提交事务
# session.commit()
from sqlalchemy import and_, or_
ret = session.query(Person).join(Hobby,Person.hobby_id==Hobby.id,isouter=True)
# ret = session.query(Person).join(Hobby,and_(Person.hobby_id==Hobby.id,Person.id >2),isouter=True)
print(ret)
# 关闭session
session.close()
```



# session和scope_session

https://blog.csdn.net/u010339879/article/details/90179518

## session 使用问题

https://pdf-lib.org/Home/Details/7406



# 连接池

https://www.cnblogs.com/pengyusong/p/5790867.html

sqlalchemy数据库连接池的使用方式是延迟初始化，就是说一开始你调用 `create_engine(...)` 后创建的那个数据库池是空的，你后面通过 `session.connection()` 或者 `engine.connect()` 才开始创建连接，

每当你创建一个连接，你调用 `engine.pool.status()` 就可以看到数据库连接池处于什么状态，下面说明以下`status()` 的输出说明：

> 'Pool size: 16  Connections in pool: 1 Current Overflow: 1 Current Checked out connections: 16'
>
> Pool size 是你指定的数据库池的大小
>
> Connections in pool 是在池子中可以使用的连接有多少个
>
> Current Overflow 这个参数说明当前存在的连接数超过Pool size多少个，当overflow (初始为Pool size的负值) 超过max_overflow(默认为10)之后就不能创建新的连接了，只能等待，换句话说：你的数据库连接池的大小虽然只有Pool size个，但是你可以创建的连接数则是Pool size+max_overflow， 没创建一个连接overflow 都会加1，到等于max_overflow时候就不能在创建连接了
>
> Current Checked out connections 是被占用的连接数
>
> 注：这些都是看源码以及在python终端查看engine/session/engine.pool等的各种函数调用和属性获取到的，重要的查看地方: `__dict__`, `__class__`；在终端创建连接时注意用变量持有连接，不然你将会看到数据库连接池的状态不变
>
> 　　`engine.pool.checkedin()` 显示闲着的连接数个数，大小从0 ~ Pool size
>
> 　　`engine.pool.checkedout()` 显示被占用的连接数个数，大小从0 ~ Pool size+max_overflow

调用 `session.connection()` 或者 `engine.connect()`，从数据库池中拿连接，如果有闲着的连接就直接返回，没有闲着的就看下是否能创建连接（即数据库池满了），如果能就创建新连接，如果不能，则等待连接，超时时间可配置，请查看文档

调用 `Connection.close()` 释放连接，将数据库连接放回连接池，而不是真的关闭连接



# QueuePool

https://blog.csdn.net/Yaokai_AssultMaster/article/details/80958052

# 连接池多线程安全的问题

1、数据库模块model.py

```
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
session_factory = sessionmaker(bind=some_engine)
Session = scoped_session(session_factory)
```

2、业务模块thread.py

    import threading
    from model import Session
    
    class User(Base):
        tablename = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        fullname = Column(String(20))
        password = Column(String(20))
        age = Column(Integer)
    
    class MyThread(threading.Thread):
        def __init__(self, threadName):
            super(MyThread, self).__init__()
            self.name = threading.current_thread().name
    
        def run(self):
            session = Session() #每个线程都可以直接使用数据库模块定义的Session
            session.query(User).all()
            user = User(name="hawk-%s"%self.name, fullname="xxxx",password="xxxx",age=10)
            session.add(user)
            time.sleep(1)
            if self.name == "thread-9":
                session.commit()
            Session.remove()
    
    if name == "main":
        arr = []
        for i in xrange(10):
            arr.append(MyThread('thread-%s' % i))
        for i in arr:
            i.start()
        for i in arr:
            i.join()

# 连接池中的连接失效问题

http://m.vlambda.com/mip/wz_xaaG4ujzBd.html