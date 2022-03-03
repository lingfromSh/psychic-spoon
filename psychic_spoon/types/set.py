from typing import TypeVar

from psychic_spoon.converter import get_converter
from psychic_spoon.types.base import ContainerType, ContainerTypeBuilder, PythonType


class SetMethodMixin:
    @classmethod
    def decode(cls, raw):
        return {
            cls.base_type.decode(item) for item in get_converter(cls.type).convert(raw)
        }

    def encode(self, _type):
        return get_converter(_type).convert(
            {self.base_type.decode(item) for item in self.data}
        )

    def issuperset(self, other):
        return self.data.issuperset(other)

    def issubset(self, other):
        return self.data.issubset(other)

    def intersection(self, other):
        return self.data.intersection(other)

    def add(self, item):
        self._data.add(self.base_type.decode(item))

    def update(self, other):
        self._data.update(other)

    def union(self, item):
        return self._data.union([self.base_type.decode(i) for i in item])

    def difference(self, item):
        return self._data.difference(item)

    def remove(self, item):
        self._data.remove(item)


SetContainer = TypeVar("SetContainer", ContainerType, SetMethodMixin)


class Set(ContainerTypeBuilder):
    type = set
    container_type = SetContainer

    def __init__(self, base_type):
        if not issubclass(base_type, PythonType):
            raise ValueError(f"base_type must be type of {PythonType}")
        self.base_type = base_type

    def build_container(self, data) -> container_type:
        return type(
            "Container",
            (SetMethodMixin, ContainerType),
            {
                "base_type": self.base_type,
                "type": self.type,
            },
        )(data)
