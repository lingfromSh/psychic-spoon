from __future__ import annotations

from datetime import timedelta
from typing import Any, AnyStr, Callable, Dict, List, TypedDict, Union

from .backend import Backend
from .types.base import Type

PyType = str

Mapping = TypedDict("Mapping", key_mapping=dict, data=PyType)


default_ttl = timedelta(minutes=1)


class Key:
    def __init__(
        self,
        name: Union[str, Callable],
        data_type: Type,
        backend: Backend = None,
        ttl: timedelta = default_ttl,
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
            isinstance(ttl, timedelta) or ttl is default_ttl
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

    def add(self, *, key_mapping: dict, data: Any) -> bool:
        return self.data_type.add(
            key=self.build_key(**key_mapping), data=data, ttl=self.ttl
        )

    def bulk_add(self, *, mappings: List[Mapping]) -> bool:
        return self.data_type.bulk_add(
            {
                self.build_key(**mapping["key_mapping"]): mapping["data"]
                for mapping in mappings
            }
        )

    def delete(self, *key_mappings: List[Dict[str, AnyStr]]) -> bool:
        return self.data_type.delete(
            *[self.build_key(**key_mapping) for key_mapping in key_mappings]
        )
