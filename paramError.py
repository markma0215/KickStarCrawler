
class ParamError(Exception):

    def __init__(self, *args):
        self.value = " ".join(arg for arg in args)

    def __str__(self):
        return self.value