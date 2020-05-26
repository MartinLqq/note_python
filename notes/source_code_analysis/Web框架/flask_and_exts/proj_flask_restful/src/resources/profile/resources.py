from flask import Blueprint

# 1.创建蓝图对象
from flask_restful import Api, Resource

from src.common.method_decorators import authenticate

bp_profile = Blueprint('profile', __name__)
# 2.使用 Api 对象接管蓝图
api = Api(bp_profile)


# 3.定义类视图
class Profile(Resource):

    method_decorators = [authenticate]

    def get(self):
        data = {
            'username': 'Martin',
            'email': '18770915328@163.com',
            'avatar': 'xxx.jpg',
        }
        return {'status': 2000, 'data': data}


# 4.使用 API 对象添加路由
# api.add_resource(Login, '/login')
# 改到 routes.py 中添加路由

# 5.将蓝图注册到 app 中
# 在 app.py 中完成注册
