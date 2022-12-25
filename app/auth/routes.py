from flask import Blueprint
from app.auth.utils import *

bp = Blueprint("auth", __name__)

@bp.route("/",methods=['POST'])
def auth_route():
    return auth()

@bp.route("/me")
def me_route():
    return me()