from app.models import *
from app.main import get_auth_user
from app.main.utils import paginate
from flask import jsonify, request, current_app as app
from werkzeug.utils import secure_filename
import os

def index():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    results = paginate(user.annonces_poste)

    return jsonify({
        "page":results['page'],
        "per_page":results['per_page'],
        "total_count":results['total_count'],
        "num_pages":results['num_pages'],
        "annonces":[annonce.to_dict() for annonce in results['items']]
    }),200

def all_announcements():
    results = paginate(Announcement.query)

    return jsonify({
        "page":results['page'],
        "per_page":results['per_page'],
        "total_count":results['total_count'],
        "num_pages":results['num_pages'],
        "annonces":[annonce.to_dict() for annonce in results['items']]
    }),200

def announcement(announcement_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    announcement:Announcement = user.annonces_poste.filter_by(id=announcement_id).first()
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

def delete_announcement(announcement_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    annonce:Announcement = user.annonces_poste.filter_by(id=announcement_id).first()
    if not annonce:
        return jsonify({
            "error":"Announcement not found",
            "message":"Error"
        }),404

    # Delete all the photos of annonce
    for photo in annonce.photos.all():
        os.remove(photo.chemin)
        db.session.delete(photo)
    db.session.delete(annonce)
    db.session.commit()

    return jsonify({
        "message":"Announcement deleted successfully"
    }),200

def search():
    query = request.args.get('q')
    if not query:
        return jsonify({
            "error":"Query is required",
            "message":"Error"
        }),400
        
    results_query = Announcement.query.filter((Announcement.type.contains(query)) | Announcement.description.contains(query))

    results = paginate(results_query)

    return jsonify({
        "page":results['page'],
        "per_page":results['per_page'],
        "total_count":results['total_count'],
        "num_pages":results['num_pages'],
        "annonces":[annonce.to_dict() for annonce in results['items']]
    }),200