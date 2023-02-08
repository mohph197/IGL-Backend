from app.models import *
from app.main import get_auth_user
from app.main.utils import paginate
from flask import jsonify, request, current_app as app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy.sql.expression import and_
from sqlalchemy import desc
import requests

def index():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    return jsonify(
        [annonce.to_dict_with_relations() for annonce in user.annonces_poste.order_by(desc(Announcement.id)).all()]
    ),200

def all_announcements():
    try:
        filter_conditions = []
        #Text Search =================================================
        if 'q' in request.args:
            query = request.args.get('q')
            filter_conditions.append((Announcement.titre.contains(query)) | (Announcement.description.contains(query)))

        #Field Filtering ====================================================
        if 'type' in request.args:
            type = request.args.get('type')
            if type != 'Autre':
                filter_conditions.append(Announcement.type == type)

        #Filtering by date =========================================
        if 'start_date' in request.args:
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
            filter_conditions.append(Announcement.date_publication >= start_date)

        if 'end_date' in request.args:
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
            filter_conditions.append(Announcement.date_publication <= end_date)

        #Filtering by price ==============================================
        if 'start_price' in request.args:
            start_price = float(request.args.get('start_price'))
            filter_conditions.append(Announcement.prix >= start_price)

        if 'end_price' in request.args:
            end_price = float(request.args.get('end_price'))
            filter_conditions.append(Announcement.prix <= end_price)

        filter_condition = and_(True, *filter_conditions)
        results_query = Announcement.query.filter(filter_condition).order_by(desc(Announcement.date_publication))
        
        #Foreign Elements Filtering ===============================
        if 'wilaya' in request.args:
            wilaya = request.args.get('wilaya')
            results_query = results_query.join(Announcement.localisation).filter(Location.wilaya_name_ascii.contains(wilaya))

        if 'commune' in request.args:
            commune = request.args.get('commune')
            results_query = results_query.join(Announcement.localisation).filter(Location.commune_name_ascii.contains(commune))

        results = paginate(results_query)

        return jsonify({
            "page":results['page'],
            "per_page":results['per_page'],
            "total_count":results['total_count'],
            "num_pages":results['num_pages'],
            "annonces":[annonce.to_dict_with_relations() for annonce in results['items']]
        }),200

    except Exception as e:
        return jsonify(
            {
                'error':e.args,
                'message':'Error',
            }
        ),500

def announcement(announcement_id):
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    announcement:Announcement = Announcement.query.filter_by(id=announcement_id).first()
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
        location = Location.query.filter_by(wilaya_name_ascii=request.form.get("wilaya"), commune_name_ascii=request.form.get("commune")).first()
        if not location:
            location = Location(wilaya_name_ascii=request.form.get("wilaya"), commune_name_ascii=request.form.get("commune"))
            db.session.add(location)
            db.session.commit()
    except:
        return jsonify({
            "error":"Error while creating location",
            "message":"Error"
        }),500

    try:
        announcement = Announcement(type=request.form.get("type") or None,titre=request.form.get("titre") or '', surface=request.form.get("surface") or None, description=request.form.get("description") or None,
        prix=request.form.get("prix"), adresse=request.form.get('adresse'), latitude=request.form.get('latitude'), longitude=request.form.get('longitude'),
        categorie=request.form.get("categorie"),date_publication=datetime.now().date(), auteur_email=user.email, localisation_id=location.id)
        db.session.add(announcement)
        db.session.commit()
    except Exception as e:
        print(e)
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
        except:
            return jsonify({
                "error":"Error while uploading pictures",
                "message":"Error"
            }),500
    db.session.refresh(announcement)

    return jsonify(announcement.to_dict_with_relations()),201

def create_announcement_from_scrapp():
    user = get_auth_user()
    if not user:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401
    data = request.get_json()
    try:
        location = Location.query.filter_by(wilaya_name_ascii=data.get("wilaya"), commune_name_ascii=data.get("commune")).first()
        if not location:
            location = Location(wilaya_name_ascii=data.get("wilaya"), commune_name_ascii=data.get("commune"))
            db.session.add(location)
            db.session.commit()
    except:
        return jsonify({
            "error":"Error while creating location",
            "message":"Error"
        }),500

    try:
        announcement = Announcement(type=data.get("type") or None,titre=data.get("titre") or '', surface=data.get("surface") or None, description=data.get("description") or None,
        prix=data.get("prix"), adresse=data.get('adresse'), latitude=data.get('latitude'), longitude=data.get('longitude'),
        categorie=data.get("categorie"),date_publication= datetime.strptime(data.get('date_publication'), '%Y-%m-%d').date(), auteur_email=user.email, localisation_id=location.id)
        db.session.add(announcement)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "error":"Error while creating announcement",
            "message":"Error"
        }),500

    cpt = 1
    for picture in data.get("photos"):
        try:
            filedir = os.path.join(os.path.normpath(app.config['UPLOAD_FOLDER']), f'announcement_{announcement.id}')
            os.makedirs(filedir, exist_ok=True)

            # Download the image
            response = requests.get(picture)

            # Get the extension info
            content_type = response.headers.get('content-type')
            extension = content_type.split('/')[-1]

            # Creating the image file
            filename = secure_filename(f'image{cpt}.{extension}')
            filepath = os.path.join(filedir, filename)
            
            with open(filepath,"wb") as f:
                f.write(response.content)

            # Save picture in DB
            picture = Picture(nom=filename, chemin=filepath, annonce_id=announcement.id)
            db.session.add(picture)
            db.session.commit()
            cpt += 1
        except:
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
        if os.path.exists(photo.chemin):
            os.remove(photo.chemin)
        db.session.delete(photo)
    db.session.delete(annonce)
    db.session.commit()

    return jsonify({
        "message":"Announcement deleted successfully"
    }),200

def announcement_messages(announcement_id):
    annonce:Announcement = Announcement.query.get(announcement_id)
    if not annonce:
        return jsonify({
            "error":"Announcement not found",
            "message":"Error"
        }),404

    discussions: list[Discussion] = annonce.discussions.all()
    return jsonify([discussion.to_dict() for discussion in discussions]),200