from typing import Union

from psychic_spoon.types.base import BasicType


class Float(BasicType):
    type = float

    def __iadd__(self, other: Union["Float", int]) -> "Float":
        if isinstance(other, Float):
            other = other._data
        return Float(self + other)

    def __sub__(self, other: Union["Float", int]) -> int:
        if isinstance(other, Float):
            other = other._data
        return self.data - other

    def __rsub__(self, other: Union["Float", int]) -> int:
        return other - self.data

    def __truediv__(self, other: Union["Float", int]) -> Union[int, float]:
        if isinstance(other, Float):
            other = other._data
        return self.data / other

    def __floordiv__(self, other: Union["Float", int]) -> int:
        if isinstance(other, Float):
            other = other._data
        return self.data // other

    def __mod__(self, other: Union["Float", int]) -> int:
        if isinstance(other, Float):
            other = other._data
        return self.data % other

    def __pow__(self, other: Union["Float", int]) -> int:
        if isinstance(other, Float):
            other = other._data
        return self.data**other
