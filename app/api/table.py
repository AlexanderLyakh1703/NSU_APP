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
