from orjson import JSONDecodeError

from psychic_spoon.converter.base import Converter
from psychic_spoon.utils import loads, singledispatch


class DictConverter(Converter):
    type = dict

    @singledispatch
    def convert(self, raw) -> type:
        raise NotImplementedError(f"No matched rules to convert this data: {raw}")

    @convert.register(dict)
    def _(self, raw) -> type:
        return raw

    @convert.register(str)
    def _(self, raw) -> type:
        try:
            decoded = loads(raw)
            if not isinstance(decoded, dict):
                raise ValueError
            return decoded
        except (JSONDecodeError, ValueError):
            raise NotImplementedError(f"No matched rules to convert this data: {raw}")
