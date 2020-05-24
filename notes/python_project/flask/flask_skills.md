# Debugger

在 flask 应用以 debug 模式启动/重启时,  一般会看到这些信息:

```
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 254-154-429
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

这里的 `Debugger PIN` 很重要,  在程序抛出未处理的异常时,  web 界面会出现 Traceback 信息,  此时可以借助这里的  `Debugger PIN`  在 web 页面上进行调试:

- 将鼠标移到在 Traceback 某一行的最右侧,  会出现一个小的控制台图标,  点击它,  在弹出的输入框中,  输入 `Debugger PIN` 对应的值
- 然后可以在 web 页面上,  像在 IDE 中一样进行调试



# SQLAlchemy

查看 SQLAlchemy 为查询生成的原生SQL

```
>>> str(User.query.filter_by(role=user_role)) 
'SELECT users.id AS users_id, users.username AS users_username, 
users.role_id AS users_role_id FROM users WHERE :param_1 = users.role_id'
```

# Flask-Script SHELL

集成Python shell,  让 Flask-Script 的 shell 命令自动导入特定的对象

*每次启动 shell 会话都要导入数据库实例和模型，这真是份枯燥的工作。为了避免一直重复导入，我们可以做些配置，让 Flask-Script 的 shell 命令自动导入特定的对象。*
*若想把对象添加到导入列表中，我们要为 shell 命令注册一个 [make_context] 回调函数*

```
from flask.ext.script import Shell 
 
def make_shell_context(): 
    return dict(app=app, db=db, User=User, Role=Role)
    
manager.add_command("shell", Shell(make_context=make_shell_context))

# make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入 shell：
$ python hello.py shell 
>>> app 
<Flask 'app'> 
>>> db 
<SQLAlchemy engine='sqlite:////home/flask/flasky/data.sqlite'> 
>>> User 
<class 'app.User'>
```



# flask 程序上下文(current_app)

在flask应用的后台线程中需要手动创建程序上下文

```
# 异步发送电子邮件
from threading import Thread 
 
def send_async_email(app, msg): 
    with app.app_context(): 
        mail.send(msg) 
 
def send_email(to, subject, template, **kwargs): 
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to]) 
    msg.body = render_template(template + '.txt', **kwargs) 
    msg.html = render_template(template + '.html', **kwargs) 
    thr = Thread(target=send_async_email, args=[app, msg]) 
    thr.start() 
    return thr

# Flask-Mail 中的 send() 函数使用 current_app，因此必须激活程序上下文。不过，
在不同线程中执行 mail.send() 函数时，程序上下文要使用 app.app_context() 人工创建。
```



# Flask-Migrate

使用 Flask-Migrate 实现数据库迁移

*数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中.*

*SQLAlchemy 的主力开发人员编写了一个迁移框架，称为 **Alembic**（https://alembic.readthedocs.*
*org/en/latest/index.html） 。除了直接使用 Alembic 之外，Flask 程序还可使用 **Flask-Migrate***
*（http://flask-migrate.readthedocs.org/en/latest/）扩展。这个扩展对 Alembic 做了轻量级包装，并*
*集成到 Flask-Script 中，所有操作都通过 **Flask-Script** 命令完成。*

```
初始化: 配置 Flask-Migrate
from flask.ext.migrate import Migrate, MigrateCommand 
# ... 
migrate = Migrate(app, db) 
manager.add_command('db', MigrateCommand)

1-创建迁移仓库
# 命令会创建 migrations 文件夹，所有迁移脚本都存放其中。
# 数据库迁移仓库中的文件要和程序的其他文件一起纳入版本控制
python hello.py db init

2-创建迁移脚本
# 在 Alembic 中，数据库迁移用迁移脚本表示。脚本中有两个函数，分别是 upgrade() 和 downgrade()。
# upgrade() 把迁移中的改动应用到数据库中，downgrade() 将改动删除。
# revision 命令手动创建 Alembic 迁移，migrate 命令自动创建。手动创建的迁移只是一个骨架，upgrade() 和 downgrade() 函数都是空的，开发者要使用Alembic 提供的 Operations 对象指令实现具体操作; 自动创建的迁移会根据模型定义和数据库当前状态之间的差异生成 upgrade() 和 downgrade() 函数的内容。
python hello.py db migrate -m "initial migration"

3-更新数据库
# db upgrade 命令把迁移应用到数据库中：
python hello.py db upgrade 
```



flask源码分析器

源码分析器能找出程序中执行最慢的部分。分析器监视运行中的程序，记录调用的函数以及运行各函数所消耗的时间，然后生成一份详细的报告，指出运行最慢的函数。

```
# manage.py：在请求分析器的监视下运行程序

@manager.command 
def profile(length=25, profile_dir=None): 
    """Start the application under the code profiler.""" 
    from werkzeug.contrib.profiler import ProfilerMiddleware 
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], 
                                      profile_dir=profile_dir) 
    app.run()

使用 python manage.py profile 启动程序后，终端会显示每条请求的分析数据。
--length 选项可以修改报告中显示的函数数量。
--profile-dir 选项会保存每条请求的分析数据到指定目录下的一个文件中。分析器数据文件可用来生成更详细的报告，例如调用图。
Python 分析器的详细信息请参阅官方文档（https://docs.python.org/2/library/profile.html）
```



flask部署的部分自动化

```
部署流程
不管使用哪种托管方案，程序安装到生产服务器上之后，都要执行一系列的任务。最好的例子就是创建或更新数据库表。
如果每次安装或升级程序都手动执行任务，那么容易出错也浪费时间，所以我们可以在manage.py 中添加一个命令，自动执行所需操作。
# 实现一个适用于 Flasky 的 deploy 命令。
# manage.py：部署命令

@manager.command 
def deploy(): 
    """Run deployment tasks.""" 
    from flask.ext.migrate import upgrade 
    from app.models import Role, User 
 
    # 把数据库迁移到最新修订版本 
    upgrade() 
 
    # 创建用户角色 
    Role.insert_roles() 

    # 让所有用户都关注此用户 
    User.add_self_follows()

# 这个命令调用的函数之前都已经定义好了，现在只是将它们集中调用
```



flask生产模式下日志处理

```
在程序启动过程中，Flask 会创建一个 Python 提供的 logging.Logger 类实例，并将其附属到程序实例上，得到 app.logger。在调试模式中，日志记录器会把记录写入终端；但在生产模式中，默认情况下没有配置日志的处理程序，所以如果不添加处理程序，就不会保存日志。

# 配置一个日志处理程序，把生产模式中出现的错误通过电子邮件发送给 FLASKY_ADMIN 中设置的管理员。
# config.py：程序出错时发送电子邮件
class ProductionConfig(Config): 
    # ... 
    @classmethod 
    def init_app(cls, app): 
        Config.init_app(app) 
 
        # 把错误通过电子邮件发送给管理员 
        import logging 
        from logging.handlers import SMTPHandler 
        credentials = None 
        secure = None 
        if getattr(cls, 'MAIL_USERNAME', None) is not None: 
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD) 
            if getattr(cls, 'MAIL_USE_TLS', None): 
                secure = () 
        mail_handler = SMTPHandler( 
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT), 
            fromaddr=cls.FLASKY_MAIL_SENDER, 
            toaddrs=[cls.FLASKY_ADMIN], 
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error', 
            credentials=credentials, 
            secure=secure) 
        mail_handler.setLevel(logging.ERROR) 
        app.logger.addHandler(mail_handler)
```









# FlaskWeb开发.pdf 第17章 部署



# Flask扩展



**Flask 官方扩展网站（http://flask.pocoo.org/extensions/）**



FLask-RESTful（http://flask-restful.readthedocs.org/en/latest/） ：开发 REST API 的工具

Flask-DebugToolbar（https://github.com/mgood/flask-debugtoolbar） ：在浏览器中使用的调试工具

Flask-WhooshAlchemy（https://pythonhosted.org/Flask-WhooshAlchemy/） ：使用 Whoosh
（http://pythonhosted.org/Whoosh/）实现 Flask-SQLAlchemy 模型的全文搜索。
Flask-KVsession（http://flask-kvsession.readthedocs.org/en/latest/） ：使用服务器端存储实现的另一种用户会话。

