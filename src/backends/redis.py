import decimal
from datetime import timedelta
from typing import AnyStr, List, Union

from redis import StrictRedis

from ..types import Boolean, Decimal, Float, Integer, Set, String
from .base import Backend


class RedisStringMixin:
    def get(self, key: AnyStr) -> AnyStr:
        return self.redis_client.get(key).decode()

    def mget(self, *keys: AnyStr) -> List[AnyStr]:
        return [data.decode() for data in self.redis_client.mget(keys)]

    def add(self, key: AnyStr, data: AnyStr, ttl: timedelta = None) -> bool:
        return self.redis_client.set(name=key, value=data, ex=ttl)

    def delete(self, *keys: AnyStr) -> bool:
        return bool(self.redis_client.delete(*keys))


class RedisNumberMixin:
    def add(
        self,
        key: AnyStr,
        data: Union[int, float, decimal.Decimal],
        ttl: timedelta = None,
    ) -> bool:
        return self.redis_client.set(name=key, value=str(data), ex=ttl)

    def delete(self, *keys: AnyStr) -> bool:
        return bool(self.redis_client.delete(*keys))

    def get(self, key: AnyStr) -> int:
        return self.redis_client.get(key).decode()

    def mget(self, *keys: AnyStr) -> List[int]:
        return [data.decode() for data in self.redis_client.mget(keys)]


class RedisIntegerMixin(RedisNumberMixin):
    def plus(self, key: AnyStr, value: int) -> int:
        return self.redis_client.incr(key, value)

    def subtract(self, key: AnyStr, value: int) -> int:
        return self.redis_client.decr(key, value)


class RedisFloatMixin(RedisNumberMixin):
    def plus(self, key: AnyStr, value: float) -> float:
        new_value = float(self.get(key)) + value
        return self.add(key, data=new_value) and new_value

    def subtract(self, key: AnyStr, value: float) -> float:
        new_value = float(self.get(key)) - value
        return self.add(key, data=new_value) and new_value


class RedisDecimalMixin(RedisNumberMixin):
    def plus(self, key: AnyStr, value: decimal.Decimal) -> decimal.Decimal:
        new_value = decimal.Decimal(self.get(key)) + value
        return self.add(key, data=new_value) and new_value

    def subtract(self, key: AnyStr, value: decimal.Decimal) -> decimal.Decimal:
        new_value = decimal.Decimal(self.get(key)) - value
        return self.add(key, data=new_value) and new_value


class RedisBooleanMixin:
    def get(self, key: AnyStr) -> bool:
        return self.redis_client.get(key).decode()

    def mget(self, *keys: AnyStr) -> List[bool]:
        return [data.decode() for data in self.redis_client.mget(keys)]

    def add(self, key: AnyStr, data: bool, ttl: timedelta = None) -> bool:
        return self.redis_client.set(name=key, value=data, ex=ttl)

    def delete(self, *keys: AnyStr) -> bool:
        return bool(self.redis_client.delete(*keys))


class RedisSetMixin:
    def get(self, key: AnyStr) -> set:
        return {item.decode() for item in self.redis_client.smembers(key)}

    def mget(self, *keys: List[AnyStr]) -> List[set]:
        return [self.redis_client.smembers(key) for key in keys]

    def set(self, key: AnyStr, data: set, ttl: timedelta = None) -> bool:
        resp = self.redis_client.sadd(key, *data)
        if ttl:
            resp = resp and self.redis_client.expire(key, ttl)
        return resp

    def add(self, key: AnyStr, data: set) -> bool:
        return self.redis_client.sadd(key, *data)

    def delete(self, *keys: AnyStr) -> bool:
        return self.redis_client.delete(*keys)

    def pop(self, key: AnyStr, data: set) -> set:
        return self.redis_client.srem(key, *data)

    def union(self, *keys) -> set:
        print({item.decode() for item in self.redis_client.sunion(keys)})
        return {item.decode() for item in self.redis_client.sunion(keys)}

    def intersection(self, *keys) -> set:
        print({item.decode() for item in self.redis_client.sinter(keys)})
        return {item.decode() for item in self.redis_client.sinter(keys)}


class RedisBackend(Backend):
    ModeMapping = {
        String: RedisStringMixin,
        Integer: RedisIntegerMixin,
        Float: RedisFloatMixin,
        Decimal: RedisDecimalMixin,
        Boolean: RedisBooleanMixin,
        Set: RedisSetMixin,
    }

    def __init__(self, host, port, db, password=None, mode=None):
        super(RedisBackend, self).__init__(mode)
        self.redis_client = StrictRedis(host=host, port=port, db=db, password=password)
