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
