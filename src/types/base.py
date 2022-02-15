class Type:
    PyType = None

    def validate(self, data: PyType):
        raise NotImplementedError("Must be implemented by its subclass.")

    def from_data(self, data: PyType):
        raise NotImplementedError("Must be implemented by its subclass.")

    def __call__(self, data):
        if not self.validate(data):
            raise ValueError("Wrong data.")
        return self.from_data(data)
