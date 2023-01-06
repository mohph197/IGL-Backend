from flask import Blueprint

bp = Blueprint("main", __name__)

# Announcements
from app.main.announcements.routes import bp as announcements_bp
bp.register_blueprint(announcements_bp, url_prefix="/announcements")

# Pictures
from app.main.pictures.routes import bp as pictures_bp
bp.register_blueprint(pictures_bp, url_prefix="/pictures")

# Messages
from app.main.discussions.routes import bp as messages_bp
bp.register_blueprint(messages_bp, url_prefix="/messages")

# Users
from app.main.users.routes import bp as users_bp
bp.register_blueprint(users_bp, url_prefix="/users")