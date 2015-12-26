from exceptions import Exception


class PlantNotFoundException(Exception):

    def __init__(self, msg, uid):
        self.msg = msg
        self.uid = uid

    def __str__(self):
        return repr(self.msg) + ": " + repr(self.uid)

