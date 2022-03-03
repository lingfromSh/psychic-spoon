from typing import Type

from psychic_spoon.types.base import PythonType


class Backend:
    def __init__(self):
        self.target_type = None

    def set_target_type(self, _type: Type[PythonType]):
        self.target_type = _type
