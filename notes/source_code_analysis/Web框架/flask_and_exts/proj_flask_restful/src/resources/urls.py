from flask_restful import Api

from . import session, user


urls = [
    {
        'bp': session.bp_session,
        'prefix': '/api/v1/session', 'urls': session.urls
    },
    {
        'bp': user.bp_user,
        'prefix': '/api/v1/user', 'urls': user.urls
    },
]


def add_routes():
    for route in urls:
        route['bp'].url_prefix = route['prefix']
        for item in route['urls']:
            # 使用 Api 对象接管蓝图, 向Api 对象添加 resource
            Api(route['bp']).add_resource(item['resource'], *item['urls'])
