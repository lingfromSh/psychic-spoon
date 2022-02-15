from typing import Any, AnyStr, List, Dict as TypingDict
from datetime import timedelta

import orjson
from redis import StrictRedis
from .base import Backend
from ..types.base import Type
from ..types import String, Dict
from ..utils import multipledispatch


class RedisBackend(Backend):
    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        self.redis_client = StrictRedis(host=host, port=port, db=db, password=password)

    @multipledispatch
    def to_python(self, data_model, raw):
        print(data_model, raw)
        raise NotImplementedError("Must be implemented by its subclass.")

    @to_python.register
    def redis_string_to_string(self, data_model: String, raw: str) -> str:
        return raw

    @to_python.register
    def redis_string_to_dict(self, data_model: Dict, raw: str) -> dict:
        return orjson.loads(raw)

    @multipledispatch
    def to_db(self, data_model, data):
        raise NotImplementedError("Must be implemented by its subclass.")

    def get(self, key: AnyStr, convert_type: Type = None) -> Type:
        raw = self.redis_client.get(key).decode()
        return self.to_python(convert_type, raw)

    def mget(self, keys: List[AnyStr], convert_type: Type = None) -> TypingDict[AnyStr, Type]:
        raws = [item.decode() for item in self.redis_client.mget(keys)]
        return {key: self.to_python(convert_type, raw) for key, raw in zip(keys, raws)}

    def add(
            self, key: AnyStr, data: Any, data_type: Type, ttl: timedelta = None
    ) -> bool:
        return self.redis_client.set(
            name=key, value=self.to_db(data_type, data), ex=ttl
        )

    def delete(self, keys: List[AnyStr]) -> bool:
        return self.redis_client.delete(*keys) == len(keys)
