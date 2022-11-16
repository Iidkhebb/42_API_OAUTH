import requests, json
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # <- change this to 0 in production means using SSL
app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route('/login')
def login():
    UID = os.getenv('UID')
    SECRET = os.getenv('SECRET')
    AUTH_URL = 'https://api.intra.42.fr/oauth/authorize'
    auth = OAuth2Session(UID, redirect_uri='http://localhost:5000/callback')
    authorization_url, state = auth.authorization_url(AUTH_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    UID = os.getenv('UID')
    SECRET = os.getenv('SECRET')
    TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
    auth = OAuth2Session(UID, state=session['oauth_state'])

    token = auth.fetch_token(TOKEN_URL, client_id=UID, client_secret=SECRET, authorization_response=request.url) # <- this is where the error is
    # session['oauth_token'] = token
    # return token.get('https://api.intra.42.fr/v2/me')
    return "Hello World"


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)