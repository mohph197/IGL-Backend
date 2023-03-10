import os
import requests
from flask import session, abort, redirect, request, jsonify
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app.auth import flow
from app import db,login_is_required
from app.models import *
import jwt
import json

def insertUserToDb(email,prenom,nom,role):
    try:
        user = db.session.query(User).filter_by(email=email).first()

        if user == None:
            new_user = User(email=email,prenom=prenom,nom=nom,role=role)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                "email" : email,
                "message": "User created"
            }), 200
        else:
            return jsonify({
                "email" : email,
                "message": "User already exists"
            }), 200
    except Exception as e:
        return jsonify({
                "error" : e.args,
                "message": "Error"
            }), 500


def auth():
    json_string = request.get_data().decode('utf-8')
    json_object = json.loads(json_string)
    if "credentials" in json_object:
        credentials = json_object["credentials"]
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        try:
            id_info = id_token.verify_oauth2_token(
                id_token=credentials,
                request=token_request,
                audience= os.environ['GOOGLE_CLIENT_ID']
            )
            result = insertUserToDb(email=id_info['email'],prenom=id_info['given_name'],nom=id_info['family_name'],role='U')

            token = jwt.encode({"email":id_info['email']},os.environ['SECRET_KEY'],algorithm=os.environ['JWT_ALGORITHM'])

            return jsonify({
                "token":token
            }),200
        except Exception as e:
            return jsonify({
                "error": e.args,
                "message": "Error"
            }), 500
    else:
        return jsonify({
                "error": "credentials miss",
                "message": "Error"
        }), 500

def me():
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        bearer_token = authorization_header.split(' ')[1]
        login_info = login_is_required(bearer_token)
        if login_info:
            user = User.query.get(login_info["email"])
            if user:
                return jsonify(user.to_dict()),200
            else:
                return jsonify({
                    "error":"User not found",
                    "message":"Error"
                }),404
        else:
            return jsonify({
                "error":"Unauthorized",
                "message":"Error"
            }),401
    else:
        return jsonify({
            "error":"Unauthorized",
            "message":"Error"
        }),401