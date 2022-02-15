from .string import String

try:
    from orjson import dumps, loads
except ImportError:
    from json import dumps, loads


class Dict(String):
    PyType = dict

    def __init__(self, **field_mapping):
        self.field_mapping = field_mapping

    def validate(self):
        pass
