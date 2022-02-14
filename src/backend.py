from datetime import timedelta
from typing import Any, Mapping, Optional

from redis import StrictRedis

from .constants import (
    PSYCHIC_SPOON_REDIS_DB,
    PSYCHIC_SPOON_REDIS_HOST,
    PSYCHIC_SPOON_REDIS_PASSWORD,
    PSYCHIC_SPOON_REDIS_PORT,
)


class Backend:
    def __init__(self, client: StrictRedis = None, ttl: Optional[timedelta] = None):
        self.ttl = ttl

        if client is None:
            client = StrictRedis(
                host=PSYCHIC_SPOON_REDIS_HOST,
                port=PSYCHIC_SPOON_REDIS_PORT,
                db=PSYCHIC_SPOON_REDIS_DB,
                password=PSYCHIC_SPOON_REDIS_PASSWORD,
            )
        self.client = client

    def add(self, key: str, data: Any, ttl: timedelta = None):
        return self.client.set(key, data, ex=ttl)

    def bulk_add(self, mapping: dict):
        return self.client.mset(mapping)

    def get(self, *keys) -> Mapping:
        return {key: data.decode() for key, data in zip(keys, self.client.mget(keys))}

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(self.client, name)
