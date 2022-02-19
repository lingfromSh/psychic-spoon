from datetime import timedelta
from inspect import getmembers, isfunction
from types import MethodType
from typing import List as TypingList

from redis import StrictRedis

from ..types import Boolean, Dict, Float, Integer, List, Set, String
from .base import Backend


class RedisBackend(Backend):
    __registry__ = {}

    def __init__(self, host, port, db, password=None):
        super(RedisBackend, self).__init__()
        self.redis_client = StrictRedis(host=host, port=port, db=db, password=password)

    def __init_subclass__(cls, **kwargs):
        RedisBackend.__registry__.update({kwargs["mode"]: cls})

    def get(self, key) -> str:
        return self.data_type.deserialize(self.redis_client.get(key).decode())

    def mget(self, *keys) -> TypingList[str]:
        return [
            self.data_type.deserialize(item.decode())
            for item in self.redis_client.mget(keys)
        ]

    def set(self, key, value, ttl: timedelta = None) -> bool:
        return self.redis_client.set(key, self.data_type.serialize(value), ex=ttl)

    def delete(self, *keys) -> bool:
        return self.redis_client.delete(*keys) == len(keys)

    def expire(self, key, ttl: timedelta = None):
        return self.redis_client.expire(key, time=ttl)

    def ready_for(self, data_type):
        super(RedisBackend, self).ready_for(data_type)
        template = RedisBackend.__registry__[data_type.__class__]
        for name, method in getmembers(template, predicate=isfunction):
            setattr(self, name, MethodType(method, self))


class RedisStringBackend(RedisBackend, mode=String):
    ...


class RedisIntegerBackend(RedisBackend, mode=Integer):
    def plus(self, key, value):
        return self.redis_client.incr(key, value)

    def subtract(self, key, value):
        return self.redis_client.decr(key, value)


class RedisFloatBackend(RedisBackend, mode=Float):
    def plus(self, key, value):
        return self.redis_client.incrbyfloat(key, value)

    def subtract(self, key, value):
        return self.redis_client.incrbyfloat(key, -value)


class RedisBooleanBackend(RedisBackend, mode=Boolean):
    ...


class RedisListBackend(RedisBackend, mode=List):
    def get(self, key) -> list:
        return self.data_type.deserialize(
            self.redis_client.lrange(key, start=0, end=-1)
        )

    def mget(self, *keys) -> TypingList:
        return [
            self.data_type.deserialize(self.redis_client.lrange(key, start=0, end=-1))
            for key in keys
        ]

    def set(self, key, value, ttl: timedelta = None) -> bool:
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
        if ttl:
            self.redis_client.rpush(key, *value)
            return self.redis_client.expire(key, time=ttl)
        else:
            return self.redis_client.rpush(key, *value) == len(value)


class RedisSetBackend(RedisBackend, mode=Set):
    def get(self, key) -> set:
        return self.data_type.deserialize(self.redis_client.smembers(key))

    def mget(self, *keys) -> TypingList[set]:
        return [
            self.data_type.deserialize(self.redis_client.smembers(key)) for key in keys
        ]

    def set(self, key, value, ttl: timedelta = None) -> bool:
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
        if ttl:
            self.redis_client.sadd(key, *self.data_type.serialize(value))
            return self.redis_client.expire(key, time=ttl)
        else:
            return self.redis_client.sadd(key, *self.data_type.serialize(value)) == len(
                value
            )

    def add(self, key, *values) -> bool:
        return self.redis_client.sadd(key, *self.data_type.serialize(values)) == len(
            values
        )

    def remove(self, key, *values):
        return self.redis_client.srem(key, *self.data_type.serialize(values))

    def union(self, *keys):
        return self.data_type.deserialize(self.redis_client.sunion(keys))

    def intersection(self, *keys):
        return self.data_type.deserialize(self.redis_client.sinter(keys))


class RedisDictBackend(RedisBackend, mode=Dict):
    ...
