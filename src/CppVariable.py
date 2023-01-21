from . import CppType


class CppVariable:
    def __init__(self, type: CppType.CppType, name: str, value=None, static=False) -> None:
        self._type = type
        self._name = name
        self._static = static
        self._value = value


    @property
    def type(self):
        return self._type


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value


    @property
    def name(self):
        return self._name


    @property
    def static(self):
        return self._static


    def get_declaration(self):
        if not self._value:
            return f'{str(self._type)} {self._name};'

        return f'{str(self._type)} {self._name} = {str(self._value)};'


    def __str__(self) -> str:
        if not self._value:
            return f'{str(self._type)} {self._name}'

        return f'{str(self._type)} {self._name} = {str(self._value)}'

