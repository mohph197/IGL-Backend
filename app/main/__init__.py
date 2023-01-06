from flask import request
from app.models import *
from app import login_is_required

def get_auth_user() -> User:
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return None
    bearer_token = authorization_header.split(' ')[1]
    login_info = login_is_required(bearer_token)
    if not login_info:
        return None
    return User.query.get(login_info["email"])

def get_socket_user(token) -> User:
    login_info = login_is_required(token)
    if not login_info:
        return None
    return User.query.get(login_info["email"])