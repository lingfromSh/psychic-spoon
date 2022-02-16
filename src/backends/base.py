from inspect import getmembers, isfunction
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
        self.update_methods(methods)

    def update_methods(self, methods: object):
        for name, attribute in getmembers(methods, predicate=isfunction):
            print(name, attribute)
            setattr(self, name, MethodType(attribute, self))
