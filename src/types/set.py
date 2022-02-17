from typing import Union

import orjson

from .base import BaseDataType, ContainerDataType


class Set(ContainerDataType):
    def __init__(self, base_type):
        if not isinstance(base_type, (BaseDataType, ContainerDataType)):
            raise ValueError(
                "base_type must be type of (BaseDataType, ContainerDataType)."
            )
        self.base_type = base_type

    def serialize(self, data: set):
        return {self.base_type.serialize(item) for item in data}

    def deserialize(self, raw: Union[str, set]):
        if isinstance(raw, str):
            raw = orjson.loads(raw)

        return {self.base_type.deserialize(item) for item in raw}
