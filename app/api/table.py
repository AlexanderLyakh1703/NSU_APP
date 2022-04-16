from http.client import HTTPSConnection
from base64 import b64encode
import json

# login:password
TABLE_TOKEN = b"SCFFAtHIAFhTa4HOBoAvOgqMDqq8uOBd_1648434328:"

# разделы БД
links = {
    "faculty":"/api/faculties",
    "teacher":"/api/teachers",
    "group":"/api/groups",
    "time":"/api/times",
    "type-occupation":"/api/type-occupations",
    "parity":"/api/parities",
    "term":"/api/terms",
    "exam-group":"/api/exam-groups",
    "schedule":"/api/schedules",
}

# type - раздел БД, search - параметры поиска
def connect(type :str, search = dict()) -> list[dict]:

    # заполнение данных дл авторизации
    connect = HTTPSConnection("table.nsu.ru")
    userAndPass = b64encode(TABLE_TOKEN).decode("utf-8")
    headers = { "Authorization" : "Basic %s" %  userAndPass }

    # собираем строку поиска
    string_of_find = ""
    if search != dict():
        string_of_find = "/search?"+"&".join([elem+"="+search[elem] for elem in search.keys()])

    # посылаем запрос
    connect.request('GET', links[type]+string_of_find, headers=headers)
    res = connect.getresponse()
    data = res.read()

    # возвращаем ответ в виде массива словарей
    return json.loads(data.decode("utf-8"))

# example: print(connect("faculty",{"id":"1"}))
