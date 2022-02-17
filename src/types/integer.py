from .base import BaseDataType


class Integer(BaseDataType):
    def serialize(self, data):
        return str(data)

    def deserialize(self, raw: str):
        return int(raw)
