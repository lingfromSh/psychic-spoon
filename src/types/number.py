from decimal import Decimal

from .string import String


class Number(String):
    PyType = (int, float, Decimal)

    def serialize(self, data: PyType) -> str:
        return str(data)

    def deserialize(self, raw) -> PyType:
        for type_ in self.PyType:
            try:
                return type_(raw)
            except TypeError:
                pass

        raise TypeError(f"Expected type in {self.PyType}, but got {raw}.")
