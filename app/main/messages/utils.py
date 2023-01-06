from app.main import get_auth_user
from app.models import *
from flask import jsonify, request
from app import socketio,connections
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


#For sending and receiving messages in real-time =========================
@socketio.on('connect')
def on_connect():
    user = get_auth_user()
    if user:
        connections[user.email] = request.sid

@socketio.on('message')
def create_message(args):
    user = get_auth_user()
    data = args.get('data')
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
        if user.email != announcement.auteur_email:
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
            sid = connections.get(message.destinataire_email)
            if sid:
                send(message.to_dict_with_relations(),room=sid)
            else:
                return jsonify({
                    "error": "The message recipient is not online",
                    "message": "Error"
                }),200
        else:
            return jsonify({
                "error":"Cannot send message to yourself",
                "message":"Error"
            }),403
    except:
        return jsonify({
            "error":"Error while creating message",
            "message":"Error"
        }),500