import os
from flask import Flask,session,abort
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

def create_app():
    load_dotenv()

    app = Flask("TP_IGL")  # Naming our application
    app.secret_key = os.environ['SECRET_KEY']  #It is necessary to set a password when dealing with OAuth 2.0
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    CORS(app)
    
    db.init_app(app)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin.routes import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app