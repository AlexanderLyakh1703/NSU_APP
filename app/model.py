class Lesson:
    # параметры для поиска одной пары:

    # под преподавателем
    id_teacher: str
    id_time: str
    weekday: str

    # под студентом
    # конкретно одна группа
    id_list_group: list[str]

    id_type_lesson: str
    room: str

    def __init__(self, **kwargs):
        # self.id - не имеет смысла
        self.id_teacher = kwargs['id_teacher']
        self.id_type_lesson = kwargs['id_type_lesson']
        self.weekday = kwargs['weekday']

        # чётность пары
        self.even = kwargs['even']

        if kwargs['id_groups'] is list:
            self.id_list_group = kwargs['id_groups']
        else:
            self.id_list_group = [ kwargs['id_groups'] ]

        self.id_time = kwargs['id_time']
        self.room = kwargs['room']


# Order.shedule[weekday][time]
# по существу, это понедельный календарь
class Order:

    # предполагается передача массива, состоящего из Lesson
    def __init__(self, list_Of_Lesson: list[Lesson]):

        self.schedule = {lesson_.weekday: {
                        lesson.id_time: lesson for lesson in list_Of_Lesson}
                        for lesson_ in list_Of_Lesson}
        # self.calendar = ... - это на будущее

class User:
    def __init__(self, **kwargs):
        # self.openid = kwargs['openid']
        self.phone = kwargs['phone']
        self.offline_access = kwargs['offline_access']
        self.roles = kwargs['roles']
        self.address = kwargs['address']
        self.microprofile_jwt = kwargs['microprofile_jwt']
        self.web_origins = kwargs['web_origins']
        self.email = kwargs['email']
        # self.profile = kwargs['profile'] - this atribute is being clarified
        self.groups = kwargs['groups']
