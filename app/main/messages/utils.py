from app.main import get_auth_user,get_socket_user
from app.models import *
from flask import jsonify, request
from app import socketio
from flask_socketio import send

def index_sent():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401
    return jsonify([message.to_dict() for message in user.messages_envoyes.all()]),200

def index_received():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401
    return jsonify([message.to_dict() for message in user.messages_recus.all()]),200

def message_sent(message_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    message:Message = user.messages_envoyes.filter_by(id=message_id).first()
    if not message:
        return jsonify({
            "error":"Message not found",
            "message":"Error"
        }),404

    return jsonify(message.to_dict_with_relations()),200

def message_received(message_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    message:Message = user.messages_recus.filter_by(id=message_id).first()

    if not message:
        return jsonify({
            "error":"Message not found",
            "message":"Error"
        }),404
    else:
        message.lu = True
        db.session.commit()

    return jsonify(message.to_dict_with_relations()),200

@socketio.on('message')
def create_message(data):
    user = get_socket_user(data.get('token'))
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    announcement_id = data.get("announcement_id")
    if not announcement_id:
        return jsonify({
            "error":"Announcement id is required",
            "message":"Error"
        }),400
    if not announcement_id.isdigit():
        announcement_id = int(announcement_id)

    announcement:Announcement = Announcement.query.get(announcement_id)
    if not announcement:
        return jsonify({
            "error":"Announcement not found",
            "message":"Error"
        }),404

    try:
        message = Message(
            objet=data.get("objet"),
            contenu=data.get("contenu"),
            lu=False,
            emetteur_email=user.email,
            destinataire_email=announcement.auteur_email,
            annonce_id=announcement_id,
        )
        db.session.add(message)
        db.session.commit()
        
        send(message.to_dict_with_relations(),broadcast=True)
    except Exception as e:
        print(e)
        return jsonify({
            "error":"Error while creating message",
            "message":"Error"
        }),500