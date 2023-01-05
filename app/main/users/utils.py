from app.models import *
from app.main import get_auth_user
from flask import jsonify, request

def contacts():
    user = get_auth_user()
    if not user:
       return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401

    try:
        tel = request.form.get('tel')
        if tel:
            user.tel = tel

        adresse = request.form.get('adresse')
        if adresse:
            user.adresse = adresse

        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "error":"Error while updating user",
            "message":"Error"
        }),500

    return jsonify(user.to_dict_with_relations()),200