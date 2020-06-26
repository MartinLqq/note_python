from flask_restful import reqparse

from . import types

class ReqParsers:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not ReqParsers._instance:
            ReqParsers._instance = super().__new__(cls, *args, **kwargs)
        return ReqParsers._instance

    def __init__(self):
        self._parsers = {}

    @property
    def login(self):
        if self._parsers.get('login'):
            return self._parsers['login']
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', required=True, type=str, location='form'
        )
        parser.add_argument(
            'password', required=True, type=types.password_type, location='form'
        )
        self._parsers['login'] = parser
        return parser

    @property
    def register(self):
        if self._parsers.get('register'):
            return self._parsers['register']
        parser = self.login.copy()
        parser.add_argument(
            'password_confirm', required=True, type=types.password_type, location='form'
        )
        parser.add_argument(
            'email', required=True, location='form'
        )
        self._parsers['register'] = parser
        return parser


parsers = ReqParsers()

__all__ = ['parsers']
