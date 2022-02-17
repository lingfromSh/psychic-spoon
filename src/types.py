import decimal
from datetime import timedelta
from typing import Any, AnyStr, List


class BasicDataType:
    def activate(self, backend):
        backend.set_mode(self)

    def get(self, backend, key: AnyStr) -> set:
        return self.to_python(backend.get(key))

    def mget(self, backend, keys: List[AnyStr]) -> str:
        return {
            key: self.to_python(data) for key, data in zip(keys, backend.mget(*keys))
        }

    def to_raw(self, data):
        raise NotImplementedError("Must be implemented by its subclass.")

    def to_python(self, data):
        raise NotImplementedError("Must be implemented by its subclass.")


class String(BasicDataType):
    def add(self, backend, key: AnyStr, data: AnyStr, ttl: timedelta = None) -> bool:
        return backend.add(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)

    def to_raw(self, data):
        return str(data)

    def to_python(self, data):
        return data


class Number(BasicDataType):
    def add(self, backend, key: AnyStr, data: Any, ttl: timedelta = None) -> bool:
        return backend.add(key, self.to_raw(data), ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)

    def plus(self, backend, key: AnyStr, value) -> bool:
        return backend.plus(key, value)

    def subtract(self, backend, key: AnyStr, value) -> bool:
        return backend.subtract(key, value)


class Integer(Number):
    def to_raw(self, data):
        if isinstance(data, int):
            return data
        return int(data)

    def to_python(self, data):
        return int(data)


class Float(Number):
    def to_raw(self, data):
        if isinstance(data, float):
            return data
        return float(data)

    def to_python(self, data):
        return float(data)


class Decimal(Number):
    def to_raw(self, data):
        if not isinstance(data, decimal.Decimal):
            return data
        return str(data)

    def to_python(self, data):
        return decimal.Decimal(data)


class Boolean(BasicDataType):
    def add(self, backend, key: AnyStr, data: bool, ttl: timedelta = None) -> bool:
        return backend.add(key, self.to_raw(data), ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)

    def to_raw(self, data):
        if isinstance(data, bool):
            return str(data)
        return data

    def to_python(self, data):
        return eval(data)


class ContainerDataType(BasicDataType):
    def __init__(self, base_data_type: BasicDataType):
        if not isinstance(base_data_type, BasicDataType):
            raise ValueError("base_data_type must be type of BasicDataType.")
        self.base_data_type = base_data_type

    def to_raw(self, data):
        return {self.base_data_type.to_raw(item) for item in data}

    def to_python(self, data):
        return {self.base_data_type.to_python(item) for item in data}


class Set(ContainerDataType):
    def add(self, backend, key: AnyStr, data: set) -> bool:
        return backend.add(key, data)

    def set(self, backend, key: AnyStr, data: set, ttl: timedelta = None) -> bool:
        return backend.set(key, data, ttl=ttl)

    def delete(self, backend, *keys: AnyStr) -> bool:
        return backend.delete(*keys)

    def pop(self, backend, key: AnyStr, data: set) -> set:
        return backend.pop(key, data)

    def union(self, backend, *keys) -> set:
        return self.to_python(backend.union(*keys))

    def intersection(self, backend, *keys) -> set:
        return self.to_python(backend.intersection(*keys))
