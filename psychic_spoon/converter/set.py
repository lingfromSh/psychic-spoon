from orjson import JSONDecodeError

from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import loads, singledispatch


class SetConverter(Converter):
    type = set

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(set)
    def _(self, raw) -> type:
        return raw

    @convert.register(bytes)
    def _(self, raw) -> type:
        return self.convert(raw.decode(encoding="utf8"))

    @convert.register(str)
    @convert.register(list)
    @convert.register(tuple)
    def _(self, raw) -> type:
        return set(raw)

    @convert.register(str)
    def _(self, raw) -> type:
        try:
            decoded = loads(raw)
            if not isinstance(decoded, list):
                raise ValueError
            return set(decoded)
        except (JSONDecodeError, ValueError):
            raise NotImplementedError(f"No matched rules to convert this data: {raw}")
