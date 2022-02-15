from .base import Type


class String(Type):
    PyType = str

    def validate(self, data: PyType) -> bool:
        return isinstance(data, str)

    @classmethod
    def from_data(cls, data: PyType) -> type:
        return type(cls.__name__, (cls,), {
            "_data": data
        })
