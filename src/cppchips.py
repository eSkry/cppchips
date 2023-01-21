

class CppType:
    ''''''
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
        if value:
            self._reference = False


    @property
    def is_reference(self):
        return self._reference

    @is_reference.setter
    def is_reference(self, value: bool):
        self._reference = value
        if value:
            self._pointer = False


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


class CppVariable:
    def __init__(self, type: CppType, name: str, value=None, static=False) -> None:
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


class CppFunction:
    def __init__(self, name: str, ret_t: CppType.CppType, args=[], body=None, static=False, constexpr=False):
        self.name = name
        self.ret_t = ret_t
        self.args = args
        self.static = static
        self.constexpr = constexpr
        self.body = body


    def get_declaration_string(self) -> str:
        function_decl = self.__str__().replace(";", "")
        function_decl += f' {{ {self.body if self.body else ""} }} '

        return function_decl


    def get_definition_string(self) -> str:
        return self.__str__()


    def __str__(self) -> str:
        function_def = f"{str(self.ret_t)} {self.name}("

        args = [str(x) for x in self.args]
        function_def += ", ".join(args)
        function_def += ");"

        return function_def


from enum import Enum


class CppClassSection(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class CppClass:
    def __init__(self, name: str, base_classes={}, methods={}, variables={}) -> None:
        self._name = name
        self._base_classes=base_classes
        self._methods = methods
        self._variables = variables

        self._type = CppType.CppType(name=name)


    @property
    def type(self):
        return self._type


    def is_base_class(self, class_t) -> bool:
        return class_t.name in self._base_classes


    def add_variable(self, var: CppVariable.CppVariable, section: CppClassSection, with_setter=False, with_getter=False, default_value=None):
        self._variables[var.name] = {"variable": var, "section": section
                                    , "with_setter": with_setter, "with_getter": with_getter, "value": default_value}


    def add_method(self, method: CppFunction.CppFunction, section: CppClassSection):
        self._methods[method.name] = {"method": method, "section": section}


    def add_base_class(self, class_name: str, inheritance="public"):
        self._base_classes[class_name] = {"class_name": class_name, "inheritance": inheritance}


    def add_base_class(self, class_t, inheritance="public"):
        self._base_classes[class_t._name] = {"class_name": class_t._name, "class": class_t, "inheritance": inheritance}


    def remove_method(self, name: str):
        self._methods.pop(name, None)


    def remove_variable(self, name: str):
        self._variables.pop(name, None)


    def remove_base_class(self, name: str):
        self._base_classes.pop(name, None)


    def __str__(self) -> str:
        class_str = f'class {self._name}'
        if self._base_classes:
            class_str += " : "
            b_class_list = [f'{str(self._base_classes[x]["inheritance"])} {self._base_classes[x]["class_name"]}' for x in self._base_classes]
            class_str += ", ".join(b_class_list)

        class_str += ' { \n'


        # start public section

        # start protected section

        # start private section

        class_str += "\n};"

        return class_str


