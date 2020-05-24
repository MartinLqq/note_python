from flask import Flask
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)


# 2. 定义装饰器
def outter(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        return '{} decorators....'.format(ret)
    return inner


# 1. 定义类视图,并设置路由
class IndexResource(Resource):

    # 为所有请求方法都添加装饰器
    # method_decorators = [outter]

    # 为指定方法添加装饰器
    method_decorators = {
        'get': [outter]
    }

    def get(self):
        return 'get ...'

    def post(self):
        return 'post ...'

api.add_resource(IndexResource, '/')

if __name__ == '__main__':
    app.run(debug=True)
