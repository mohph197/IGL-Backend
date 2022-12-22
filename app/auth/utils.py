import os
import requests
from flask import Blueprint,session, abort, redirect, request
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app.auth import flow

def auth():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)

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
    session["name"] = id_info.get("name")
    
    return redirect("/protected_area")  #the final page where the authorized users will end up

def logout():
    session.clear()
    return redirect("/")