from typing import TypeVar

from psychic_spoon.types.base import ContainerType, ContainerTypeBuilder, PythonType


class DictMethodMixin:
    def __init__(self, data):
        data = self.decode(data)

        self._data = {}
        for k, v in data.items():
            if k not in self.fields:
                raise ValueError(f"Got unexpected key: {k}")
            self._data[k] = self.fields[k].decode(v)

    def __getitem__(self, item):
        return self.fields[item].decode(self.data[item])

    def __setitem__(self, key, value):
        self._data[key] = self.fields[key].decode(value)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.fields:
                continue
            self._data[k] = self.fields[k].decode(v)


DictContainer = TypeVar("DictContainer", ContainerType, DictMethodMixin)


class Dict(ContainerTypeBuilder):
    type = dict
    container_type = DictContainer

    def __init__(self, **fields):
        for field in fields.values():
            if not issubclass(field, PythonType):
                raise ValueError(f"Only accept subclass of {PythonType}")
        self.fields = fields

    def __call__(self, data):
        return self.build_container(data)

    def build_container(self, data) -> container_type:
        return type(
            "DictContainer",
            (DictMethodMixin, ContainerType),
            {"fields": self.fields, "type": self.type},
        )(data)


if __name__ == "__main__":
    from psychic_spoon.types.integer import Integer
    from psychic_spoon.types.string import String

    builder = Dict(name=String, age=Integer)
    d = builder(name="ling", age=11)
    assert d == {"name": "ling", "age": 11}
    d.update(name="wang")
    assert d == {"name": "wang", "age": 11}
    assert d["name"] == "wang"
