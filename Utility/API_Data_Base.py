import requests

token = "SCFFAtHIAFhTa4HOBoAvOgqMDqq8uOBd_1648434328"
links = {
    "faculty":"table.nsu.ru/api/faculties",
    "teacher":"table.nsu.ru/api/teachers",
    "group":"table.nsu.ru/api/groups",
    "time":"table.nsu.ru/api/times",
    "type-occupation":"table.nsu.ru/api/type-occupations",
    "parity":"table.nsu.ru/api/parities",
    "term":"table.nsu.ru/api/terms",
    "exam-group":"table.nsu.ru/api/exam-groups",
    "schedule":"table.nsu.ru/api/schedules",
}

# запрос links["<type_information>"] + "/search?" + ...

def get_Time_By_IdTime(id_time :str):
    link_request = links["time"] + "/search?" +

def get_smb():
    ...
