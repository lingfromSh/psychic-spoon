from .base import Type


class String(Type):
    PyType = str

    def serialize(self, data) -> str:
        return data

    def deserialize(self, raw) -> PyType:
        return raw
