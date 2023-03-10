from flask import Blueprint

bp = Blueprint("main", __name__)

# Announcements
from app.main.announcements.routes import bp as announcements_bp
bp.register_blueprint(announcements_bp, url_prefix="/announcements")

# Pictures
from app.main.pictures.routes import bp as pictures_bp
bp.register_blueprint(pictures_bp, url_prefix="/pictures")

# Discussions
from app.main.discussions.routes import bp as discussions_bp
bp.register_blueprint(discussions_bp, url_prefix="/discussions")

# Users
from app.main.users.routes import bp as users_bp
bp.register_blueprint(users_bp, url_prefix="/users")

# Locations
from app.main.locations.routes import bp as locations_bp
bp.register_blueprint(locations_bp, url_prefix="/locations")