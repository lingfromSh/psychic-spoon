from datetime import timedelta
from typing import Union

from redis import Redis

from psychic_spoon.backends.base import Backend
from psychic_spoon.converter import get_converter
from psychic_spoon.types.base import PythonType


class RedisBackend(Backend):
    type = NotImplemented

    def __init__(self, host, port=6379, db=0, username=None, password=None):
        super(RedisBackend, self).__init__()
        self.client = Redis(
            host=host, port=port, db=db, username=username, password=password
        )


class RedisStringBackend(RedisBackend):
    type = str

    def set(self, key, value: Union[PythonType, type], ttl: timedelta = None):
        if isinstance(value, PythonType):
            value = value.encode(self.type)
        else:
            value = get_converter(self.type).convert(value)
        self.client.set(key, value, ex=ttl)

    def get(self, key):
        if data := self.client.get(key):
            return self.target_type(data)
        return None

    def expire(self, key, ttl: timedelta = None):
        self.client.expire(key, time=ttl)


if __name__ == "__main__":
    backend = RedisStringBackend("localhost", port=49153)
    import inspect

    print(inspect.getfullargspec(backend.get))
    print(inspect.getfullargspec(backend.set))
    print(inspect.getfullargspec(backend.expire))
