import json
import sys
from config import api_config as aconf
import requests
from datetime import datetime
import asyncio as ai
import concurrent.futures

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

def make_url(type_,search=None):

    string_of_find = ""

    if search:
        string_of_find = "/search?" + "&".join(
            [str(key) + "=" + str(value) for key, value in search.items()]
        )

    url = "https://table.nsu.ru" + links[type_] + string_of_find

    return url


def get_or_create_eventloop():
    try:
        return ai.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = ai.new_event_loop()
            ai.set_event_loop(loop)
            return ai.get_event_loop()


def async_get_jsons(urls, max_workers=100, **kwargs):

    result = []

    async def get_urls():
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

            loop = ai.get_event_loop()
            futures = [
                loop.run_in_executor(executor, lambda: requests.get(url, **kwargs))
                for url in urls
            ]
            for response in await ai.gather(*futures):
                obj = json.loads(response.text)
                print(response, file=sys.stderr)
                result.append(obj)

    loop = get_or_create_eventloop()
    loop.run_until_complete(get_urls())
    return result


def get_jsons(urls, **kwargs):
    result = []
    for url in urls:
        response = requests.get(url, **kwargs)
        result.append(json.loads(response.text))
        print(response, file=sys.stderr)
    return result

def get_role(user):
        if 'groups' in user and 'StudentGroups' in user['groups']:
            return 'student'
        return 'teacher'

def get_info(session):
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

    role = get_role(user)

    if role == 'student':
        print('MESSAGE: You are student!')

        url = make_url('group',{'name':user['groups']['StudentGroups']})
        id_group = async_get_jsons([url],auth=(aconf.TABLE_TOKEN, ""))[0][0]['id']
        url = make_url('schedule',{'id_group':id_group})
        Info = async_get_jsons([url],auth=(aconf.TABLE_TOKEN, ""))[0]
        urls = []
        for elem in Info:
            time = make_url('time',{'id':elem['id_time']})
            teacher_name = make_url('teacher',{'id':elem['id_teacher']})
            urls.append(time)
            urls.append(teacher_name)

        request_time_and_teacher = async_get_jsons( urls,
                                            auth=(aconf.TABLE_TOKEN, "") )

        for pos in range(len(request_time_and_teacher)):
            Info[pos//2]['time' if pos%2 == 0 else 'teacher'] = request_time_and_teacher[pos]

        url = make_url('parity')
        even = async_get_jsons(url, auth=(aconf.TABLE_TOKEN, "") )[0]["actual"]

        return Info,role,even


    # elif role == 'teacher':
    #     print('MESSAGE: You are teacher!')
    #
    #
    # else:
    #     print('ERROR: You have not role')
