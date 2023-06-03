from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

import os
import requests
import json
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

auth = Blueprint('auth', __name__)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()



@auth.route('/login')
def login():
    # Find out what URL to hit for Google login
     
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth.route("/login/callback")
def callback():

    try:
        # Get authorization code Google sent back to you
        code = request.args.get("code")
    except: 
        return "stage 1", 400

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    try:
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
    except: 
        return "stage 2", 400

    # Prepare and send a request to get tokens! Yay tokens!
    try:
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
    except: 
        return token_endpoint+', '+request.url+', '+request.base_url+', '+code, 400
    
    try:
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        )
    except: 
        return "stage 4", 400

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]        
        family_name = userinfo_response.json()["family_name"]
        full_name = userinfo_response.json()["name"]        
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided    

    user = User.query.filter_by(id=unique_id).first()

    new_user = User(id=unique_id, email=users_email, first_name=users_name, last_name=family_name, full_name=full_name)
    
    if not user:        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    else:
        login_user(user, remember=True)
        
    # Send user back to homepage
    return render_template('home.html', user=current_user)
"""

@auth.route('/login')
def login():
    # Find out what URL to hit for Google login
     
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth.route("/login/callback")
def callback():

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]        
        family_name = userinfo_response.json()["family_name"]
        full_name = userinfo_response.json()["name"]        
    else:
        return "User email not available or not verified by Google.", 400

  
    user = User.query.filter_by(id=unique_id).first()

    new_user = User(id=unique_id, email=users_email, first_name=users_name, last_name=family_name, full_name=full_name)
    
    if not user:        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    else:
        login_user(user, remember=True)
        

    return render_template('home.html', user=current_user)

    """

@auth.route('/logout')
@login_required
def logout():       
    token = client.access_token
    requests.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    logout_user() 
    return render_template('logout.html')
