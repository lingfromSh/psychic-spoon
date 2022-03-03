from abc import ABCMeta


class Converter(metaclass=ABCMeta):
    type = NotImplemented

    def convert(self, raw) -> type:
        raise NotImplementedError
