from .base import Type


class Set(Type):
    PyType = set

    def serialize(self, data) -> PyType:
        return set(data)

    def deserialize(self, raw) -> PyType:
        return set(raw)
