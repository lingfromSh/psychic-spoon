from typing import TypeVar

from psychic_spoon.types.base import ContainerType, ContainerTypeBuilder, PythonType


class ListMethodMixin:
    def __setitem__(self, key, value):
        self._data[key] = self.base_type.decode(value)

    def append(self, item):
        self._data.append(self.base_type.decode(item))

    def extend(self, item):
        self._data.extend([self.base_type.decode(i) for i in item])

    def insert(self, item):
        self._data.insert(self.base_type.decode(item))

    def remove(self, item):
        self._data.remove(item)

    def pop(self, index=-1):
        return self._data.pop(index)


ListContainer = TypeVar("ListContainer", ContainerType, ListMethodMixin)


class List(ContainerTypeBuilder):
    type = list
    container_type = ListContainer

    def __init__(self, base_type):
        if not issubclass(base_type, PythonType):
            raise ValueError(f"base_type must be type of {PythonType}")
        self.base_type = base_type

    def build_container(self, data) -> container_type:
        return type(
            "Container",
            (ListMethodMixin, ContainerType),
            {
                "base_type": self.base_type,
                "type": self.type,
            },
        )(data)
