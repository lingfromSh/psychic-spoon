class DataType:
    ...


class BaseDataType(DataType):
    def serialize(self, data):
        raise NotImplementedError("Must be implemented by its subclass.")

    def deserialize(self, raw: str):
        raise NotImplementedError("Must be implemented by its subclass.")


class ContainerDataType(DataType):
    def serialize(self, data):
        raise NotImplementedError("Must be implemented by its subclass.")

    def deserialize(self, raw: str):
        raise NotImplementedError("Must be implemented by its subclass.")
