from flask_restful import reqparse
from . import types

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True, type=str)
login_parser.add_argument('password', required=True, type=types.password_type)
