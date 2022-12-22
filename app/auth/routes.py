from flask import Blueprint
from app.auth.utils import auth, callback, logout

bp = Blueprint("auth", __name__)

@bp.route("/")
def auth_route():
    return auth()

@bp.route("/callback")
def callback_route():
    return callback()

@bp.route("/logout")
def logout_route():
    return logout()