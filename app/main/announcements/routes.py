from flask import Blueprint
from app.main.announcements.utils import *

bp = Blueprint("announcements", __name__)

@bp.get("/")
def index_route():
    return index()

@bp.get('/all')
def all_announcements_route():
    return all_announcements()

@bp.get("/<int:announcement_id>")
def announcement_route(announcement_id):
    return announcement(announcement_id)

@bp.post("/create")
def create_announcement_route():
    return create_announcement()

@bp.delete("/<int:announcement_id>/delete")
def delete_announcement_route(announcement_id):
    return delete_announcement(announcement_id)

@bp.get("/search")
def search_route():
    return search()

@bp.get("/filter")
def filter_route():
    return filter()