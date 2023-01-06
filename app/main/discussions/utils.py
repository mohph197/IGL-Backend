from app.main import get_auth_user
from app.models import *
from flask import jsonify, request
from app import socketio,connections
from flask_socketio import send
from sqlalchemy.sql.expression import and_

def index_sent():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401
    return jsonify([discussion.to_dict() for discussion in user.discussions_demandees.all()]),200

def index_received():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401
    return jsonify([discussion.to_dict() for discussion in user.discussions_annonces.all()]),200

def discussion_sent(discussion_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    discussion:Discussion = user.discussions_demandees.filter_by(id=discussion_id).first()

    if not discussion:
        return jsonify({
            "error":"Discussion not found",
            "message":"Error"
        }),404
    else:
        for message in discussion.messages:
            if user.email != message.emetteur_email:
                message.lu = True
        db.session.commit()

    return jsonify(discussion.to_dict_with_relations()),200

def discussion_received(discussion_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    discussion:Discussion = user.discussions_annonces.filter_by(id=discussion_id).first()

    if not discussion:
        return jsonify({
            "error":"Discussion not found",
            "message":"Error"
        }),404
    else:
        for message in discussion.messages:
            if user.email != message.emetteur_email:
                message.lu = True
        db.session.commit()

    return jsonify(discussion.to_dict_with_relations()),200


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

    #Check if a previous discussion exists for the announcement
    discussion:Discussion = Discussion.query.filter(and_(Discussion.annonce_id == announcement_id, (Discussion.annonceur_email == user.email) | (Discussion.demandeur_email == user.email))).first()
    if discussion:
        message = Message(
            objet=data.get("objet"),
            contenu=data.get("contenu"),
            lu=False,
            emetteur_email=user.email,
            discussion_id=discussion.id,
        )

        db.session.add(message)
        db.session.commit()

        sid = connections.get(discussion.demandeur_email if user.email == discussion.annonceur_email else discussion.annonceur_email)
        if sid:
            send(message.to_dict_with_relations(),room=sid)
        else:
            return jsonify({
                "error": "The message recipient is not online",
                "message": "Error"
            }),200
    else:
        #Check if the announcement exists
        announcement:Announcement = Announcement.query.get(announcement_id)
        if not announcement:
            return jsonify({
                "error":"Announcement not found",
                "message":"Error"
            }),404

        try:
            if user.email != announcement.auteur_email:
                discussion = Discussion(
                    annonce_id = announcement_id,
                    annonceur_email = announcement.auteur_email,
                    demandeur_email = user.email,
                )
                db.session.add(discussion)
                db.session.commit()
                
                message = Message(
                    objet=data.get("objet"),
                    contenu=data.get("contenu"),
                    lu=False,
                    emetteur_email=user.email,
                    discussion_id=discussion.id,
                )

                db.session.add(message)
                db.session.commit()

                sid = connections.get(discussion.annonceur_email)
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
        except Exception as e:
            return jsonify({
                "error":e.args,
                "message":"Error"
            }),500