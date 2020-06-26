from flask import Blueprint

from flask_restful import Resource, marshal_with

from src.common.fields import login_fields
from src.common.reqparsers import parsers

# 创建蓝图对象
bp_session = Blueprint('session', __name__)


# 定义类视图
class SessionResource(Resource):

    @marshal_with(login_fields)
    def post(self):
        """Login.

        获取登录参数
        校验参数: 参数格式正确 -> 用户存在 -> 密码正确
        返回结果
        """

        args = parsers.login.parse_args(strict=True)
        print(args)
        return {'username': args['username']}


# 创建 API 对象, 使用 API 对象添加路由
# api = Api(bp_session)
# api.add_resource(SessionResource, '/session')
# 改到 urls.py 中添加路由

# 将蓝图注册到 app 中
# 在 app.py 中完成注册
