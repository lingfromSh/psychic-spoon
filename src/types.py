import decimal
from datetime import timedelta
from typing import Any, AnyStr, Dict, List


class DataType:
    def activate(self, backend):
        backend.set_mode(self)


class String(DataType):
    def get(self, backend, key: AnyStr) -> str:
        print(self)
        return backend.get(key)

    def mget(self, backend, keys: List[AnyStr]) -> str:
        return {key: data for key, data in zip(keys, backend.mget(*keys))}

    def add(self, backend, key: AnyStr, data: AnyStr, ttl: timedelta = None) -> bool:
        return backend.add(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)


class Number(DataType):
    def get(self, backend, key: AnyStr) -> Any:
        return backend.get(key)

    def mget(self, backend, keys: List[AnyStr]) -> Dict[AnyStr, Any]:
        return {key: data for key, data in zip(keys, backend.mget(*keys))}

    def add(self, backend, key: AnyStr, data: Any, ttl: timedelta = None) -> bool:
        print(dir(backend))
        return backend.add(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)

    def plus(self, backend, key: AnyStr, value) -> bool:
        return backend.plus(key, value)

    def subtract(self, backend, key: AnyStr, value) -> bool:
        return backend.subtract(key, value)


class Integer(Number):
    def plus(self, backend, key: AnyStr, value: int) -> bool:
        return backend.plus(key, value)

    def subtract(self, backend, key: AnyStr, value: int) -> bool:
        return backend.subtract(key, value)


class Float(Number):
    def plus(self, backend, key: AnyStr, value: float) -> bool:
        return backend.plus(key, value)

    def subtract(self, backend, key: AnyStr, value: float) -> bool:
        return backend.subtract(key, value)


class Decimal(Number):
    def plus(self, backend, key: AnyStr, value: decimal.Decimal) -> bool:
        return backend.plus(key, value)

    def subtract(self, backend, key: AnyStr, value: decimal.Decimal) -> bool:
        return backend.subtract(key, value)


class Boolean(DataType):
    def get(self, backend, key: AnyStr) -> bool:
        return backend.get(key)

    def mget(self, backend, keys: List[AnyStr]) -> Dict[AnyStr, bool]:
        return {key: data for key, data in zip(keys, backend.mget(*keys))}

    def add(self, backend, key: AnyStr, data: bool, ttl: timedelta = None) -> bool:
        return backend.add(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)


# class Set(DataType):
#
#     def get(self, backend, key: AnyStr) -> set:
#         return backend.get(key)
#
#     def mget(self, backend, keys: List[AnyStr]) -> Dict[AnyStr, set]:
#         return {key: data for key, data in zip(keys, backend.mget(*keys))}
#
#     def set(self, backend, key: AnyStr, data: set, ttl: timedelta = None) -> bool:
#         return backend.set(key, data, ttl=ttl)
#
#     def add(self, backend, key: AnyStr, data: set) -> bool:
#         return backend.add(key, data)
#
#     def delete(self, backend, *keys: AnyStr) -> bool:
#         return backend.delete(*keys)
#
#     def pop(self, backend, key: AnyStr, data: set) -> set:
#         return backend.pop(key, data)
#
#     def union(self, backend, *keys) -> set:
#         return backend.union(*keys)
#
#     def intersection(self, backend, *keys) -> set:
#         return backend.intersection(*keys)
