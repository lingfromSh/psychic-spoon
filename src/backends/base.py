from datetime import timedelta
from typing import Any, AnyStr, List

from ..types.base import Type
from ..utils import multipledispatch


class Backend:
    @multipledispatch
    def to_python(self, data_model, raw):
        raise NotImplementedError("Must be implemented by its subclass.")

    @multipledispatch
    def to_db(self, data_model, data):
        raise NotImplementedError("Must be implemented by its subclass.")

    def get(self, key: AnyStr, convert_type: Type = None):
        raise NotImplementedError("must be implemented by its subclass.")

    def mget(self, keys: List[AnyStr], convert_type: Type = None):
        raise NotImplementedError("must be implemented by its subclass.")

    def add(
        self, key: AnyStr, data: Any, data_type: Type, ttl: timedelta = None
    ) -> bool:
        raise NotImplementedError("must be implemented by its subclass.")

    def delete(self, keys: List[AnyStr]) -> bool:
        raise NotImplementedError("must be implemented by its subclass.")
