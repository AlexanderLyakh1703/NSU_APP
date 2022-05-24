from flask import jsonify, redirect, render_template, request, session, url_for
from datetime import datetime
from ..api import auth, table
from . import main


@main.route("/index")
def index():
    return render_template("index.html")


@main.route("/")
@main.route("/timetable")
def timetable():

    Info,role,even = table.get_info(session)

    thisData = datetime.today().weekday() + 1

    if even == "even":
        array_of_days = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]
    else:
        array_of_days = [8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]

    array_of_days = array_of_days[thisData - 1 : :] + array_of_days[: thisData - 1 :]

    return render_template(
        "timetable.html",
        timetable=Info,
        array_of_days=array_of_days,
        role=role,
        # time=
    )


@main.route("/about")
def about():
    return render_template("about.html")


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
