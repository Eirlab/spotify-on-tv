from flask import Flask, request, redirect, render_template
from waitress import serve
import requests
import base64
import random
import string
import urllib.parse as urlparse

app = Flask(__name__)

client_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
refresh_token = "xxxx"

# https://gistcdn.githack.com/antoinepringalle/3a4aa2d4f0fc1c2a9a178e95e815f348/raw/40fc1230accf2108b82e8e65761112ae5dbf3b8e/no-music-spotify.svg
no_song_svg = "static/svg/no-music-spotify.svg"
port = 8000
redirect_uri = "http://localhost:{}/callback".format(str(port))
code = ""


@app.route("/favicon.ico")
def favicon():
    return ""


@app.route("/callback")
def callback():
    global code
    code = request.args.get("code")
    return ""


@app.route("/login")
def login():
    query_params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "user-read-private user-read-email",
        "redirect_uri": redirect_uri,
        "state": "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    }
    login_url = "https://accounts.spotify.com/authorize?" + urlparse.urlencode(query_params)
    return redirect(login_url)


@app.route("/getToken")
def get_token():
    global code
    auth_options = {
        "url": "https://accounts.spotify.com/api/token",
        "form": {
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        },
        "headers": {
            "Authorization": "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode(),
            "Access-Control-Allow-Origin": "*"
        },
        "json": True
    }
    response = requests.post(auth_options["url"], data=auth_options["form"], headers=auth_options["headers"])
    if response.status_code == 200:
        data = response.json()
        global refresh_token
        refresh_token = data["refresh_token"]
        return {
            "refreshToken": refresh_token,
            "accessToken": data["access_token"]
        }
    return ""


@app.route("/nextToken")
def next_token():
    auth_options = {
        "url": "https://accounts.spotify.com/api/token",
        "form": {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        "headers": {
            "Authorization": "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode(),
        },
        "json": True
    }
    response = requests.post(auth_options["url"], data=auth_options["form"], headers=auth_options["headers"])
    if response.status_code == 200:
        data = response.json()
        return {
            "accessToken": data["access_token"]
        }
    return ""


@app.route("/")
def home():
    return render_template("index.html", port=port, refresh_token=refresh_token, noSongSVG=no_song_svg)


if __name__ == "__main__":
    print("Listening on port {}".format(str(port)))
    serve(app, host="0.0.0.0", port=port)
