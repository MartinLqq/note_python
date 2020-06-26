# ==== flask-restful ====

看这个就够了:   0.3.1 中文问文档   http://www.pythondoc.com/Flask-RESTful/index.html 



# 概览

```python
# Resource
    restful.Resource   # 类视图的父类
    method_decorators  # 类属性, 指定资源方法装饰器
    
# Api
    restful.Api()
    api.add_resource()
    @api.representation()  # 自定义响应格式
    
# RequestParser
    restful.reqparse.RequestParser()
    parser.add_argument()   # 传 Argument 类实例化参数
    # 自定义校验规则: parser.add_argument(type=my_func)
    parser.parse_args()
    parser.copy()
    parser.replace_argument()
    parser.remove_argument()
    
# fields: 数据格式化
    restful.fields.XXX
    marshal()
    @marshal_with(xx_fields)
    @marshal_with_field(field)
    
    
# 错误处理
    # a.自定义错误处理器, 使 Flask-RESTful 处理除了自己路由上的错误还有应用程序上所有的 404 错误
    api = flask_restful.Api(app, catch_all_404s=True)

    # b.使用 flask 信号处理异常
    def log_exception(sender, exception, **extra):
        """ Log an exception to our logging framework """
        sender.logger.debug('Got exception during processing: %s', exception)

    flask.got_request_exception.connect(log_exception, app)

    # c.定义自定义错误消息
    errors = {
        'UserAlreadyExistsError': {
            'message': "A user with that username already exists.",
            'status': 409,
        },
    }
    api = flask_restful.Api(app, errors=errors)
    
    # d.使用 flask 的 @app.errorhandler(xxx)


# 配合 BluePrint 使用
    from flask import Flask, Blueprint
    from flask_restful import Api, Resource
    app = Flask(__name__)

    # 1.创建蓝图对象
    bp_index = Blueprint('flask_blueprint', __name__)
    # 2.使用 Api 对象接管蓝图
    api = Api(bp_index)

    # 3.定义类视图
    class IndexResource(Resource):
        def get(self): return 'index'
    # 4.使用API对象添加路由
    api.add_resource(IndexResource, '/')
    # 5.将蓝图注册到app中
    app.register_blueprint(bp_index)
```





一个最小的 Flask-RESTful API:

```python
# from flask.ext import restful
import flask_restful as restful
from flask import Flask

app = Flask(__name__)
api = restful.Api(app)

class UserInfo(restful.Resource):
    """UserInfo API."""
    def get(self):
        data = {'username': 'Martin'}
        return {'status': 2000, 'data': data}
    def post(self):
        return {'status': 2000, 'data': 'userinfo changed'}

api.add_resource(UserInfo, '/userinfo')


if __name__ == '__main__':
    app.run(debug=True)

"""
api tests:
    $ curl http://127.0.0.1:5000/userinfo -X get -s
    $ curl http://127.0.0.1:5000/userinfo -X post -s
"""
```

# \_\_init__.py

## Api

Api 类是 flask_restful 应用程序的主入口,  可以在实例化时传入 flask.Flask or flask.Blueprint 对象 (app),  也可以调用 Api::init_app 方法初始化 app.

一些接口:

```
init_app
add_resource
resource
url_for
make_response
app
blueprint
endpoints
prefix
urls
```



## Resource

```
dispatch_request
method_decorators
representations
```



## marshal

- 主要用于被 marshal_with 和 marshal_with_field 调用,  用来进行  格式化和过滤响应 

```python
def marshal(data, fields, envelope=None):
    """
    >>> from flask_restful import fields, marshal
    >>> data = { 'a': 100, 'b': 'foo' }
    >>> mfields = { 'a': fields.Raw }

    >>> marshal(data, mfields)
    OrderedDict([('a', 100)])

    >>> marshal(data, mfields, envelope='data')
    OrderedDict([('data', OrderedDict([('a', 100)]))])

    """
    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    if isinstance(data, (list, tuple)):
        return (OrderedDict([(envelope, [marshal(d, fields) for d in data])])
                if envelope else [marshal(d, fields) for d in data])

    items = ((k, marshal(data, v) if isinstance(v, dict)
              else make(v).output(k, data))
             for k, v in fields.items())
    return OrderedDict([(envelope, OrderedDict(items))]) if envelope else OrderedDict(items)

```

## @marshal_with()

- marshal:  安排,  组织
- 重新组织响应内容,  格式化和过滤响应 

```python
class marshal_with(object):
    """A decorator that apply marshalling to the return values of your methods.

    >>> from flask_restful import fields, marshal_with
    >>> mfields = { 'a': fields.Raw }
    >>> @marshal_with(mfields)
    ... def get():
    ...     return { 'a': 100, 'b': 'foo' }
    ...
    >>> get()
    OrderedDict([('a', 100)])

    >>> @marshal_with(mfields, envelope='data')
    ... def get():
    ...     return { 'a': 100, 'b': 'foo' }
    ...
    >>> get()
    OrderedDict([('data', OrderedDict([('a', 100)]))])
    """
    def __init__(self, fields, envelope=None):
        """
        :param fields: a dict of whose keys will make up the final
                       serialized response output
        :param envelope: optional key that will be used to envelop the serialized
                         response
        """
        self.fields = fields
        self.envelope = envelope

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)
            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return marshal(data, self.fields, self.envelope), code, headers
            else:
                return marshal(resp, self.fields, self.envelope)
        return wrapper
```



## @marshal_with_field()

```python
class marshal_with_field(object):
    """
    A decorator that formats the return values of your methods with a single field.

    >>> from flask_restful import marshal_with_field, fields
    >>> @marshal_with_field(fields.List(fields.Integer))
    ... def get():
    ...     return ['1', 2, 3.0]
    ...
    >>> get()
    [1, 2, 3]

    see :meth:`flask_restful.marshal_with`
    """
    def __init__(self, field):
        """
        :param field: a single field with which to marshal the output.
        """
        if isinstance(field, type):
            self.field = field()
        else:
            self.field = field

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)

            if isinstance(resp, tuple):
                data, code, headers = unpack(resp)
                return self.field.format(data), code, headers
            return self.field.format(resp)

        return wrapper
```





# reqparse.py

```
Namespace
text_type
Argument
RequestParser
```

## Argument

## RequestParser









