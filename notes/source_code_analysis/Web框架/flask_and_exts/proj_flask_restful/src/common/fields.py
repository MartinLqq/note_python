import random

from flask_restful import fields


class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()


login_fields = {
    'username': fields.String,
    'random_str': RandomNumber
}
