import decimal
from datetime import timedelta
from typing import AnyStr, List, Union

from redis import StrictRedis

from ..types import Boolean, Decimal, Float, Integer, String
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


class RedisIntegerMixin(RedisNumberMixin):
    def get(self, key: AnyStr) -> int:
        return int(self.redis_client.get(key).decode())

    def mget(self, *keys: AnyStr) -> List[int]:
        return [int(data.decode()) for data in self.redis_client.mget(keys)]

    def plus(self, key: AnyStr, value: int) -> int:
        return self.redis_client.incr(key, value)

    def subtract(self, key: AnyStr, value: int) -> int:
        return self.redis_client.decr(key, value)


class RedisFloatMixin(RedisNumberMixin):
    def get(self, key: AnyStr) -> float:
        return float(self.redis_client.get(key).decode())

    def mget(self, *keys: AnyStr) -> List[float]:
        return [float(data.decode()) for data in self.redis_client.mget(keys)]

    def plus(self, key: AnyStr, value: float) -> float:
        new_value = self.get(key) + value
        return self.add(key, data=new_value) and new_value

    def subtract(self, key: AnyStr, value: float) -> float:
        new_value = self.get(key) - value
        return self.add(key, data=new_value) and new_value


class RedisDecimalMixin(RedisNumberMixin):
    def get(self, key: AnyStr) -> decimal.Decimal:
        return decimal.Decimal(self.redis_client.get(key).decode())

    def mget(self, *keys: AnyStr) -> List[decimal.Decimal]:
        return [decimal.Decimal(data.decode()) for data in self.redis_client.mget(keys)]

    def plus(self, key: AnyStr, value: decimal.Decimal) -> decimal.Decimal:
        new_value = self.get(key) + value
        return self.add(key, data=new_value) and new_value

    def subtract(self, key: AnyStr, value: decimal.Decimal) -> decimal.Decimal:
        new_value = self.get(key) - value
        return self.add(key, data=new_value) and new_value


class RedisBooleanMixin:
    def get(self, key: AnyStr) -> bool:
        return eval(self.redis_client.get(key).decode())

    def mget(self, *keys: AnyStr) -> List[bool]:
        return [eval(data.decode()) for data in self.redis_client.mget(keys)]

    def add(self, key: AnyStr, data: bool, ttl: timedelta = None) -> bool:
        return self.redis_client.set(name=key, value=str(data), ex=ttl)

    def delete(self, *keys: AnyStr) -> bool:
        return bool(self.redis_client.delete(*keys))


class RedisBackend(Backend):
    ModeMapping = {
        String: RedisStringMixin,
        Integer: RedisIntegerMixin,
        Float: RedisFloatMixin,
        Decimal: RedisDecimalMixin,
        Boolean: RedisBooleanMixin,
    }

    def __init__(self, host, port, db, password=None, mode=None):
        super(RedisBackend, self).__init__(mode)
        self.redis_client = StrictRedis(host=host, port=port, db=db, password=password)
