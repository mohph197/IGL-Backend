from flask import Blueprint
from app.main.locations.utils import *

bp = Blueprint("locations", __name__)

@bp.get("/get-communes/<string:wilaya>")
def get_communes_route(wilaya):
    return get_communes(wilaya)