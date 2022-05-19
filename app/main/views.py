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

    dict_of_vars = table.getInfo(session)
    print(dict_of_vars["timetable"])

    thisData = dict_of_vars["weekday"]

    if dict_of_vars["even"] == "even":
        array_of_days = [1,2,3,4,5,6,8,9,10,11,12,13]
    else:
        array_of_days = [8,9,10,11,12,13,1,2,3,4,5,6]

    array_of_days = array_of_days[thisData-1::] + array_of_days[:thisData-1:]

    timetable = dict_of_vars["timetable"]
    for weekday in timetable.keys():
        for time in timetable[weekday].keys():
            timetable[weekday][time] = table.presentation(timetable[weekday][time])
            print(timetable[weekday][time])

    return render_template(
        "timetable.html",
        timetable=timetable,
        array_of_days=array_of_days,
        role=dict_of_vars["roles"],
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
