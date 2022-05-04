import datetime

from flask import jsonify, redirect, render_template, request, session, url_for

from ..api import auth, table
from . import main


# @main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")


@main.route("/settings")
def option():
    # i needed design from Vova Bobenko!!!

    # i will use super params User please

    return render_template("Settings.html")  # rename files


@main.route("/timetable")
def table():
    # get User from variable of session
    User = session["User"]

    # get the parity of the week
    even = table.connect("parity")["actual"]  # "odd" or "even"

    if User.roles == "student":

        # get id of group our User
        id_group = table.connect("group", {"name": User.group})[0]["id"]

        req_for_table = table.connect("schedule", {"id_group": id_group})

        # make array of lessons
        array_of_lessons = []

        for row in req_for_lessons:
            lesson = Lesson(row)
            array_of_lessons.append(lesson)

        order = Order(array_of_lessons)

    elif User.roles == "teacher":

        # we must swap all lessons with different id_groups and equal other params
        req_for_table = table.connect("schedule", {"id_teacher": id_teacher})

        # function for check equals of lessons
        present = lambda write: [write["weekday"], write["id_time"], write["roomsokr"]]

        req_for_table.sort(key=present)

        number_write = 0

        while number_write + 1 < len(req_for_table):

            this_write = req_for_table[number_write]
            next_write = number_writes[number_write + 1]

            if present(this_write) == present(next_write):

                # i am writting here swap two objects
                if isinstance(his_write["id_groups"], list):
                    this_write["id_groups"].append(next_write["id_groups"])
                else:
                    this_write["id_groups"] = [
                        this_write["id_groups"],
                        next_write["id_groups"],
                    ]
                del req_for_table[number_write + 1]
            else:
                number_write += 1

        # make array of lessons
        array_of_lessons = []

        for row in req_for_lessons:
            lesson = Lesson(row)
            array_of_lessons.append(lesson)

        order = Order(array_of_lessons)

    elif User.roles == "combo":
        pass
        # it's combination of "teacher" ahd "student"
        # i don't smt about this

    else:
        pass
        # ERROR: I don't know your role...

    return render_template(
        "Timetable.html",
        table=order,
        even=even,
        weekday=datetime.datetime.today().weekday() + 1,
    )


@main.route("/orderBook")
def orderBook():
    # I needed API !!!!!! for cab.nsu.ru

    # i will use super params User
    # even = api.table.connect()
    return render_template("Order-Book.html")  # rename files


@main.route("/")
@main.route("/login")
def login():
    auth_url, state = auth.authorization()
    session["oauth_state"] = state
    session.modified = True
    return redirect(auth_url)


@main.route("/callback", methods=["GET"])
def callback():
    session["oauth_token"] = auth.get_token(session.get("oauth_state"), request.url)
    session.modified = True
    return redirect(url_for("main.profile"))


@main.route("/profile", methods=["GET"])
def profile():
    session["userinfo"] = auth.get_userinfo(session.get("oauth_token"))
    session.modified = True
    return jsonify(session["userinfo"])
