from flask import Blueprint
from app.main.announcements.utils import *

bp = Blueprint("announcements", __name__)

@bp.get("/")
def index_route():
    return index()

@bp.get("/<int:announcement_id>")
def announcement_route(announcement_id):
    return announcement(announcement_id)

@bp.post("/create")
def create_announcement_route():
    return create_announcement()

@bp.patch("/<int:announcement_id>/edit")
def edit_announcement_route(announcement_id):
    return edit_announcement(announcement_id)

@bp.delete("/<int:announcement_id>/delete")
def delete_announcement_route(announcement_id):
    return delete_announcement(announcement_id)