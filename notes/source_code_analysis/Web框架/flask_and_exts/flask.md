[TOC]



# ==== flask ====

资源:

- 用尽洪荒之力学习Flask源码:  https://www.jianshu.com/p/c19beeea32a1 



# 模块文件概览

已简单分析的在前面打勾

```
√ flask/ext
  flask/testsuite
  __init__.py
  _compat.py
√ app.py
  blueprints.py
√ config.py
√ ctx.py
  debughelpers.py
√ exthook.py
√ globals.py
  helpers.py
  json.py
  logging.py
√ module.py
√ sessions.py
  signals.py
√ templating.py
  testing.py
  views.py
  wrappers.py
```





# app.py::Flask

## 接口概览 

Flask 对象的接口概览 (从下往上看, 下面是属性)

```
name    # locked_cached_property, 当前应用名称.
propagate_exceptions  # property, 返回配置 PROPAGATE_EXCEPTIONS
preserve_context_on_exception   # property, 返回配置 PRESERVE_CONTEXT_ON_EXCEPTION
logger
jinja_env             # locked_cached_property, 
got_first_request     # locked_cached_property, 返回当前应用是否已经处理过请求
make_config
auto_find_instance_path
open_instance_resource   # Opens a resource from the application's instance folder
create_jinja_environment    # 创建 Jinja2 environment, 添加一些全局变量.
create_global_jinja_loader  # Creates the loader for the Jinja2 environment
init_jinja_globals  # 已改为 create_jinja_environment
select_jinja_autoescape
update_template_context
run                 # 启动一个本地开发服务, 本质是调用 werkzeug.serving::run_simple
test_client	 		# 为当前应用创建一个测试客户端, 用于单元测试. 详见 FlaskClient
open_session
save_session
make_null_session
register_module     # 方法, 用于注册Module, 实现模块化应用. 详见: www.jb51.net/article/123329.htm
register_blueprint  # 方法, 为应用注册一个蓝图
add_url_rule  # 方法
route         # 装饰器, 用于注册一个视图函数, 与 add_url_rule 方法类似
endpoint      # 装饰器, A decorator to register a function as an endpoint
errorhandler  # 装饰器, 用于全局捕获指定异常对象或异常码(如404)
register_error_handler  # 作用等同于 errorhandler, 但不是装饰器
template_filter     # 装饰器, 用于定义一个 模板过滤器
add_template_filter
template_test
add_template_test
template_global     #  装饰器, 用来增加一个模板全局方法
add_template_global  # 在 template_global 内部会被调用的方法
before_request
before_first_request
after_request
teardown_request
teardown_appcontext
context_processor
url_value_preprocessor
url_defaults
handle_http_exception
trap_http_exception
handle_user_exception
handle_exception
log_exception
raise_routing_exception
dispatch_request       # 方法, 用于 self.full_dispatch_request 方法内, 分发请求
full_dispatch_request  # 方法, 用于 self.wsgi_app 方法内, 执行请求钩子函数 & 分发请求
# full_dispatch_request 基本调用流程:
    """
    1. try_trigger_before_first_request_functions
    2  preprocess_request
    3. dispatch_request
    4. handle_user_exception
    5. make_response
    6. process_response
    """

try_trigger_before_first_request_functions
make_default_options_response  # 创建 OPTIONS 请求方式对应的默认响应
should_ignore_error
make_response    # 方法, 将 视图函数的返回值 包装成响应对象, 
				# 视图函数返回值可以是:
                   1. self.response_class 的实例
                   2. str
                   3. unicode
                   4. a WSGI function
                   5. tuple:  (响应内容, 状态码, 响应头)
create_url_adapter
inject_url_defaults
handle_url_build_error  # 方法, 处理 url_for 抛出的 BuildError
preprocess_request  # 方法, 在分发请求之前执行
process_response    # 方法, 处理响应
do_teardown_request
do_teardown_appcontext
app_context        # 方法, 返回一个应用上下文 RequestContext 对象
request_context    # 方法, 返回一个请求上下文 AppContext 对象
test_request_context  # 用于单元测试, 在 testing.py::FlaskClient 内部有使用到
wsgi_app		  # 方法, The actual WSGI application. 
				 # 建立请求上下文 -> 分发请求 -> 处理响应/异常

modules   # property, 实际返回 self.blueprints
after_request_funcs
app_ctx_globals_class
before_first_request_funcs
before_request_funcs
blueprints		   # 属性, dict, 存储所有可访问的蓝图
config			   # 属性, self.make_config 方法的返回结果, 实际是 Config 对象.
debug
debug_log_format
default_config      # 属性, ImmutableDict, 存储默认配置项
enable_modules      # 属性, bool
error_handler_spec  # 属性, dict, 存储所有已注册的 error handlers.  The key is `None`
error_handlers      # 现在用 error_handler_spec
extensions          # 属性, 与扩展模块有关
instance_path
jinja_options  # ImmutableDict, 直接传给 Jinja2 environment 的选项.
json_decoder
json_encoder
logger_name
permanent_session_lifetime  # 属性, session过期时间
request_class
request_globals_class  # property, 默认是 _AppCtxGlobals
response_class
secret_key
session_cookie_name  # 属性, 在cookie中存储的session键, 默认是'session'
session_interface    # 属性, session接口对象, 默认是 SecureCookieSessionInterface()
static_folder        # property, 获取静态文件的绝对路径
static_url_path		 # property, 获取静态文件访问路由, 如 '/static'
teardown_appcontext_funcs  # 属性, list, 存储应用上下文被销毁时会被执行的函数
teardown_request_funcs     # 属性, dict, 存储每次请求后会被执行的函数
template_context_processors
test_client_class    # 属性, 被 test_client 方法使用.
testing  			# 属性, bool, TESTING配置项
url_build_error_handlers  # 属性, 函数列表, 当 url_for 抛出 BuildError 时函数会被调用
url_default_functions  # 属性, dict, URL value preprocessors
url_map			    # 属性, Map(), 路由映射关系
url_rule_class		# 属性, Rule, The rule object to use for URL rules created
url_value_preprocessors  # 属性, dict, URL value processor functions
use_x_sendfil		# 属性, bool
view_functions		# 属性, dict, 记录所有的视图函数
```



## 重要接口

列出一些比较重要的接口方法/属性

```
run           # 基于wekzeug，可以迅速启动一个WSGI应用 
test_client   # 为当前应用创建一个测试客户端, 用于单元测试. 详见 FlaskClient
register_blueprint  # 为应用注册一个蓝图
route         # 装饰器, 用于注册一个视图函数, 与 add_url_rule 方法类似
errorhandler  # 装饰器, 用于全局捕获指定异常对象或异常码(如404)
before_request
before_first_request
after_request
teardown_request
# 上面这些钩子函数(装饰器) 是在 Flask 类中定义的,
# 还有一个 ctx.py::after_this_request 装饰器, 在视图函数内部装饰一个目标函数, 目标函数在请求后, 响应前会被执行, 这是也算是一个钩子函数, 但仅作用于当前路由下.


dispatch_request
full_dispatch_request
make_response
app_context
request_context
wsgi_app		  # 方法, The actual WSGI application. 
				 # 建立请求上下文 -> 分发请求 -> 处理响应/异常
config
url_map
view_functions
```





# config.py

## Config

```python
class Config(dict):
    """
    1.from_envvar
    2.from_pyfile
    3.from_object
    """
    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_envvar(self, variable_name, silent=False):
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:  # 提供silent选项, 是否抛出异常
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        # ======== Tip =========
        # d = imp.new_module('config')
        # 对于新版本python, 可以使用:
        d = modulefinder.Module('config')
        # ======================
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                # compile 结合 exec: 执行文件中的变量定义语句, 并将所有变量加入 d.__dict__
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, string_types):  # 支持通过字符串指定obj, 如 'config.Config'
            obj = import_string(obj)  # 调用werkzeug\utils.py的 import_string 函数. 下面列出了源码
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
```





## ConfigAttribute

使用 ConfigAttribute 描述符来管理 flask config

```python
class ConfigAttribute(object):
    """Makes an attribute forward to the config"""

    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        if self.get_converter is not None:
            rv = self.get_converter(rv)  # 数据经过get_converter指定的转换器来转换类型
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value
```

app.py::Flask 中使用到了 ConfigAttribute, 如下例子是传了 get_converter 的情况:

```python
# flask\app.py::Flask
permanent_session_lifetime = ConfigAttribute('PERMANENT_SESSION_LIFETIME',
                                             get_converter=_make_timedelta)
# flask\app.py::_make_timedelta
def _make_timedelta(value):
    if not isinstance(value, timedelta):
        return timedelta(seconds=value)
    return value
```





# ctx.py

- 定义上下文需要的一些对象

## after_this_request

- 装饰一个函数,  被装饰函数在请求后 (响应前) 会被执行,  需要接收一个参数: **response**

Example:

```python
@app.route('/')
def index():
    @after_this_request
    def add_header(response):
        response.headers['X-Foo'] = 'Parachute'
        return response
    return 'Hello World!'
```

## copy_current_request_context

- 复制当前请求上下文,  让多线程不会超出请求上下文

```python
@app.route('/multi_threads')
def multi_threads_out_of_ctx():
    @copy_current_request_context
    def background_task():
        import time
        time.sleep(10)
        print(request.method)

    from threading import Thread
    th = Thread(target=background_task)
    th.start()
    th.join()   # 阻塞主线程, 等待子线程执行完
    return 'multi_threads done'
```

## has_request_context

## has_app_context

## AppContext

## RequestContext



# ext/\_\_init__.py

主要是调用 exthook.py::ExtensionImporter 来重定向导入扩展模块

```python
"""
    重定向导入扩展模块.
        1. 当使用 `from flask.ext.foo import bar` 时, ExtensionImporter 会重定向为 `from flask_foo import bar`.
        2. 当上面方法导入失败时, 再尝试 `from flaskext.foo import bar`.
"""

def setup():
    from ..exthook import ExtensionImporter
    importer = ExtensionImporter(['flask_%s', 'flaskext.%s'], __name__)
    importer.install()

setup()
del setup
```

# exthook.py

## ExtensionImporter

```python
"""重定向导入扩展模块. This is used by `flask.ext`.
"""
import sys
import os
from ._compat import reraise


class ExtensionImporter(object):
    def __init__(self, module_choices, wrapper_module):
        self.module_choices = module_choices
        self.wrapper_module = wrapper_module
        self.prefix = wrapper_module + '.'
        self.prefix_cutoff = wrapper_module.count('.') + 1

    def __eq__(self, other):
        # 判断两个模块对象是否相同
        return self.__class__.__module__ == other.__class__.__module__ and \
               self.__class__.__name__ == other.__class__.__name__ and \
               self.wrapper_module == other.wrapper_module and \
               self.module_choices == other.module_choices

    def __ne__(self, other):
        return not self.__eq__(other)

    def install(self):
        # 将当前 ExtensionImporter 对象添加到 sys.meta_path 列表中, 不重复添加.
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]

    def find_module(self, fullname, path=None):
        # 相当于路由, 匹配 `flask.` 开头的导入方式. 
        # 如果匹配成功, 返回当前 ExtensionImporter 对象.
        if fullname.startswith(self.prefix):
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        # fullname如: `flask.ext.wtf`
        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        # modname如: wtf
        for path in self.module_choices:
            realname = path % modname
            # realname如: flask_wtf 或 flaskext.wtf
            try:
                __import__(realname)  # 相当于: import flask_wtf
            except ImportError:
                # 存疑: 这是处理什么情况?
                exc_type, exc_value, tb = sys.exc_info()
                sys.modules.pop(fullname, None)
			   # 存疑: 这是处理什么情况?
                if self.is_important_traceback(realname, tb):
                    reraise(exc_type, exc_value, tb.tb_next)
                continue
            # 上面__import__成功执行后, sys.modules[realname]就指向目标模块,
            # 再将模块对象重定向到 sys.modules[fullname],
            module = sys.modules[fullname] = sys.modules[realname]
            if '.' not in modname:
                setattr(sys.modules[self.wrapper_module], modname, module)
            # 返回模块对象
            return module
        raise ImportError('No module named %s' % fullname)

    def is_important_traceback(self, important_module, tb):
        """Walks a traceback's frames and checks if any of the frames
        originated in the given important module.  If that is the case then we
        were able to import the module itself but apparently something went
        wrong when the module was imported.  (Eg: import of an import failed).
        """
        while tb is not None:
            if self.is_important_frame(important_module, tb):
                return True
            tb = tb.tb_next
        return False

    def is_important_frame(self, important_module, tb):
        """Checks a single frame if it's important."""
        g = tb.tb_frame.f_globals
        if '__name__' not in g:
            return False

        module_name = g['__name__']

        # Python 2.7 Behavior.  Modules are cleaned up late so the
        # name shows up properly here.  Success!
        if module_name == important_module:
            return True

        # Some python versions will will clean up modules so early that the
        # module name at that point is no longer set.  Try guessing from
        # the filename then.
        filename = os.path.abspath(tb.tb_frame.f_code.co_filename)
        test_string = os.path.sep + important_module.replace('.', os.path.sep)
        return test_string + '.py' in filename or \
               test_string + os.path.sep + '__init__.py' in filename

```



# globals.py

- Defines all the global objects that are proxies to the current active context

```python
def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return getattr(top, name)


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return top.app


# context locals
_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))
```





# module.py

- flask应用注册 Module:  https://www.jb51.net/article/123329.htm 
  -  **Flask应用怎么注册一个Module** 
  -  **注册Module时发生了什么** 

```python
import os

from .blueprints import Blueprint


def blueprint_is_module(bp):
    """Used to figure out if something is actually a module"""
    return isinstance(bp, Module)


class Module(Blueprint):
    """Deprecated module support.  Until Flask 0.6 modules were a different
    name of the concept now available as blueprints in Flask.  They are
    essentially doing the same but have some bad semantics for templates and
    static files that were fixed with blueprints.

    .. versionchanged:: 0.7
       Modules were deprecated in favor for blueprints.
    """

    def __init__(self, import_name, name=None, url_prefix=None,
                 static_path=None, subdomain=None):
        if name is None:
            assert '.' in import_name, 'name required if package name ' \
                'does not point to a submodule'
            name = import_name.rsplit('.', 1)[1]
        Blueprint.__init__(self, name, import_name, url_prefix=url_prefix,
                           subdomain=subdomain, template_folder='templates')

        if os.path.isdir(os.path.join(self.root_path, 'static')):
            self._static_folder = 'static'
```



##  Flask应用注册 Module 的示例

- Module 的注册同 蓝图 的注册

项目结构

```
/myapplication
  /__init__.py
  /app.py
  /views
    /__init__.py
    /admin.py
    /blog.py
```

admin.py

```python
# admin.py
from flask import Module
admin = Module(__name__)

@admin.route('/')
def index():
  return "This is admin page!"

@admin.route('/profile')
def profile():
  return "This is profile page."
```

blog.py

```python
# blog.py
from flask import Module
blog = Module(__name__)

@blog.route('/')
def index():
  return "This is my blog!"

@blog.route('/article/<int:id>')
def article(id):
  return "The article id is %d." % id
```

app.py  注册 module

```python
# app.py
from flask import Flask
from views.admin import admin
from views.blog import blog
app = Flask(__name__)

@app.route('/')
def index():
  return "This is my app."

app.register_module(blog, url_prefix='/blog')
app.register_module(admin, url_prefix='/admin')
# 查看路由映射关系
print(url_map)

if __name__ == '__main__':
    app.run(debug=True)
```



## app.register_module

```python
class Flask:
    
    # ...
    
    def register_module(self, module, **options):
        """Registers a module with this application.  The keyword argument
        of this function are the same as the ones for the constructor of the
        :class:`Module` class and will override the values of the module if
        provided.

        .. versionchanged:: 0.7
           The module system was deprecated in favor for the blueprint
           system.
        """
        assert blueprint_is_module(module), 'register_module requires ' \
            'actual module objects.  Please upgrade to blueprints though.'
        if not self.enable_modules:
            raise RuntimeError('Module support was disabled but code '
                'attempted to register a module named %r' % module)
        else:
            from warnings import warn
            warn(DeprecationWarning('Modules are deprecated.  Upgrade to '
                'using blueprints.  Have a look into the documentation for '
                'more information.  If this module was registered by a '
                'Flask-Extension upgrade the extension or contact the author '
                'of that extension instead.  (Registered %r)' % module),
                stacklevel=2)

        self.register_blueprint(module, **options)
```



# sessions.py

## 内置session的处理机制

flask 默认使用的 session接口 是 SecureCookieSessionInterface,  使用的 session类 是 **SecureCookieSession**

```python
# flask\app.py::Flask	~line-313
session_interface = SecureCookieSessionInterface()

# flask\sessions.py::SecureCookieSessionInterface	~line-272
class SecureCookieSessionInterface(SessionInterface):
    # ...
    session_class = SecureCookieSession
    # ...

# flask\sessions.py::SecureCookieSession	~line-109
class SecureCookieSession(CallbackDict, SessionMixin): 
    pass
```

-  https://blog.csdn.net/m0_37519490/article/details/80774069 



## SessionMixin

```python
class SessionMixin(object):
    """Expands a basic dictionary with an accessors that are expected
    by Flask extensions and users for the session.
    """
    def _get_permanent(self):
        return self.get('_permanent', False)
    def _set_permanent(self, value):
        self['_permanent'] = bool(value)
    permanent = property(_get_permanent, _set_permanent)
    del _get_permanent, _set_permanent

    new = False
    modified = True
```

## TaggedJSONSerializer

```python
class TaggedJSONSerializer(object):
    """A customized JSON serializer that supports a few extra types that
    we take for granted when serializing (tuples, markup objects, datetime).
    """
    pass
```

## SecureCookieSession

```python
class SecureCookieSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False
```

## NullSession

```python
class NullSession(SecureCookieSession):
    """Class used to generate nicer error messages if sessions are not
    available.  Will still allow read-only access to the empty session
    but fail on setting.
    """

    def _fail(self, *args, **kwargs):
        raise RuntimeError('the session is unavailable because no secret '
                           'key was set.  Set the secret_key on the '
                           'application to something unique and secret.')
    __setitem__ = __delitem__ = clear = pop = popitem = \
        update = setdefault = _fail
    del _fail
```

## SessionInterface

```python
class SessionInterface(object):
    null_session_class = NullSession
    pickle_based = False
    def make_null_session(self, app):
        return self.null_session_class()
    def is_null_session(self, obj):
        return isinstance(obj, self.null_session_class)
    def get_cookie_domain(self, app):
        # ....
    def get_cookie_path(self, app):
        # ....
    def get_cookie_httponly(self, app):
        # ....
    def get_cookie_secure(self, app):
        # ....
    def get_expiration_time(self, app, session):
        # ....

    def open_session(self, app, request):
        raise NotImplementedError()

    def save_session(self, app, session, response):
        raise NotImplementedError()
```

## SecureCookieSessionInterface

```python
class SecureCookieSessionInterface(SessionInterface):
    salt = 'cookie-session'
    digest_method = staticmethod(hashlib.sha1)
    key_derivation = 'hmac'
    serializer = session_json_serializer
    session_class = SecureCookieSession

    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = total_seconds(app.permanent_session_lifetime)
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
            return
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)
```





# signals.py

## flask信号机制

资源:

-  https://segmentfault.com/a/1190000002454953 
-  https://segmentfault.com/u/digwtx 

介绍:

- Flask框架中的信号基于 blinker，其主要就是让开发者可是在flask请求过程中定制一些用户行为。 

  - ```
    from blinker import Namespace
    ```

- 对扩展开发者:

  如果你正在编写一个Flask扩展，你想优雅地减少缺少Blinker安装的影响，你可以这样做使用`flask.signals.Namespace`类。

- 信号的操作:

  -  创建信号
  - 订阅信号
  - 发送信号 

flask 内置信号

```python
request_started = _signals.signal('request-started')                # 请求到来前执行
request_finished = _signals.signal('request-finished')              # 请求结束后执行
  
before_render_template = _signals.signal('before-render-template')  # 模板渲染前执行
template_rendered = _signals.signal('template-rendered')            # 模板渲染后执行

got_request_exception = _signals.signal('got-request-exception')    # 请求执行出现异常时执行

request_tearing_down = _signals.signal('request-tearing-down')      # 请求执行完毕后自动执行（无论成功与否）
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')# 请求上下文执行完毕后自动执行（无论成功与否）
  
appcontext_pushed = _signals.signal('appcontext-pushed')            # 请求上下文push时执行
appcontext_popped = _signals.signal('appcontext-popped')            # 请求上下文pop时执行
message_flashed = _signals.signal('message-flashed')                # 调用flask在其中添加数据时，自动触发
```



# templating.py

- 实现到 Jinja2 模板引擎的桥

```
Environment
DispatchingJinjaLoader
_render
render_template
render_template_string
```

## Environment

```python
# 继承自 jinja2  Environment as BaseEnvironment
class Environment(BaseEnvironment):
    """Works like a regular Jinja2 environment but has some additional
    knowledge of how Flask's blueprint works so that it can prepend the
    name of the blueprint to referenced templates if necessary.
    """

    def __init__(self, app, **options):
        if 'loader' not in options:
            options['loader'] = app.create_global_jinja_loader()
        BaseEnvironment.__init__(self, **options)
        self.app = app
```

## DispatchingJinjaLoader

```python
# 继承自 jinja2  BaseLoader
class DispatchingJinjaLoader(BaseLoader):
    """A loader that looks for templates in the application and all
    the blueprint folders.
    """
    pass
```

## _render

```python
def _render(template, context, app):
    """Renders the template and fires the signal"""
    rv = template.render(context)
    template_rendered.send(app, template=template, context=context)
    return rv
```

## render_template

```python
def render_template(template_name_or_list, **context):
    """Renders a template from the template folder with the given
    context.

    :param template_name_or_list: the name of the template to be
                                  rendered, or an iterable with template names
                                  the first one existing will be rendered
    :param context: the variables that should be available in the
                    context of the template.
    """
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.get_or_select_template(template_name_or_list),
                   context, ctx.app)
```

## render_template_string

```python
def render_template_string(source, **context):
    """Renders a template from the given template source string
    with the given context.

    :param source: the sourcecode of the template to be
                   rendered
    :param context: the variables that should be available in the
                    context of the template.
    """
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.from_string(source),
                   context, ctx.app)
```

# testing.py

```
make_test_environ_builder
FlaskClient
```

## make_test_environ_builder

## FlaskClient



# views.py

```
View
MethodViewType
MethodView
```

## MethodView

用法

```python
class CounterAPI(MethodView):

    def get(self):
        return session.get('counter', 0)

    def post(self):
        session['counter'] = session.get('counter', 0) + 1
        return 'OK'

app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))
```



# wrappers.py

```
Request
Response
```

## Request

## Response

