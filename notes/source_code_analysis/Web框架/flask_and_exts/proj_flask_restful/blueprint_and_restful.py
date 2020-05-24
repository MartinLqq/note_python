from flask import Flask, Blueprint
from flask_restful import Api, Resource


app = Flask(__name__)

# 1.创建蓝图对象
bp_index = Blueprint('flask_blueprint', __name__)
# 2.使用 Api 对象接管蓝图
api = Api(bp_index)


# 3.定义类视图
class IndexResource(Resource):
    def get(self):
        return 'index'

# 4.使用API对象添加路由
api.add_resource(IndexResource, '/')

# 5.将蓝图注册到app中
app.register_blueprint(bp_index)


if __name__ == '__main__':
    app.run()