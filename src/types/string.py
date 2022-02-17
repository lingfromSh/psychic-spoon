from .base import BaseDataType


class String(BaseDataType):
    def serialize(self, data):
        return str(data)

    def deserialize(self, raw: str):
        if isinstance(raw, str):
            return raw
        return str(str)
