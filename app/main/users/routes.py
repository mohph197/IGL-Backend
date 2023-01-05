from flask import Blueprint
from app.main.users.utils import *

bp = Blueprint("users", __name__)

@bp.put("/edit-contacts")
def contacts_route():
    return contacts()