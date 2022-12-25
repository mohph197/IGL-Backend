from flask import Blueprint
from app.auth.utils import *

bp = Blueprint("auth", __name__)

@bp.route("/",methods=['POST'])
def auth_route():
    return new_auth()

@bp.route("/me")
def me_route():
    return me()

@bp.route("/callback")
def callback_route():
    return callback()

@bp.route("/logout")
def logout_route():
    return logout()