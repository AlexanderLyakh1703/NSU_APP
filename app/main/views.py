from config import oauth_config as auconf
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from requests_oauthlib import OAuth2Session

from . import main


# @main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")


def get_auth(state=None, token=None):
    if token:
        return OAuth2Session(auconf.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            auconf.CLIENT_ID, state=state, redirect_uri=auconf.REDIRECT_URI
        )
    return OAuth2Session(
        auconf.CLIENT_ID, redirect_uri=auconf.REDIRECT_URI, scope=auconf.SCOPE
    )


@main.route("/")
@main.route("/login")
def login():
    service = get_auth()
    authorization_url, state = service.authorization_url(auconf.AUTH_BASE_URL)

    # State is used to prevent CSRF, keep this for later.
    session["oauth_state"] = state
    print(state)
    return redirect(authorization_url)


@main.route("/callback", methods=["GET"])
def callback():

    print(request.url)
    service = get_auth(state=session["oauth_state"])
    token = service.fetch_token(
        auconf.TOKEN_URL,
        client_secret=auconf.CLIENT_SECRET,
        authorization_response=request.url,
    )

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session["oauth_token"] = token

    return redirect(url_for("main.profile"))


@main.route("/profile", methods=["GET"])
def profile():
    service = get_auth(token=session["oauth_token"])
    return jsonify(
        service.get(
            "https://sso.nsu.ru/auth/realms/NSU/protocol/openid-connect/userinfo"
        ).json()
    )
    # return jsonify(service.get("https://www.googleapis.com/oauth2/v1/userinfo").json())
