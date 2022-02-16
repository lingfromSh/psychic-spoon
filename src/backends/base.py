from inspect import isfunction
from types import MethodType


class Backend:
    ModeMapping = {}

    def __init__(self, mode=None):
        self.mode = mode

    def set_mode(self, mode):
        if isinstance(mode, type):
            methods = self.ModeMapping[mode]
        else:
            methods = self.ModeMapping[mode.__class__]
        print(methods.get)
        self.update_methods(methods)

    def update_methods(self, methods: object):
        for name, attribute in methods.__dict__.items():
            if not isfunction(attribute):
                continue
            setattr(self, name, MethodType(attribute, self))
