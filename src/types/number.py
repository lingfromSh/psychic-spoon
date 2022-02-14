from decimal import Decimal as PyDecimal

from .string import String


class Number(String):
    PyType = NotImplemented

    def serialize(self, data) -> str:
        return str(data)

    def deserialize(self, raw) -> PyType:
        return self.PyType(raw)


class Integer(Number):
    PyType = int


class Float(Number):
    PyType = float


class Decimal(Number):
    PyType = PyDecimal

    def serialize(self, data) -> str:
        return data.to_eng_string()

    def deserialize(self, raw) -> PyType:
        return PyDecimal(raw)
