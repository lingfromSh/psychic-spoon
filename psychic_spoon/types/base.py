from inspect import getmembers, ismethod

from psychic_spoon.converter import get_converter


class PythonType:
    type = NotImplemented

    def __init__(self, data):
        self._data = self.decode(data)

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.data}>"

    def __eq__(self, other) -> bool:
        return self.data == other

    @property
    def data(self):
        return self._data

    @classmethod
    def decode(cls, raw) -> type:
        return get_converter(cls.type).convert(raw)

    def encode(self, _type):
        return get_converter(_type).convert(self.data)


class BasicType(PythonType):
    def __bool__(self) -> bool:
        return bool(self.data)

    def __add__(self, other):
        return self.data + other

    def __radd__(self, other):
        return other + self.data

    def __mul__(self, other: int):
        return self.data * other

    def __rmul__(self, other: int):
        return other * self.data


class ContainerType(PythonType):
    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class ContainerTypeBuilder:
    container_type = NotImplemented

    def __call__(self, data) -> container_type:
        return self.build_container(data)

    @property
    def container_methods(self):
        print(getmembers(self, predicate=ismethod))
        return getmembers(self, predicate=ismethod)

    def build_container(self, data) -> container_type:
        raise NotImplementedError("Must be implemented by its subclass.")
