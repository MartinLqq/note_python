# from flask.ext import restful
import flask_restful as restful
from flask_restful import reqparse
from flask import Flask

app = Flask(__name__)
module_user = restful.Api(app, prefix='/user')
module_comments = restful.Api(app, prefix='/comments')

USERINFO = {}


class UserInfo(restful.Resource):
    """UserInfo API."""

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        args = parser.parse_args()
        info = {'username': USERINFO[args['username']],
                "age": USERINFO[args['username']]}
        return {'status': 2000, 'data': info}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', help='Username string.', trim=True, required=True
        )
        parser.add_argument(
            'age', type=int, help='Age of the user must be int.', required=True
        )
        args = parser.parse_args()
        info = {args['username']: args['age']}
        USERINFO.update(info)
        print(USERINFO)
        return {'status': 2000, 'data': info}


class Comments(restful.Resource):
    """Comments."""
    def get(self):
        data = ['comments...']
        return {'status': 2000, 'data': data}


module_user.add_resource(UserInfo, '/info')
module_comments.add_resource(Comments, '/list')


if __name__ == '__main__':
    app.run(debug=True)
