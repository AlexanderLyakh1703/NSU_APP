import json
from config import api_config as aconf
import requests
from datetime import datetime
import sys

# импоритруем модели
from ..model import Lesson,Order

# -----------------------------------------------------------------------------
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
def connect(type_: str, search=None) -> list[dict]:
    # собираем строку поиска
    string_of_find = ""
    if search:
        string_of_find = "/search?" + "&".join(
            [str(key) + "=" + str(value) for key, value in search.items()]
        )

    # посылаем запрос
    data = requests.get(
        "https://table.nsu.ru" + links[type_] + string_of_find,
        auth=(aconf.TABLE_TOKEN, ""),
    ).text
    # возвращаем ответ в виде массива словарей
    # print(json.loads(data))
    return json.loads(data)



# function for sortings and check lessons
def check_for_equals(write: dict()):
    return [write["weekday"], write["id_time"],write["id_teacher"]]


# объединяем пары с одинаковым днём недели, временем и преподавателем
def union_of_lessons_by_groups(request_for_timetable: list[dict]):  # for teachers

    request_for_timetable.sort(key=check_for_equals)

    number_write = 0

    while number_write + 1 < len(request_for_timetable):

        this_write = request_for_timetable[number_write]
        next_write = number_write[number_write + 1]

        if check_for_equals(this_write) == check_for_equals(next_write):

            # i am writting here swap two objects
            if this_write["id_groups"] is list:
                this_write["id_groups"].append(next_write["id_groups"])
            else:
                this_write["id_groups"] = [
                    this_write["id_groups"],
                    next_write["id_groups"],
                ]
            del request_for_timetable[number_write + 1]
        else:
            number_write += 1

    # make array of lessons
    array_of_lessons = []

    for row in request_for_timetable:
        lesson = Lesson(row)
        array_of_lessons.append(lesson)

    order = Order(array_of_lessons)

    return order


# получаем роль студент/преподаватель
def get_roles(user):

    fullname = " ".join(list(user["name"].split()[::-1] + [user["middlename"]]))

    # не, тут явно уязвимость, т. к. люди с одинаковым ФИО будут учителями
    id_teacher = connect("teacher", {"fullname": fullname})

    # есть ровно ОДНА запись с таким fullname И есть он НЕ бакалавр
    if len(id_teacher) == 1:
        roles = "teacher"
    else:
        roles = "student"

    return roles


# конвертируем массив словарей в тип данных order
def convert(list_of_dicts: list[dict]):

    array_of_lessons = []

    for elem in list_of_dicts:
        array_of_lessons.append(Lesson(**elem))
        print(elem)

    res = Order(array_of_lessons)

    return res


def getInfo(session):
    # get User from variable of session
    # user = session["userinfo"]

    user = {
        "email": "d.sukhorukov1@g.nsu.ru",
        "family_name": "\u0421\u0443\u0445\u043e\u0440\u0443\u043a\u043e\u0432",
        "given_name": "\u0414\u0430\u043d\u0438\u0438\u043b",
        "groups": {
            "NSU": "Hist",
            "StudentCourses": "all_1y_bac",
            "StudentFaculties": "mmf",
            "StudentFacultyCourses": "mmf_1y_bac",
            "StudentGroups": "21114",
        },
        "middlename": "\u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u043e\u0432\u0438\u0447",
        "name": "\u0414\u0430\u043d\u0438\u0438\u043b \u0421\u0443\u0445\u043e\u0440\u0443\u043a\u043e\u0432",
        "preferred_username": "d.sukhorukov1",
        "sub": "f:a04424ec-9f9c-4ac6-85c7-fe09e25348f7:d.sukhorukov1",
    }

    # get the parity of the week
    even = connect("parity")["actual"]  # "odd" or "even"
    weekday = datetime.today().weekday() + 1  # value from {1,...,7}
    roles = get_roles(user)

    if roles == "student":
        id_group = connect("group", {"name": user["groups"]["StudentGroups"]})[0]["id"]
        timetable = connect("schedule", {"id_group": str(id_group)})
        for elem in timetable:
            print(elem)
        order = convert(timetable)
    else:  # roles == 'teacher'
        fullname = " ".join(list(user["name"].split()[::-1] + [user["middlename"]]))
        id_teacher = connect("teacher", {"fullname": fullname})[0]["id"]
        timetable = connect("schedule", {"id_teacher": str(id_teacher)})
        # for elem in timetable:
        #     print(elem)
        order = convert(union_of_lessons_by_groups(timetable))


    return {"timetable": order.schedule, "even": even, "weekday": weekday, "roles": roles}

def presentation(lesson):

    teacher_name = connect("teacher", {"id": lesson.id_teacher})[0]["name"]
    type_lesson_name = str(lesson.type)
    weekday_name = {
        0: "ВОСКРЕСЕНЬЕ",
        1: "ПОНЕДЕЛЬНИК",
        2: "ВТОРНИК",
        3: "СРЕДА",
        4: "ЧЕТВЕРГ",
        5: "ПЯТНИЦА",
        6: "СУББОТА",
    }[lesson.weekday % 7]

    even_name = lesson.even

    list_group_names = []
    for id_group in lesson.id_list_groups:
        group_name = connect("group", {"id": id_group})[0]["name"]
        list_group_names.append(group_name)

    request_for_time = connect("time", {"id": lesson.id_time})[0]

    fast_lesson_name = connect(
        "schedule",
        {
            "id_teacher": str(lesson.id_teacher),
            "id_time": str(lesson.id_time),
            "weekday": str(lesson.weekday),
        },
    )[0]["namesokr"]

    time_name = {"begin": request_for_time["begin"], "end": request_for_time["end"]}
    room_name = lesson.room
    ret_dict = {
        "teacher": teacher_name,
        "type": type_lesson_name,
        "weekday": weekday_name,
        "even": even_name,
        "groups": list_group_names,
        "time": time_name,
        "room": room_name,
        "name": fast_lesson_name,
    }
    # print(ret_dict)
    return ret_dict
