from flask import Blueprint

bp = Blueprint("main", __name__)

# Announcements
from app.main.announcements.routes import bp as announcements_bp
bp.register_blueprint(announcements_bp, url_prefix="/announcements")