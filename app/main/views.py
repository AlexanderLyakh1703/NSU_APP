from flask import jsonify, redirect, render_template, request, session, url_for

from ..api import auth, table
from . import main


@main.route("/index")
def index():
    return render_template("index.html")


@main.route("/")
@main.route("/timetable")
def timetable():

    dict_of_vars = table.info_for_Timetable(session)

    return render_template(
        "options/Timetable.html",
        table=dict_of_vars["timetable"],
        even=dict_of_vars["even"],
        weekday=dict_of_vars["weekday"],
        roles=dict_of_vars["roles"],
    )


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
