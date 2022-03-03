from __future__ import annotations

import inspect
from datetime import timedelta
from functools import partial
from typing import AnyStr, Callable, List, Type, Union

from psychic_spoon.backends.base import Backend
from psychic_spoon.exceptions import KeyPatternError, TTLError
from psychic_spoon.types.base import ContainerTypeBuilder, PythonType

default_ttl = timedelta(minutes=1)


class Key:
    def __init__(
        self,
        pattern: Union[AnyStr, Callable],
        datatype: Union[Type[PythonType], ContainerTypeBuilder],
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

        if not isinstance(datatype, ContainerTypeBuilder) and not issubclass(
            datatype, PythonType
        ):
            raise ValueError(
                "datatype must be type of ContainerTypeBuilder or subclass of PythonType."
            )
        self.datatype = datatype

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

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        try:
            backend_attr = object.__getattribute__(self.backend, name)
            if not inspect.ismethod(backend_attr):
                raise AttributeError("Cannot access backend attribute from key.")

            self.backend.set_target_type(self.datatype)
            spec = inspect.getfullargspec(backend_attr)

            if "ttl" in spec.args:
                return partial(backend_attr, ttl=self.ttl)
            return backend_attr
        except AttributeError:
            raise AttributeError(f"{self} has no method {name}.")


if __name__ == "__main__":

    def main():
        from psychic_spoon.backends.redis_backend import RedisStringBackend
        from psychic_spoon.types.set import Set
        from psychic_spoon.types.string import String

        backend = RedisStringBackend("localhost", port=49153)
        k = Key("user:{id}", datatype=String, backend=backend)
        key = k.build_key(id=1)
        print(key)
        assert key == "user:1"
        k.set(key, "hello-world")
        print(k.get(key))
        assert k.get(key) == "hello-world"
        k.set(key, "hello-today")
        print(k.get(key))
        assert k.get(key)

        k = Key("user:{id}:roles", datatype=Set(String), backend=backend)
        key = k.build_key(id=1)
        print(key)
        assert key == "user:1:roles"
        k.set(key, {1, 2, 3})
        print(k.get(key))
        assert k.get(key) == {"1", "2", "3"}

    main()
