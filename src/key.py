from __future__ import annotations

from datetime import timedelta
from typing import Any, AnyStr, Callable, Dict, List, TypedDict, Union

from .backend import Backend
from .types.base import Type

PyType = str


class KeyParamDataMapping(TypedDict):
    key_params: Dict[str, Any]
    data: Any


default_ttl = timedelta(minutes=1)


class Key:
    def __init__(
        self,
        name: Union[str, Callable],
        data_type: Type,
        backend: Backend = None,
        ttl: timedelta = default_ttl,
        fail_callback_list: List[Callable] = None,
        success_callback_list: List[Callable] = None,
    ):
        """

        :param name:
        :param data_type:
        :param backend:
        :param ttl:
        :param fail_callback_list:
        :param success_callback_list:
        """
        assert isinstance(name, str) or callable(name), "name must be str or Callable."
        assert isinstance(data_type, Type), "data_type must be subclass of Type."
        assert (
            isinstance(ttl, timedelta) or ttl is default_ttl
        ), "ttl must be type of timedelta."
        assert (
            fail_callback_list is None
            or isinstance(fail_callback_list, list)
            and all(map(callable, fail_callback_list))
        ), "fail_callback_list must be a list of callable or None."
        assert (
            success_callback_list is None
            or isinstance(success_callback_list, list)
            and all(map(callable, success_callback_list))
        ), "success_callback_list must be a list of callable or None."

        self.name = name
        self.data_type = data_type
        self.ttl = ttl
        self.fail_callback_list = fail_callback_list
        self.success_callback_list = success_callback_list
        self._cache = None

    def build_key(self, **key_params: Dict[str, AnyStr]) -> str:
        if isinstance(self.name, str):
            return self.name.format(**key_params)
        else:
            return self.name(**key_params)

    def get(self, **key_params) -> "Type":
        key = self.build_key(**key_params)
        return self.data_type.get(key)

    def mget(self, key_params_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.data_type.mget(
            *[self.build_key(**key_params) for key_params in key_params_list]
        )

    def add(self, *, key_params: dict, data: Any) -> bool:
        return self.data_type.add(
            key=self.build_key(**key_params), data=data, ttl=self.ttl
        )

    def bulk_add(
        self, *, key_param_data_mapping_list: List[KeyParamDataMapping]
    ) -> bool:
        return self.data_type.bulk_add(
            {
                self.build_key(
                    **key_param_data_mapping["key_params"]
                ): key_param_data_mapping["data"]
                for key_param_data_mapping in key_param_data_mapping_list
            }
        )

    def delete(self, *key_mappings: Dict[str, Any]) -> bool:
        return self.data_type.delete(
            *[self.build_key(**key_mapping) for key_mapping in key_mappings]
        )
