import json
from base64 import b64encode
from http.client import HTTPSConnection

from config import api_config as aconf

# разделы БД
links = {
    "faculty": "/api/faculties",
    "teacher": "/api/teachers",
    "group": "/api/groups",
    "time": "/api/times",
    "type-occupation": "/api/type-occupations",
    "parity": "/api/parities",
    "term": "/api/terms",
    "exam-group": "/api/exam-groups",
    "schedule": "/api/schedules",
}

# type - раздел БД, search - параметры поиска
def connect(type_: str, search=dict()) -> list[dict]:

    # заполнение данных для авторизации
    connect = HTTPSConnection("table.nsu.ru")
    userAndPass = b64encode(aconf.TABLE_TOKEN).decode("utf-8")
    headers = {"Authorization": "Basic %s" % userAndPass}

    # собираем строку поиска
    string_of_find = ""
    if search != dict():
        string_of_find = "/search?" + "&".join(
            [elem + "=" + search[elem] for elem in search.keys()]
        )

    # посылаем запрос
    connect.request("GET", links[type] + string_of_find, headers=headers)
    res = connect.getresponse()
    data = res.read()

    # возвращаем ответ в виде массива словарей
    return json.loads(data.decode("utf-8"))

# example: print(connect("faculty",{"id":"1"}))

def info_for_Timetable():
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


    elif User.roles == "teacher":

        # we must swap all lessons with different id_groups and equal other params
        req_for_table = api.table.connect("schedule",{"id_teacher":id_teacher})

        # function for check equals of lessons
        present = lambda write:[write["weekday"],
                                write["id_time"],
                                write["roomsokr"]]

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

    elif User.roles == "combo":
        pass
        # it's combination of "teacher" ahd "student"
        # i don't smt about this

    else:
        pass
        # ERROR: I don't know your role...

    return render_template("Timetable.html",table=order,even=even,weekday=datetime.datetime.today().weekday()+1)
