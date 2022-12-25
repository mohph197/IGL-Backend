import os
import requests
from flask import session, abort, redirect, request, jsonify
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app.auth import flow
from app import db,login_is_required
from app.auth.models import *
import jwt


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


def new_auth():
    credentials = request.args.get('credentials')

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

def auth():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)

def me():
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        bearer_token = authorization_header.split(' ')[1]
        login_info = login_is_required(bearer_token)
        if login_info:
            user = db.session.query(User).filter_by(email=login_info.email).first()
            if user:
                return jsonify({
                    "email":user.email,
                    "firstName":user.prenom,
                    "lastName":user.nom,
                    "role":user.role
                }),200
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

def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience= os.environ['GOOGLE_CLIENT_ID']
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["user_info"] = {
        "email":id_info['email'],
        "firstName":id_info['given_name'],
        "lastName":id_info['family_name'],
        "role":'U'
    }

    result = insertUserToDb(email=id_info['email'],prenom=id_info['given_name'],nom=id_info['family_name'],role='U')

    return result

def logout():
    session.clear()
    return jsonify({
        "message": "Successfully logged out"
    }), 200