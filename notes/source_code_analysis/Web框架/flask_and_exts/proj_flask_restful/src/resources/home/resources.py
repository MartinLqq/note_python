from flask import Blueprint

# 1.创建蓝图对象
from flask_restful import Api, Resource

from src.common.exceptions import DemoError

bp_home = Blueprint('home', __name__)
# 2.使用 Api 对象接管蓝图
api = Api(bp_home)


# 3.定义类视图
class Home(Resource):
    def get(self):

        raise DemoError

        return {'status': 2000, 'data': 'home'}


# 4.使用 API 对象添加路由
# 改到 routes.py 中添加路由

# 5.将蓝图注册到 app 中
# 在 app.py 中完成注册
