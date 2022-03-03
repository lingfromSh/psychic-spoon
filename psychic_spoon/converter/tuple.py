from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import singledispatch


class TupleConverter(Converter):
    type = tuple

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(tuple)
    def _(self, raw) -> type:
        return raw

    @convert.register(str)
    @convert.register(set)
    @convert.register(list)
    def _(self, raw) -> type:
        return tuple(raw)
