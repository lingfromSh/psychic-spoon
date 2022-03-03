from psychic_spoon.types.base import BasicType


class Boolean(BasicType):
    type = bool


if __name__ == "__main__":
    t = Boolean(True)
    assert t
    f = Boolean(False)
    assert not f
