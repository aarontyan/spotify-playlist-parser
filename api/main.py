import requests
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'Boba'

CLIENT_ID = 'd8869a3b24c8428f945c7c60d7f716f9'
CLIENT_SECRET = 'c0b2c25bc9234b32a0c8e1ccc8d81606'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def home():
    return "Lol <a href='/login'>Login with your Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(auth_url)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error" : request.args['error']})
    if 'code' in request.args:
        req = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data = req)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    headers = {
        'Authorization' : f"Bearer {session['access_token']}"
    }
    response = requests.get(BASE_URL + 'me/playlists', headers = headers)
    playlists = response.json()
    return jsonify(playlists)
    
@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        request_body = {
            'grant_type' : 'refresh_token',
            'refresh_token' : session['refresh_token'],
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data = request_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        return redirect('/playlists')
