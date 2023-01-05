from flask import request
from app.models import *
from app import login_is_required

annonces_algerie_url = "http://www.annonce-algerie.com/"

def get_auth_admin() -> User:
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return None
    bearer_token = authorization_header.split(' ')[1]
    login_info = login_is_required(bearer_token)
    if not login_info:
        return None
    
    user = User.query.get(login_info["email"])
    if user:
        if user.role == 'A':
            return user
        else:
            return None
    else:
        return None