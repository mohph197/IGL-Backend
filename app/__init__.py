import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask("TP_IGL")  # Naming our application
    app.secret_key = "TP_IGL"  #It is necessary to set a password when dealing with OAuth 2.0
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")


    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin.routes import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app