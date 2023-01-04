from app.models import *
from flask import jsonify, send_file

def serve_image(picture_id):
    picture = Picture.query.get(picture_id)
    if not picture:
        return jsonify({
            "error":"Picture not found",
            "message":"Error"
        }),404
    return send_file(picture.chemin)