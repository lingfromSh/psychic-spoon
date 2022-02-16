from datetime import timedelta
from typing import AnyStr, Dict

from redis import StrictRedis

from ..types import String
from .base import Backend


class RedisStringMixin:
    def get(self, key: AnyStr) -> AnyStr:
        return self.redis_client.get(key).decode()

    def mget(self, *keys: AnyStr) -> Dict[AnyStr, AnyStr]:
        return {
            key: data.decode() for key, data in zip(keys, self.redis_client.mget(keys))
        }

    def add(self, key: AnyStr, data: AnyStr, ttl: timedelta = None) -> bool:
        return self.redis_client.add(name=key, value=data, ex=ttl)

    def delete(self, *keys: AnyStr) -> bool:
        return bool(self.redis_client.delete(*keys))


class RedisBackend(Backend):
    ModeMapping = {String: RedisStringMixin}

    def __init__(self, host, port, db, password=None, mode=None):
        super(RedisBackend, self).__init__(mode)
        self.redis_client = StrictRedis(host=host, port=port, db=db, password=password)
