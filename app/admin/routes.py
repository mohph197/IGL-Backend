from flask import Blueprint
from app.admin.utils import *

bp = Blueprint("admin", __name__)

@bp.get('/get_online')
def get_online_route():
    return get_online()