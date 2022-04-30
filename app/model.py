class Lesson:
    # параметры для поиска:

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
        self.id_teacher = id_teacher
        self.id_type_lesson = id_type_lesson
        self.weekday = weekday

        # чётность пары
        self.even = even

        self.id_list_group = id_groups
        self.id_time = id_time
        self.room = room


# Order.shedule[weekday][time]
# по существу, это понедельный календарь
class Order:

    # предполагается передача массива, состоящего из Lesson
    def __init__(self, list_Of_Lesson: list[Lesson]):

        self.schedule = {weekday: dict() for weekday in range(1, 7)}
        # self.calendar = ... - это на будущее

        for lesson in list_Of_Lesson:
            # могут быть проблемы с отображением времени
            # из-за оперированием id_time, а не time
            self.schedule[lesson.weekday][lesson.id_time] = lesson

class User:
    def __init__(self, **kwargs):
        self.openid = id
        self.phone = id_group
        self.offline_access = id_faculty
        self.roles = roles
        self.address = address
        self.microprofile_jwt = microprofile_jwt
        self.web_origins = web_origins
        self.email = email
        self.profile = profile
        self.groups = groups
