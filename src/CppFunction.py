from . import CppType


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
