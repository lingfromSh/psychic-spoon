from .base import BaseDataType


class Float(BaseDataType):
    def serialize(self, data):
        if isinstance(data, float):
            return str(data)
        return str(float(data))

    def deserialize(self, raw: str):
        return float(raw)
