from __future__ import annotations

from datetime import timedelta
from typing import Any, AnyStr, Callable, Dict, List, Union

from .backends.base import Backend
from .exceptions import KeyPatternError, TTLError, ValidationError
from .types.base import Type

default_ttl = timedelta(minutes=1)


class Key:
    def __init__(
        self,
        pattern: Union[AnyStr, Callable],
        data_type: Type,
        backend: Backend = None,
        ttl: timedelta = default_ttl,
        on_add_fail_callback_list: List[Callable] = None,
        on_add_success_callback_list: List[Callable] = None,
        on_delete_fail_callback_list: List[Callable] = None,
        on_delete_success_callback_list: List[Callable] = None,
    ):
        """

        :param pattern:
        :param data_type:
        :param backend:
        :param ttl:
        :param on_add_fail_callback_list:
        :param on_add_success_callback_list:
        :param on_delete_fail_callback_list:
        :param on_delete_success_callback_list:
        """
        if not isinstance(pattern, str) and not callable(pattern):
            raise KeyPatternError("pattern must be str or callable.")
        self.pattern = pattern

        if not isinstance(data_type, Type):
            raise ValueError("data_type must be type of Type.")
        self.data_type = data_type

        if not isinstance(backend, Backend):
            raise ValueError("backend must be type of Backend.")
        self.backend = backend

        if not isinstance(ttl, timedelta):
            raise TTLError("ttl must be type of timedelta.")
        self.ttl = ttl

        if on_add_fail_callback_list is not None and (
            not isinstance(on_add_fail_callback_list, list)
            or not all(map(callable, on_add_fail_callback_list))
        ):
            raise ValueError("on_add_fail_callback_list must be list of callable.")
        self.on_add_fail_callback_list = on_add_fail_callback_list

        if on_add_success_callback_list is not None and (
            not isinstance(on_add_success_callback_list, list)
            or not all(map(callable, on_add_success_callback_list))
        ):
            raise ValueError("on_add_success_callback_list must be list of callable.")
        self.on_add_success_callback_list = on_add_success_callback_list

        if on_delete_fail_callback_list is not None and (
            not isinstance(on_delete_fail_callback_list, list)
            or not all(map(callable, on_delete_fail_callback_list))
        ):
            raise ValueError("on_delete_fail_callback_list must be list of callable.")
        self.on_delete_fail_callback_list = on_delete_fail_callback_list

        if on_delete_success_callback_list is not None and (
            not isinstance(on_delete_success_callback_list, list)
            or not all(map(callable, on_delete_success_callback_list))
        ):
            raise ValueError(
                "on_delete_success_callback_list must be list of callable."
            )
        self.on_delete_success_callback_list = on_delete_success_callback_list

    def build_key(self, **key_params):
        if isinstance(self.pattern, str):
            return self.pattern.format(**key_params)
        elif callable(self.pattern):
            return self.pattern(**key_params)
        else:
            raise KeyPatternError(
                f"<Key pattern: {id(self.pattern)}> must be str or callable."
            )

    def get(self, **key_params) -> Type:
        key = self.build_key(**key_params)
        return self.backend.get(key, convert_type=self.data_type)

    def mget(self, key_params_list: List[Dict]) -> List[Type]:
        keys = [self.build_key(**key_params) for key_params in key_params_list]
        return self.backend.mget(keys, convert_type=self.data_type)

    def add(self, key: AnyStr, data: Any, ttl: timedelta = None) -> bool:
        if not isinstance(ttl, timedelta):
            raise TTLError("ttl must be type of timedelta.")
        if not self.data_type.validate(data):
            raise ValidationError(f"Expected {self.data_type}, but got {data}.")
        return self.backend.add(key, data, data_type=self.data_type, ttl=ttl)

    def delete(self, keys: List[AnyStr]) -> bool:
        return self.backend.delete(keys)
