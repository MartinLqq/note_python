import falcon

class HelloResource:

    def on_get(self, req, resp):

        resp.status = falcon.HTTP_200
        resp.body = 'hello world\n'


app = falcon.App()
app.add_route('/', HelloResource())
