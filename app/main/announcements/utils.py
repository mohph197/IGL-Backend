from app.models import *
from app import login_is_required
from flask import jsonify, request, current_app as app
from werkzeug.utils import secure_filename
import os

def get_auth_user():
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return None
    bearer_token = authorization_header.split(' ')[1]
    login_info = login_is_required(bearer_token)
    if not login_info:
        return None
    return User.query.get(login_info["email"])

def index():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    return jsonify([announcement.to_dict() for announcement in user.annonces_poste.all()]),200

def announcement(announcement_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    announcement = user.annonces_poste.filter_by(id=announcement_id).first()
    if not announcement:
        return jsonify({
            "error":"Announcement not found",
            "message":"Error"
        }),404

    return jsonify(announcement.to_dict_with_relations()),200

def create_announcement():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    try:
        location = Location.query.filter_by(wilaya=request.form.get("wilaya"), commune=request.form.get("commune"), adresse=request.form.get("adresse")).first()
        if not location:
            location = Location(wilaya=request.form.get("wilaya"), commune=request.form.get("commune"), adresse=request.form.get("adresse"))
            db.session.add(location)
            db.session.commit()
    except:
        return jsonify({
            "error":"Error while creating location",
            "message":"Error"
        }),500

    try:
        announcement = Announcement(type=request.form.get("type") or None, surface=request.form.get("surface") or None, description=request.form.get("description") or None, prix=request.form.get("prix"), categorie=request.form.get("categorie"), auteur_email=user.email, localisation_id=location.id)
        db.session.add(announcement)
        db.session.commit()
    except:
        return jsonify({
            "error":"Error while creating announcement",
            "message":"Error"
        }),500

    for picture in request.files.getlist("photos"):
        try:
            filename = secure_filename(picture.filename)
            filedir = os.path.join(os.path.normpath(app.config['UPLOAD_FOLDER']), f'announcement_{announcement.id}')
            os.makedirs(filedir, exist_ok=True)
            filepath = os.path.join(filedir, filename)
            picture.save(filepath)
            picture = Picture(nom=filename, chemin=filepath, annonce_id=announcement.id)
            db.session.add(picture)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({
                "error":"Error while uploading pictures",
                "message":"Error"
            }),500
    db.session.refresh(announcement)

    return jsonify(announcement.to_dict_with_relations()),201

def edit_announcement(announcement_id):
    # TODO: Implement this
    return f"Edit Announcement {announcement_id}"

def delete_announcement(announcement_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    annonce = user.annonces_poste.filter_by(id=announcement_id).first()
    if not annonce:
        return jsonify({
            "error":"Announcement not found",
            "message":"Error"
        }),404

    db.session.delete(annonce)
    db.session.commit()

    return jsonify({
        "message":"Announcement deleted successfully"
    }),200