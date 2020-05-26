from flask import Blueprint, request

# 1.创建蓝图对象
from flask_restful import Api, Resource, marshal_with

from src.common.fields import auth_fields
from src.common.reqparsers import login_parser

bp_auth = Blueprint('auth', __name__)
# 2.使用 Api 对象接管蓝图
api = Api(bp_auth)


# 3.定义类视图
class Login(Resource):

    @marshal_with(auth_fields)
    def get(self):
        args = login_parser.parse_args()
        print(args)
        return {'username': args['username'], 'xxx': 'yyy'}


# 4.使用 API 对象添加路由
# api.add_resource(Login, '/login')
# 改到 routes.py 中添加路由

# 5.将蓝图注册到 app 中
# 在 app.py 中完成注册
