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
        self.even = ["even","odd"][kwargs['weekday']>7]

        if kwargs['id_groups'] is list:
            self.id_list_group = kwargs['id_groups']
        else:
            self.id_list_group = [ kwargs['id_groups'] ]

        self.id_time = kwargs['id_time']
        self.room = kwargs['roomsokr']

    def presentation(self):

        teacher_name = connect("teacher",{"id":self.id_teacher})[0]["name"]
        type_lesson_name = connect("type-occupation",{"id":self.id_type_lesson})[0]["abbr"]
        weekday_name = {0:"ВОСКРЕСЕНЬЕ",1:"ПОНЕДЕЛЬНИК",2:"ВТОРНИК",3:"СРЕДА",
                        4:"ЧЕТВЕРГ",5:"ПЯТНИЦА",6:"СУББОТА"}[self.weekday%7]

        even_name = self.even

        list_group_names = []
        for id_group in self.id_list_group:
            group_name = connect("group",{"id":id_group})[0]["name"]
            list_group_names.append(group_name)

        request_for_time = connect("time",{"id":self.id_time})[0]

        fast_lesson_name = connect("schedule",{"id_teacher":self.id_teacher,
                                        "id_time":self.id_time,"weekday":self.weekday})["namesokr"]

        time_name = {"begin":request_for_time["begin"],
                     "end":request_for_time["end"]}
        room_name = self.room

        return {"teacher":teacher_name,"type":type_lesson,
                "weekday":weekday_name,"even":even_name,
                "groups":list_group_names,"time":time_name,
                "room":room_name,"name":fast_lesson_name}


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
