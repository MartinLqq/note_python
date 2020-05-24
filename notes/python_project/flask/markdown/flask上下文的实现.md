# [flask 上下文的实现](https://segmentfault.com/a/1190000004223296)

6.1k 次阅读  ·  读完需要 8 分钟

### 引言

本文主要梳理了flask的current_app, request, session, g的实现原理

### 源码说明

本文使用flask 0.5 版本

### application context 和request context

*flask*有两个context: `application context`和`request context`

| application context | request context |
| ------------------- | --------------- |
| current_app         | request         |
| g                   | session         |

这里需要通俗地解释一下**application context**与**request context**：

1. *application* 指的就是当你调用`app = Flask(__name__)`创建的这个对象`app`；
2. *request* 指的是每次`http`请求发生时，`WSGI server`(比如gunicorn)调用`Flask.__call__()`之后，在`Flask`对象内部创建的`Request`对象；
3. *application* 表示用于响应WSGI请求的应用本身，*request* 表示每次http请求；
4. *application*的生命周期大于*request*，一个*application*存活期间，可能发生多次http请求，所以，也就会有多个*request*

下面通过源码了解一下 **flask** 如何实现这两种context：

```
# 代码摘选自flask 0.5 中的ctx.py文件, 进行了部分删减
class _RequestContext(object):
    
    def __init__(self, app, environ):
        self.app = app
        self.request = app.request_class(environ)
        self.session = app.open_session(self.request)
        self.g = _RequestGlobals()
```

**flask** 使用`_RequestContext`的代码如下：

```
class Flask(object):

    def request_context(self, environ):
        return _RequestContext(self, environ)
```

在`Flask`类中，每次请求都会调用这个`request_context`函数。这个函数则会创建一个`_RequestContext`对象。

值得注意的是：这个对象在创建时，将`Flask`实例的本身作为实参传入`_RequestContext`自身，因此，
`self.app = Flask()`。

所以，虽然每次http请求都会创建一个`_RequestContext`对象，但是，每次创建的时候都会将同一个`Flask`对象传入该对象的`app`成员变量，使得：

> 由同一个`Flask`对象响应的请求所创建的`_RequestContext`对象的`app`成员变量都共享同一个**application**

通过在`Flask`对象中创建`_RequestContext`对象，并将`Flask`自身作为参数传入`_RequestContext`对象的方式，实现了多个**request context**对应一个**application context** 的目的。

接下来，看`self.request = app.request_class(environ)`这句。
由于`app`成员变量就是`app = Flask(__name__)`这个对象，所以，`app.request_class`就是`Flask.request_class`。
在`Flask`类的定义中：

```
request_class = Request # Request 是一个类，定义如下：

class Request(RequestBase):
    ...
```

所以：
`self.request = app.request_class(environ)`实际上是创建了一个`Request`对象。
由于，一个http请求对应一个`_RequestContext`对象的创建，而每个`_RequestContext`对象的创建对应一个`Request`对象的创建，所以，每个http请求对应一个`Request`对象。

到这里想必已经很清楚了：

**application** 就是指`app = Flask(__name__)`对象
**request** 就是对应每次http 请求创建的`Request`对象
**flask**通过`_RequestContext`将`app`与`Request`关联起来

### 总结

1. `app = Flask(__name__)`创建了application， 这个application对应的上下文，就是**application context**
2. `Flask`每响应一个http请求，就会创建一个`Request`对象，这个request对象对应的上下文，就是**request context**