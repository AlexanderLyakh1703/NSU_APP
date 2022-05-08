import json
from base64 import b64encode
from http.client import HTTPSConnection

from config import api_config as aconf
from flask import session

from datetime import datetime

# импоритруем модели
from model import Order, Lesson

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


# function for sortings and check lessons
def check_for_equals(write :dict()):
    return [ write["weekday"], write["id_time"] ]

# объединяем пары с одинаковым днём недели, временем и преподавателем
def union_of_lessons_by_groups(request_for_timetable :list[dict]): # for teachers

    request_for_timetable.sort(key=check_for_equals)

    number_write = 0

    while number_write+1 < len(request_for_timetable):

        this_write = request_for_timetable[number_write]
        next_write = number_writes[number_write+1]

        if present(this_write) == present(next_write):

                # i am writting here swap two objects
                if this_write['id_groups'] is list:
                    this_write['id_groups'].append(next_write['id_groups'])
                else:
                    this_write['id_groups'] = [this_write['id_groups'],
                                               next_write['id_groups'] ]
                del request_for_timetable[number_write+1]
        else:
            number_write += 1

    # make array of lessons
    array_of_lessons = []

    for row in req_for_lessons:
        lesson = Lesson(row)
        array_of_lessons.append(lesson)

    order = Order(array_of_lessons)

    return order

# получаем роль студент/преподаватель
def get_roles(user):

    fullname = ' '.join(list(user['name'].split()[::-1]
                                + [user['middlename']]))

    # не, тут явно уязвимость, т. к. люди с одинаковым ФИО будут учителями
    id_teacher = connect("teacher",{'fullname':fullname})

    # есть ровно ОДНА запись с таким fullname И есть он НЕ бакалавр
    if len(id_teacher) == 1 and user['groups']['StudentCourses'].split('_')[-1] != 'bac':
        roles = 'teacher'
    else:
        roles = 'student'

    return roles

# конвертируем массив словарей в тип данных order
def convert(list_of_dicts :list[dict]):

    array_of_lessons = []

    for elem in list_of_dicts:
        array_of_lessons.append(Lesson(elem))

    order = Order(array_of_lessons)

    return order


def info_for_Timetable(session):
    # get User from variable of session
    user = session["userinfo"]

    # get the parity of the week
    even = connect("parity")["actual"] # "odd" or "even"

    weekday = datetime.today().weekday()+1 # value from {1,...,7}


    roles = get_roles(user)


    if roles == 'student':

        id_group = connect("group",{'name':group})[0]['id']

        timetable = connect("schedule",{'id_group':id_group})

        order = convert(timetable)

    else: # roles = 'teacher'

        timetable = connect("schedule",{'id_teacher':id_teacher})
        order = convert(union_of_lessons_by_groups(timetable))



    return {'timetable':order,'even':even,
            'weekday':weekday,'roles':roles}
