from ast import literal_eval

from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import singledispatch


class IntegerConverter(Converter):
    type = int

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(int)
    def _(self, raw) -> type:
        return raw

    @convert.register(bytes)
    def _(self, raw) -> type:
        return int(raw.decode(encoding="utf8"))

    @convert.register(str)
    @convert.register(float)
    @convert.register(bool)
    def _(self, raw) -> type:
        try:
            decoded = literal_eval(raw)
            if not isinstance(decoded, (int, float)):
                raise ValueError
            return int(decoded)
        except ValueError:
            raise NotImplementedError(f"No matched rules to convert this data: {raw}")
