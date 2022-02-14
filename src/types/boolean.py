from .string import String


class Boolean(String):
    PyType = bool

    def serialize(self, data):
        assert isinstance(
            data, self.PyType
        ), f"Expected type of {self.PyType}, but got {type(data)}"
        return str(bool(data))

    def deserialize(self, raw: str):
        return eval(raw)
