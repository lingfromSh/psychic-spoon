from ast import literal_eval

from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import singledispatch


class BooleanConverter(Converter):
    type = bool

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(str)
    def _(self, raw) -> type:
        try:
            decoded = literal_eval(raw)
            if not isinstance(decoded, bool):
                raise ValueError
            return decoded
        except ValueError:
            raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(int)
    @convert.register(float)
    @convert.register(bool)
    def _(self, raw) -> type:
        return bool(raw)
