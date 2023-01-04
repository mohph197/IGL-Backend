import os
from flask import Flask,session,abort,request
from app.models import *
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import jwt

db = SQLAlchemy()

def login_is_required(token):  #a function to check if the user is authorized or not
    try:
        decoded = jwt.decode(token,os.environ['SECRET_KEY'],os.environ['JWT_ALGORITHM'])
        return decoded
    except:
        return None

def get_auth_user():
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return None
    bearer_token = authorization_header.split(' ')[1]
    login_info = login_is_required(bearer_token)
    if not login_info:
        return None
    return User.query.get(login_info["email"])

def create_app():
    load_dotenv()

    app = Flask("TP_IGL")  # Naming our application
    app.secret_key = os.environ['SECRET_KEY']  #It is necessary to set a password when dealing with OAuth 2.0
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['UPLOAD_FOLDER'] = 'storage/pictures'
    CORS(app)
    
    db.init_app(app)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin.routes import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app