from flask import Blueprint
from app.main.pictures.utils import *

bp = Blueprint("pictures", __name__)

@bp.get('/<int:picture_id>')
def serve_image_route(picture_id):
    return serve_image(picture_id)