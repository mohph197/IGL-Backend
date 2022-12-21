from flask import Flask

def create_app():
    app = Flask("TP_IGL")  # Naming our application
    app.secret_key = "TP_IGL"  #It is necessary to set a password when dealing with OAuth 2.0

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin.routes import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app