class CppType:
    def __init__(self, name: str, description=None, const=False, reference=False, pointer=False):
        self._name = name
        self._const = const
        self._reference = reference
        self._pointer = pointer
        self._description = description


    @property
    def is_const(self):
        return self._const

    @is_const.setter
    def is_const(self, value: bool):
        self._const = value


    @property
    def is_pointer(self):
        return self._pointer

    @is_pointer.setter
    def is_pointer(self, value: bool):
        self._pointer = value


    @property
    def is_reference(self):
        return self._reference

    @is_reference.setter
    def is_reference(self, value: bool):
        self._reference = value


    def valid(self) -> bool:
        if self._pointer and self._reference:
            return False

        return True


    def convertable_to(self, type) -> bool:
        if type.is_pointer() and not self._pointer and not self._reference:
            return False

        if type.is_reference() and not self._reference:
            return False

        return True


    def __repr__(self) -> str:
        return f'{self.__str__()} -> {self._description}'


    def __str__(self) -> str:
        return f'{"const " if self._const else ""}{self._name}{"&" if self._reference else ""}{"*" if self._pointer else ""}'
