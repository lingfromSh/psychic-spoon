from .string import String

try:
    from orjson import dumps, loads
except ImportError:
    from json import dumps, loads


class JSON(String):
    PyType = dict

    def __init__(self, fields=None, backend=None):
        super().__init__(backend=backend)
        self.fields = fields

    def serialize(self, data) -> str:
        return dumps(data)

    def deserialize(self, raw) -> PyType:
        return loads(raw)
