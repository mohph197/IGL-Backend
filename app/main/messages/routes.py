from flask import Blueprint
from app.main.messages.utils import *

bp = Blueprint("messages", __name__)

@bp.get("/sent")
def index_sent_route():
    return index_sent()

@bp.get("/received")
def index_received_route():
    return index_received()

@bp.get("/sent/<int:message_id>")
def message_sent_route(message_id):
    return message_sent(message_id)

@bp.get("/received/<int:message_id>")
def message_received_route(message_id):
    return message_received(message_id)