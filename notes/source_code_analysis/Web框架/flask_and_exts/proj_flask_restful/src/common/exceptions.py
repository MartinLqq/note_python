class RestError(Exception):
    message = 'rest error'
    code = '000000'


class DemoError(RestError):
    message = 'demo error'
    code = '100001'
