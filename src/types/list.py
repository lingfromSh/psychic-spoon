from typing import Union

import orjson

from .base import ContainerDataType


class List(ContainerDataType):
    def __init__(self, base_type):
        self.base_type = base_type

    def serialize(self, data: list) -> str:
        return orjson.dumps([self.base_type.serialize(item) for item in data]).decode()

    def deserialize(self, raw: Union[str, list]):
        if isinstance(raw, str):
            raw = orjson.loads(raw)

        return [self.base_type.deserialize(item) for item in raw]
