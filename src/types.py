from datetime import timedelta
from typing import AnyStr, List


class DataType:
    def activate(self, backend):
        backend.set_mode(self)


class String(DataType):
    def get(self, backend, key: AnyStr) -> str:
        return backend.get(key)

    def mget(self, backend, keys: List[AnyStr]) -> str:
        return backend.mget(keys=keys)

    def add(self, backend, key: AnyStr, data: AnyStr, ttl: timedelta = None) -> bool:
        return backend.add(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(keys)
