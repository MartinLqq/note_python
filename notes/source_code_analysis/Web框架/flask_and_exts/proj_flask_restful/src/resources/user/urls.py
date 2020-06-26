from .resources import UserResource

urls = [
    {'resource': UserResource, 'urls': ['/<string:user_id>', '/']}
]
