from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import dumps, singledispatch


class StringConverter(Converter):
    type = str

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(bytes)
    def _(self, raw) -> type:
        return raw.decode(encoding="utf8")

    @convert.register(str)
    def _(self, raw) -> type:
        return raw

    @convert.register(int)
    @convert.register(float)
    @convert.register(bool)
    def _(self, raw) -> type:
        return str(raw)

    @convert.register(set)
    @convert.register(tuple)
    def _(self, raw) -> type:
        return dumps(raw).decode(encoding="utf8")

    @convert.register(list)
    @convert.register(dict)
    def _(self, raw: list) -> type:
        return dumps(raw).decode(encoding="utf8")
