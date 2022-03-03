from typing import Union

from psychic_spoon.converter import get_converter
from psychic_spoon.types.base import BasicType


class Integer(BasicType):
    type = int
    _converter = get_converter(type)

    def __iadd__(self, other: Union["Integer", int]) -> "Integer":
        if isinstance(other, Integer):
            other = other._data
        return Integer(self + other)

    def __sub__(self, other: Union["Integer", int]) -> int:
        if isinstance(other, Integer):
            other = other._data
        return self.data - other

    def __rsub__(self, other: Union["Integer", int]) -> int:
        return other - self.data

    def __truediv__(self, other: Union["Integer", int]) -> Union[int, float]:
        if isinstance(other, Integer):
            other = other._data
        return self.data / other

    def __floordiv__(self, other: Union["Integer", int]) -> int:
        if isinstance(other, Integer):
            other = other._data
        return self.data // other

    def __mod__(self, other: Union["Integer", int]) -> int:
        if isinstance(other, Integer):
            other = other._data
        return self.data % other

    def __pow__(self, other: Union["Integer", int]) -> int:
        if isinstance(other, Integer):
            other = other._data
        return self.data**other
