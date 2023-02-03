from flask import Blueprint
from app.admin.utils import *

bp = Blueprint("admin", __name__)

@bp.get('/get-online')
def get_online_route():
    return get_online()

@bp.get('/get-users')
def get_users_route():
    return get_users()