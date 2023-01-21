from . import CppType


class CppVoid(CppType.CppType):
    def __init__(self, description=None, const=False, pointer=False):
        super().__init__(name='void', description=description, const=const, reference=False, pointer=pointer)

    def __str__(self) -> str:
        return super().__str__()

    def valid(self) -> bool:
        if self._reference or (self._const and not self._pointer):
            return False

        return True


class TypeWithUnsigned(CppType.CppType):
    def __init__(self, name: str, description=None, const=False, reference=False, pointer=False, unsigned=False):
        super().__init__(name, description, const, reference, pointer)
        self.unsigned = unsigned

    @property
    def is_unsigned(self):
        return self.unsigned

    @is_unsigned.setter
    def is_unsigned(self, value: bool):
        self.unsigned = value

    def __str__(self) -> str:
        if self.unsigned:
            return super().__str__().replace(self._name, f'unsigned {self._name}')
        return super().__str__()


class CppChar(TypeWithUnsigned):
    def __init__(self, const=False, reference=False, pointer=False, unsigned=False):
        super().__init__(name='char', description='char type', const=const, reference=reference, pointer=pointer, unsigned=unsigned)

    def __str__(self) -> str:
        return super().__str__()


class CppInt(TypeWithUnsigned):
    def __init__(self, const=False, reference=False, pointer=False, unsigned=False) -> None:
        super().__init__(name='int', description='int type', const=const, reference=reference, pointer=pointer, unsigned=unsigned)

    def __str__(self) -> str:
        return super().__str__()


class CppFloat(TypeWithUnsigned):
    def __init__(self, const=False, reference=False, pointer=False, unsigned=False):
        super().__init__(name='float', description='float type', const=const, reference=reference, pointer=pointer, unsigned=unsigned)

    def __str__(self) -> str:
        return super().__str__()


class CppDouble(TypeWithUnsigned):
    def __init__(self, const=False, reference=False, pointer=False, unsigned=False):
        super().__init__(name='double', description='double type', const=const, reference=reference, pointer=pointer, unsigned=unsigned)

    def __str__(self) -> str:
        return super().__str__()