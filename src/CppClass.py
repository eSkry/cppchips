from enum import Enum

from . import CppType
from . import CppVariable
from . import CppFunction


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
