from .base import BaseDataType


class Boolean(BaseDataType):
    def serialize(self, data: bool):
        return str(data)

    def deserialize(self, raw: str):
        return eval(raw)
