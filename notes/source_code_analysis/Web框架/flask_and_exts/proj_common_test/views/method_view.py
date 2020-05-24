from flask.views import MethodView

class MyView(MethodView):

    def get(self):
        return 'MethodView-get'

    def post(self):
        return 'MethodView-post'
