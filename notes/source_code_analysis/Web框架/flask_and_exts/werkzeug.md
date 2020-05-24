# ==== werkzeug ====



# utils.py

## import_string

```python
def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).
    """
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if not silent:
            reraise(
                ImportStringError,
                ImportStringError(import_name, e),
                sys.exc_info()[2])
```



# local.py

资源:

- Werkzeug(Flask)之Local、LocalStack和LocalProxy:   https://www.jianshu.com/p/3f38b777a621 

介绍:

- local.py 定义上下文本地对象  (线程局部变量)

（1）Local->LocalStack，线程隔离对象实现

- Local内部有一个字典，以线程ID号作为key

- LocalStack如何实现？LocalStack封装了Local

- 操作Local，通常使用.去访问下面的属性；使用LocalStack，需要使用那几个常用的方法和属性，push、pop、top

（2）AppContext->RequestContext

- 请求进来，会被推入到LocalStack的栈中去，同时在请求结束时，AppContext和RequestContext会被pop弹出去

（3）Flask->AppContext Request->RequestContext

- AppContext重要特点，将Flask核心对象作为它的一个属性，保存了起来

- RequestContext请求上下文，将请求对象Request封装和保存

（4）current_app->(LocalStack.top=Appcontext top.app=Flask)

- current_app指向的是LocalStack下面的栈顶元素的一个属性，也就是top.app，Flask的核心对象

- 栈顶元素为应用上下文

（5）request->(LocalStack.top=RequestContext top.request=Request)

- request实际指向的是LocalStack栈顶元素下面的Request请求对象

![img](https://images2018.cnblogs.com/blog/1426593/201807/1426593-20180726162909503-2066003195.png)



## Local

-   基于线程存储全局变量 ,  通过这种方式存储的数据只在本线程中有效，而对于其它线程则不可见 

Local 的定义:

```python
class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        # __storage__字典的 key 为线程ID号. 值为该线程下赋给 Local 对象的属性字典
        # 从开头的模块导入可以看出: 当有greenlet时使用greenlet id，没有则使用thread id
        object.__setattr__(self, '__storage__', {})
        # # _thred.get_ident() 获取当前线程ID号, 是一个非零整数.
        object.__setattr__(self, '__ident_func__', get_ident)

    def __iter__(self):
        # 此方法可以访问到所有线程下赋给 Local 对象的所有属性
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
```

测试 Local:

```python
from werkzeug.local import Local, release_local
import threading

loc = Local()
loc.foo = 123
loc.bar = 456
print(loc.__storage__)  # 此时只有一个线程, 打印结果如: {12852: {'foo': 123, 'bar': 456}}

th = threading.Thread(
    target=lambda loc: setattr(loc, 'my_demo', 789), args=(loc,)
)
th.start()

print(loc.__storage__)  
# 此时有两个线程, 且子线程向loc中增加了属性, 打印结果如: 
# {12852: {'foo': 123, 'bar': 456}, 15040: {'my_demo': 789}}

release_local(loc)
print(loc.__storage__) 
# 此时主线程对应的键值对被释放, 打印结果如: {16228: {'my_demo': 789}}
```



## LocalStack

- 线程局部变量堆栈
- LocalStack在Flask框架中频繁出现，其 Request Context 和 App Context 的实现都是基于LocalStack 

```python
class LocalStack(object):
    """This class works similar to a :class:`Local` but keeps a stack
    of objects instead.  This is best explained with an example::

        >>> ls = LocalStack()
        >>> ls.push(42)
        >>> ls.top
        42
        >>> ls.push(23)
        >>> ls.top
        23
        >>> ls.pop()
        23
        >>> ls.top
        42

    They can be force released by using a :class:`LocalManager` or with
    the :func:`release_local` function but the correct way is to pop the
    item from the stack after using.  When the stack is empty it will
    no longer be bound to the current context (and as such released).

    By calling the stack without arguments it returns a proxy that resolves to
    the topmost item on the stack.

    .. versionadded:: 0.6.1
    """
    def __init__(self):
        self._local = Local()

    def __release_local__(self):
        self._local.__release_local__()

    def _get__ident_func__(self):
        return self._local.__ident_func__

    def _set__ident_func__(self, value):
        object.__setattr__(self._local, '__ident_func__', value)
    __ident_func__ = property(_get__ident_func__, _set__ident_func__)
    del _get__ident_func__, _set__ident_func__

    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError('object unbound')
            return rv
        return LocalProxy(_lookup)

    def push(self, obj):
        rv = getattr(self._local, 'stack', None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(obj)
        return rv

    def pop(self):
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return None
        elif len(stack) == 1:
            release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()

    @property
    def top(self):

        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None
```



## LocalManager

- 首先 Local 对象需要通过 LocalManager 来管理，初次生成 LocalManager 对象需要传一个 list 类型的参数，list 中是 Local 对象，当有新的 Local 对象时，可以通过`local_manager.locals.append()`来添加。而当 LocalManager 对象清理的时候会将所有存储于locals中的当前 context 的数据都清理掉

```python
class LocalManager(object):
    """Local objects cannot manage themselves. For that you need a local
    manager.  You can pass a local manager multiple locals or add them later
    by appending them to `manager.locals`.  Every time the manager cleans up,
    it will clean up all the data left in the locals for this context.

    The `ident_func` parameter can be added to override the default ident
    function for the wrapped locals.
    """
    def __init__(self, locals=None, ident_func=None):
        if locals is None:
            self.locals = []
        elif isinstance(locals, Local):
            self.locals = [locals]
        else:
            self.locals = list(locals)
        if ident_func is not None:
            self.ident_func = ident_func
            for local in self.locals:
                object.__setattr__(local, '__ident_func__', ident_func)
        else:
            self.ident_func = get_ident

    def get_ident(self):
        return self.ident_func()

    def cleanup(self):
        """Manually clean up the data in the locals for this context.  Call
        this at the end of the request or use `make_middleware()`.
        """
        for local in self.locals:
            release_local(local)

    def make_middleware(self, app):
        """Wrap a WSGI application so that cleaning up happens after
        request end.
        """
        def application(environ, start_response):
            return ClosingIterator(app(environ, start_response), self.cleanup)
        return application

    def middleware(self, func):
        """Like `make_middleware` but for decorating functions.

        Example usage::

            @manager.middleware
            def application(environ, start_response):
                ...

        The difference to `make_middleware` is that the function passed
        will have all the arguments copied from the inner application
        (name, docstring, module).
        """
        return update_wrapper(self.make_middleware(func), func)

    def __repr__(self):
        return '<%s storages: %d>' % (
            self.__class__.__name__,
            len(self.locals)
        )
```



## LocalProxy

- LocalProxy 用于代理 Local 对象和 LocalStack 对象，作为中间的代理人来处理所有针对被代理对象的操作 

初始化LocalProxy有三种方式：

1. 通过Local或者LocalStack对象的`__call__` method

```python
from werkzeug.local import Local
lo = Local()

# these are proxies
request = lo('request')
user = lo('user')


from werkzeug.local import LocalStack
_response_local = LocalStack()

# this is a proxy
response = _response_local()
```

上述代码直接将对象像函数一样调用，这是因为Local和LocalStack都实现了`__call__` method，这样其对象就是callable的，因此当我们将对象作为函数调用时，实际调用的是`__call__` method，可以看下本文开头部分的Local的源代码，会发现`__call__` method会返回一个LocalProxy对象

2. 通过LocalProxy类进行初始化

```python
lo = Local()
request = LocalProxy(lo, 'request')
```

实际上这段代码跟第一种方式是等价的，但这种方式是最'原始'的方式，我们在Local的源代码实现中看到其`__call__` method就是通过这种方式生成LocalProxy的

3. 使用 callable 对象作为参数

```python
request = LocalProxy(get_current_request())
```



## > flask 上下文的实现

- https://segmentfault.com/a/1190000004223296

## > 复制上下文到后台线程

```python
@app.route('/multi_threads')
def multi_threads_out_of_ctx():
    @copy_current_request_context
    def background_task():
        print(request.method)

    from threading import Thread
    th = Thread(target=background_task)
    th.start()
    # th.join()
    return 'multi_threads done'
```

# datastructures.py

## 接口概览

> immutable:   不可变的

```
is_immutable
iter_multi_items
native_itermethods
ImmutableListMixin
ImmutableList
ImmutableDictMixin
ImmutableMultiDictMixin
UpdateDictMixin
TypeConversionDict
ImmutableTypeConversionDict
ViewItems
MultiDict
OrderedMultiDict
Headers
ImmutableHeadersMixin
EnvironHeaders
CombinedMultiDict
FileMultiDict
ImmutableDict
ImmutableMultiDict
ImmutableOrderedMultiDict
Accept
MIMEAccept
LanguageAccept
CharsetAccept
cache_property
_CacheControl
RequestCacheControl
ResponseCacheControl
CallbackDict
HeaderSet
ETags
IfRange
Range
ContentRange
Authorization
WWWAuthenticate
FileStorage
```

## ImmutableList

- 不可变  列表

## TypeConversionDict

- 自动转换类型  字典

```python
class TypeConversionDict(dict):
    """Works like a regular dict but the :meth:`get` method can perform
    type conversions.  :class:`MultiDict` and :class:`CombinedMultiDict`
    are subclasses of this class and provide the same feature.
    """
    def get(self, key, default=None, type=None):
        """
        >>> d = TypeConversionDict(foo='42', bar='blub')
        >>> d.get('foo', type=int)
        42
        >>> d.get('bar', -1, type=int)
        -1
        """
        try:
            rv = self[key]
        except KeyError:
            return default
        if type is not None:
            try:
                rv = type(rv)
            except ValueError:
                rv = default
        return rv
```

## ImmutableTypeConversionDict

- 不可变  自动转换类型  字典

## MultiDict

- 多值  字典

```python
# md = MultiDict()
# md = MultiDict([('a', 1), ('a', 2)])
# md = MultiDict(MultiDict({'a': [1, 2]}))
md = MultiDict({'a': [1, 2]})
print(md.get('a'))      # 1
print(md.getlist('a'))  # [1, 2]
```

## OrderedMultiDict

- 有序  多值  字典

## CombinedMultiDict

- 不可变  联合  多值  字典

```python
>>> from werkzeug.datastructures import CombinedMultiDict, MultiDict
>>> post = MultiDict([('foo', 'bar')])
>>> get = MultiDict([('blub', 'blah')])
>>> combined = CombinedMultiDict([get, post])
>>> combined['foo']
'bar'
>>> combined['blub']
'blah'
```

## FileMultiDict

- 文件  多值  字典

## ImmutableDict

- 不可变  字典

## ImmutableMultiDict

- 不可变  多值  字典

## ImmutableOrderedMultiDict

- 不可变  有序  多值  字典

## cache_property

```python
def cache_property(key, empty, type):
    """Return a new property object for a cache header.  Useful if you
    want to add support for a cache extension in a subclass."""
    return property(lambda x: x._get_cache_value(key, empty, type),
                    lambda x, v: x._set_cache_value(key, v, type),
                    lambda x: x._del_cache_value(key),
                    'accessor for %r' % key)
```



## CallbackDict

- CallbackDict 字典的内容发生改变时,  调用指定的回调函数

```python
class CallbackDict(UpdateDictMixin, dict):
    """A dict that calls a function passed every time something is changed.
    The function is passed the dict instance.
    """
    def __init__(self, initial=None, on_update=None):
        dict.__init__(self, initial or ())
        self.on_update = on_update

    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            dict.__repr__(self)
        )
```





## 示例: CombinedMultiDict、MultiDict

post提交时提交 json 数据,  在flask应用中使用 flask_wtf 插件的表单来 校验 json请求数据

```python
from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from werkzeug.datastructures import CombinedMultiDict, MultiDict
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.secret_key = 'something_secret'
app.config['WTF_CSRF_ENABLED'] = False


class RegisterForm(FlaskForm):
    username = StringField("用户名：", validators=[DataRequired("请输入用户名")])
    password = PasswordField("密码：", validators=[DataRequired("请输入密码")])
    password2 = PasswordField("确认密码：", validators=[DataRequired("请输入确认密码"), EqualTo("password", "两次密码不一致")])
    # submit = SubmitField("注册")


@app.route('/register', methods=['POST'])
def register():
    print(request.json)
    # =========== 注意此用法 ===========
    # RegisterForm, CombinedMultiDict, MultiDict
    form = RegisterForm(CombinedMultiDict([MultiDict(request.json)]))
    if form.validate():
        return jsonify({'code': 2000, 'message': '校验通过, 执行注册...'})
    # 校验失败, 通过 form.errors 获取失败信息
    print(form.errors)
    return jsonify({'error_code': 4000, 'error_msg': form.errors})


if __name__ == '__main__':
    app.run(debug=True)
```


