from flask import Blueprint
from flask_restful import Resource

from src.common.method_decorators import authenticate
from src.common.reqparsers import parsers

bp_user = Blueprint('user', __name__)


# 3.定义类视图
class UserResource(Resource):

    method_decorators = [authenticate]

    def post(self):
        """Register a user.

        获取注册参数
        校验参数: 参数格式正确 -> 用户不存在 -> 两次密码一致
        保存用户
        返回结果
        """
        args = parsers.register.parse_args()
        return {
            'username': args['username'],
            'email': args['email'],
        }

    def get(self, user_id: str):
        """Get user info.

        获取请求参数
        校验参数: 已登录(带token) -> 参数格式正确 -> 用户存在
        查询用户数据
        返回结果
        """
        print(user_id)
        return {
            'username': 'Martin',
            'email': '18770915328@163.com',
            'avatar': 'xxx.jpg',
        }
