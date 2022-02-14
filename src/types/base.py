from datetime import timedelta
from typing import Dict

from ..backend import Backend


class Type:
    PyType = None

    def __init__(self, backend: Backend = None):
        if backend is None:
            backend = Backend()
        self.backend = backend

    def serialize(self, data):
        raise NotImplementedError("Must be implemented by subclass.")

    def deserialize(self, raw):
        raise NotImplementedError("Must be implemented by subclass.")

    def get(self, key: str) -> PyType:
        return self.deserialize(self.backend.get(key)[key])

    def mget(self, *keys) -> Dict[str, PyType]:
        return {
            key: self.deserialize(data) for key, data in self.backend.get(*keys).items()
        }

    def add(self, key, data, ttl: timedelta = None) -> bool:
        return self.backend.add(key, self.serialize(data), ttl)

    def bulk_add(self, mapping: Dict[str, PyType]) -> bool:
        return self.backend.bulk_add(
            {key: self.serialize(data) for key, data in mapping.items()}
        )

    def delete(self, *keys) -> bool:
        return self.backend.delete(*keys)
