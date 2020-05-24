from flask import Blueprint

BP_USER = Blueprint('user', __name__, url_prefix='/users')

from . import views
