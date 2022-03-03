from ast import literal_eval

from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import singledispatch


class FloatConverter(Converter):
    type = float

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(float)
    def _(self, raw) -> type:
        return raw

    @convert.register(str)
    def _(self, raw) -> type:
        try:
            decoded = literal_eval(raw)
            if not isinstance(decoded, (int, float)):
                raise ValueError
            return float(decoded)
        except ValueError:
            raise NotImplementedError(f"No matched rules to convert this data: {raw}")
