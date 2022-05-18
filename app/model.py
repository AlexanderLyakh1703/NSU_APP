

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
        self.id_teacher = kwargs["id_teacher"]
        self.type = kwargs["type"]
        self.weekday = kwargs["weekday"]

        # чётность пары
        self.even = ["even", "odd"][kwargs["weekday"] > 7]

        if isinstance(kwargs["id_group"], list):
            self.id_list_groups = kwargs["id_group"]
        else:
            self.id_list_groups = [kwargs["id_group"]]

        self.id_time = kwargs["id_time"]
        self.room = kwargs["roomsokr"]


# # Order.shedule[weekday][time]
# # по существу, это понедельный календарь
class Order:

    # предполагается передача массива, состоящего из Lesson
    def __init__(self, list_Of_Lesson: list[Lesson]):

        self.schedule = {
            lesson_.weekday: {lesson.id_time: lesson for lesson in list_Of_Lesson}
            for lesson_ in list_Of_Lesson
        }
        # self.calendar = ... - это на будущее
