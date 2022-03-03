from typing import Any

from psychic_spoon.converter.boolean import BooleanConverter
from psychic_spoon.converter.dict import DictConverter
from psychic_spoon.converter.float import FloatConverter
from psychic_spoon.converter.integer import IntegerConverter
from psychic_spoon.converter.list import ListConverter
from psychic_spoon.converter.set import SetConverter
from psychic_spoon.converter.string import StringConverter
from psychic_spoon.converter.tuple import TupleConverter

__all__ = [
    BooleanConverter,
    DictConverter,
    FloatConverter,
    IntegerConverter,
    ListConverter,
    SetConverter,
    StringConverter,
    TupleConverter,
]


def get_converter(type_: Any):
    try:
        return next(converter for converter in __all__ if converter.type == type_)()
    except StopIteration:
        raise ValueError(f"No matched converter for this type: {type_}")
