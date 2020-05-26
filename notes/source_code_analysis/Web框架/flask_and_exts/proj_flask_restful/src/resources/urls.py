from . import auth, home, profile


routes = [
    {
        'bp': auth.bp_auth,
        'api': auth.api,
        'prefix': '/auth',
        'urls': auth.urls
    },
    {
        'bp': home.bp_home,
        'api': home.api,
        'prefix': '/',
        'urls': home.urls
    },
    {
        'bp': profile.bp_profile,
        'api': profile.api,
        'prefix': '/profile',
        'urls': profile.urls
    },
]


def add_routes():
    for route in routes:
        route['bp'].url_prefix = route['prefix']
        for item in route['urls']:
            route['api'].add_resource(item['resource'], item['url'])
