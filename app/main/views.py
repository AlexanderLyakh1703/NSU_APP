from config import oauth_config as auconf
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from requests_oauthlib import OAuth2Session

from . import main
from .. import api

# @main.route("/")
@main.route("/index")
def index():
    session["User"] = User() # make this in auth, please
    return render_template("index.html")

@main.route("/settings")
def option():
    # i will use super params User please

    return render_template("Settings.html") # rename files

@main.route("/timetable")
def table():
    # get User from variable of session
    User = session["User"]

    # get the parity of the week
    even = api.table.connect("parity")["actual"] # "odd" or "even"

    if User.roles == "student":

        # get id of group our User
        id_group = api.table.connect("group",{"name":User.group})[0]["id"]

        req_for_table = api.table.connect("schedule",{"id_group":id_group})

        # make array of lessons
        array_of_lessons = []

        for row in req_for_lessons:
            lesson = Lesson(row)
            array_of_lessons.append(lesson)

        order = Order(array_of_lessons)

        return render_template("Timetable.html",order=order,even=even)

    elif User.roles == "teacher":

        # we must swap all lessons with different id_groups and equal other params
        req_for_table = api.table.connect("schedule",{"id_teacher":id_teacher})

        # function for check equals of lessons
        present = lambda write:[write["id_group"],
                                write["weekday"],
                                write["id_time"],
                                write["id_teacher"],
                                write["room"]]

        req_for_table.sort(key=present)

        number_write = 0

        while number_write+1 < len(req_for_table):

            this_write = req_for_table[number_write]
            next_write = number_writes[number_write+1]

            if present(this_write) == present(next_write):

                    # i am writting here swap two objects
                    if this_write['id_groups'] is list:
                        this_write['id_groups'].append(next_write['id_groups'])
                    else:
                        this_write['id_groups'] = [this_write['id_groups'],
                                                   next_write['id_groups'] ]
                    del req_for_table[number_write+1]
            else:
                number_write += 1

            # make array of lessons
            array_of_lessons = []

            for row in req_for_lessons:
                lesson = Lesson(row)
                array_of_lessons.append(lesson)

            order = Order(array_of_lessons)

            return render_template("Timetable.html",order=order,even=even)

    elif User.roles == "combo":
        pass
        # it's combination of "teacher" ahd "student"

@main.route("/orderBook")
def table():
    # i will use super params User
    # even = api.table.connect()
    return render_template("Order-Book.html") # rename files

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
    # session["user"] = User // type User (from model.py)

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
