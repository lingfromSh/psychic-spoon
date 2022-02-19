from typing import Union

import orjson

from .base import BaseDataType, ContainerDataType


class Dict(ContainerDataType):
    def __init__(self, **fields):
        self.field_mapping = {}
        for field_name, field in fields.items():
            if isinstance(field, (BaseDataType, ContainerDataType)):
                self.field_mapping.update({field_name: field})
            else:
                continue

    def serialize(self, data: dict) -> str:
        return orjson.dumps(
            {
                field_name: field.serialize(data.get(field_name))
                for field_name, field in self.field_mapping.items()
            }
        ).decode()

    def deserialize(self, raw: Union[str, dict]):
        if isinstance(raw, str):
            raw = orjson.loads(raw)
        return {
            k: self.field_mapping[k].deserialize(v) if k in self.field_mapping else v
            for k, v in raw.items()
        }
