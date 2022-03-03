from typing import Any, AnyStr

from psychic_spoon.types.base import BasicType


class String(BasicType):
    type = str

    def __getitem__(self, item):
        return self.data[item]

    def __add__(self, other: Any) -> str:
        return self.data + other

    def __radd__(self, other: Any) -> str:
        return other + self.data

    def __iadd__(self, other: AnyStr) -> "String":
        return String(self + other)

    def __contains__(self, item: AnyStr) -> bool:
        return item in self.data

    def __eq__(self, other: Any) -> bool:
        return self.data == other


if __name__ == "__main__":
    s = String("Hello")
    assert "Hello" == s
    assert "Hell" in s
    assert s[0] == "H"
    assert s * 2 == "Hello" * 2
    assert s + ",world" == "Hello,world"
    assert "olleH," + s == "olleH,Hello"
    s += "HHH"
    assert s == "HelloHHH"
    print(s)
    print(repr(s))
