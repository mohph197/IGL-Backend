from flask import Blueprint
from app.main.discussions.utils import *

bp = Blueprint("discussions", __name__)

@bp.get("/sent")
def index_sent_route():
    return index_sent()

@bp.get("/received")
def index_received_route():
    return index_received()

@bp.get("/sent/<int:discussion_id>")
def message_sent_route(discussion_id):
    return discussion_sent(discussion_id)

@bp.get("/received/<int:discussion_id>")
def message_received_route(discussion_id):
    return discussion_received(discussion_id)