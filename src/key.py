from __future__ import annotations

from datetime import timedelta
from functools import partial
from typing import AnyStr, Callable, List, Union

from .backends.base import Backend
from .exceptions import KeyPatternError, TTLError
from .types import DataType

default_ttl = timedelta(minutes=1)


class Key:
    def __init__(
        self,
        pattern: Union[AnyStr, Callable],
        data_type: DataType,
        backend: Backend = None,
        ttl: timedelta = default_ttl,
        on_add_fail_callback_list: List[Callable] = None,
        on_add_success_callback_list: List[Callable] = None,
        on_delete_fail_callback_list: List[Callable] = None,
        on_delete_success_callback_list: List[Callable] = None,
    ):
        """

        :param pattern:
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

        if not isinstance(data_type, DataType):
            raise ValueError("data_type must be type of DataType.")
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

        self.data_type.activate(self.backend)

    def build_key(self, **key_params):
        if isinstance(self.pattern, str):
            return self.pattern.format(**key_params)
        elif callable(self.pattern):
            return self.pattern(**key_params)
        else:
            raise KeyPatternError(
                f"<Key pattern: {id(self.pattern)}> must be str or callable."
            )

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return partial(getattr(self.data_type, item), self.backend)
