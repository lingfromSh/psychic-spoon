from __future__ import annotations

from datetime import timedelta
from typing import AnyStr, Callable, Dict, List, Union

from .types.base import Type


class DefaultTTL:
    pass


class Key:
    def __init__(
        self,
        name: Union[str, Callable],
        data_type: Type,
        ttl: timedelta = DefaultTTL,
        fail_callback: List[Callable] = None,
        success_callback: List[Callable] = None,
    ):
        """

        :param name: Union[str, Callable]
        :param type_cls:Type
        :param ttl: timedelta
        :param fail_callback:
        :param success_callback:
        """
        assert isinstance(name, str) or callable(name), "name must be str or Callable."
        assert isinstance(data_type, Type), "data_type must be subclass of Type."
        assert (
            isinstance(ttl, timedelta) or ttl is DefaultTTL
        ), "ttl must be type of timedelta."
        assert (
            fail_callback is None
            or isinstance(fail_callback, list)
            and all(map(callable, fail_callback))
        ), "fail_callback must be a list of callable or None."
        assert (
            success_callback is None
            or isinstance(success_callback, list)
            and all(map(callable, success_callback))
        ), "success_callback must be a list of callable or None."

        self.name = name
        self.data_type = data_type
        self.ttl = ttl
        self.fail_callback = fail_callback
        self.success_callback = success_callback
        self._cache = None

    def build_key(self, **kwargs) -> str:
        if isinstance(self.name, str):
            return self.name.format(**kwargs)
        else:
            return self.name(**kwargs)

    def get(self, **key_mapping) -> "Type":
        key = self.build_key(**key_mapping)
        return self.data_type.get(key)

    def mget(self, key_mappings: List[Dict[str, AnyStr]]) -> List["Type"]:
        return self.data_type.mget(
            *[self.build_key(**key_mapping) for key_mapping in key_mappings]
        )

    def add(self, mapping: dict) -> bool:
        ...

    def save(self, data, ttl: int = None) -> bool:
        ...

    def delete(self) -> bool:
        ...
