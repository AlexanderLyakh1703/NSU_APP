from flask import jsonify, redirect, render_template, request, session, url_for

from ..api import auth
from . import main


@main.route("/")
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

@main.route("/timetable")
def timetable():

    # magic

    return render_template("options/Timetable.html")

@main.route("/login")
def login():
    return redirect(auth.authorization())


@main.route("/callback", methods=["GET"])
def callback():
    auth.get_token(request.url)

    return redirect(url_for("main.profile"))


@main.route("/profile", methods=["GET"])
def profile():
    auth.get_userinfo()
    return jsonify(session.get("userinfo"))
