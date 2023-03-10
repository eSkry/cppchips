from typing import List


CLASS_MEMBER_PREFIX='m'
FUNCTION_ARGUMENT_PREFIX='a'
GETTER_PREFIX="get"
SETTER_PREFIX="set"
DEFAULT_STRING_TYPE="std::string"


def _getClassPrefixedVariableName(variable_name: str) -> str:
    return f'{CLASS_MEMBER_PREFIX}{variable_name}'


def _getPrefixedVariableArgument(variable_name: str) -> str:
    return f'{FUNCTION_ARGUMENT_PREFIX}{variable_name}'


def _getSetterPrefixForVariable(variable_name: str) -> str:
    return f'{SETTER_PREFIX}{variable_name}'


def _getGetterPrfixForVariable(variable_name: str) -> str:
    return f'{GETTER_PREFIX}{variable_name}'


class CppNamespace:
    def __init__(self, name: str) -> None:
        self._name = name
        self._namespaces = {}


    def namespace_path(self):
        return self.name


    def get_namespace(self, namespace_name: str):
        return self._namespaces[namespace_name]


    def add_namespace(self, namespace_name: str):
        self._namespaces[namespace_name, CppNamespace(namespace_name)]
        return self


class GlobalNamespace(CppNamespace):
    def __init__(self) -> None:
        super().__init__('')

gnamespace = GlobalNamespace()


class CppFuncDescription:
    def __init__(self, description) -> None:
        self._description = description


    @property
    def description(self):
        return self._description


class CppType():
    def __init__(self, name: str, description=None, reference=False, pointer=False, rvalue_ref=False, const=False):
        self._name = name
        self._reference = reference
        self._pointer = pointer
        self._description = description
        self._rvalue_ref = rvalue_ref
        self._const = const


    def _clear_references(self):
        self._pointer = False
        self._reference = False
        self._rvalue_ref = False


    @property
    def rvalue(self):
        return self._rvalue_ref


    @rvalue.setter
    def rvalue(self, value: bool):
        if value:
            self._clear_references()
        self._rvalue_ref = value


    @property
    def const(self):
        return self._const


    @const.setter
    def const(self, value: bool):
        self._const = value


    @property
    def pointer(self):
        return self._pointer


    @pointer.setter
    def pointer(self, value: bool):
        if value:
            self._clear_references()
        self._pointer = value


    @property
    def reference(self):
        return self._reference


    @reference.setter
    def reference(self, value: bool):
        if value:
            self._clear_references()
        self._reference = value


    @property
    def type_clear(self) -> str:
        return f'{self._name}'


    @property
    def type_reference(self) -> str:
        return f'{self._name}&'


    @property
    def type_pointer(self) -> str:
        return f'{self._name}*'


    @property
    def type_rvalue_reference(self) -> str:
        return f'{self._name}&&'


    @property
    def type_const_reference(self) -> str:
        return f'const {self.type_reference}'


    @property
    def type_const_pointer(self) -> str:
        return f'const {self.type_pointer}'


    @property
    def type_const(self) -> str:
        return f'const {self.type_clear}'


    @property
    def type(self) -> str:
        if self._const:
            if self._reference:
                return self.type_const_reference
            elif self._pointer:
                return self.type_const_pointer
            return self.type_const

        if self._rvalue_ref:
            return self.type_rvalue_reference
        elif self._reference:
            return self.type_reference
        elif self._pointer:
            return self.type_pointer

        return self.type_clear


    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CppType):
            return self.type == __o.type

        return False


class CppVoid(CppType):
    def __init__(self, pointer=False):
        super().__init__(name='void', description='void type', reference=False, pointer=pointer)


    def valid(self) -> bool:
        if self._reference or not self._pointer:
            return False

        return True


class TypeWithUnsigned(CppType):
    def __init__(self, name: str, description=None, reference=False, pointer=False, unsigned=False, const=False):
        super().__init__(name, description, reference, pointer, const=const)
        self._unsigned = unsigned


    @property
    def unsigned(self):
        return self._unsigned


    @unsigned.setter
    def unsigned(self, value: bool):
        self._unsigned = value


    @property
    def type_unsigned(self):
        return f'unsigned {super().type}'


    @property
    def type_signed(self):
        return f'{super().type}'


    @property
    def type(self) -> str:
        if self._unsigned:
            return self.type_unsigned
        return self.type_signed


class CppChar(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False, const=False):
        super().__init__(name='char', description='char type', reference=reference, pointer=pointer, unsigned=unsigned, const=const)


class CppInt(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False, const=False) -> None:
        super().__init__(name='int', description='int type', reference=reference, pointer=pointer, unsigned=unsigned, const=const)


class CppFloat(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False, const=False):
        super().__init__(name='float', description='float type', reference=reference, pointer=pointer, unsigned=unsigned, const=const)


class CppDouble(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False, const=False):
        super().__init__(name='double', description='double type', reference=reference, pointer=pointer, unsigned=unsigned, const=const)


class CppString(CppType):
    def __init__(self, reference=False, pointer=False, const=False):
        super().__init__(DEFAULT_STRING_TYPE, 'C++ string type', reference, pointer, const=const)


class CppAuto(CppType):
    def __init__(self, reference=False, pointer=False, rvalue_ref=False, const=False):
        super().__init__('auto', 'c++ auto type', reference, pointer, rvalue_ref, const=const)


class CppBool(CppType):
    def __init__(self, reference=False, pointer=False, rvalue_ref=False, const=False):
        super().__init__('bool', 'c++ boolean type', reference, pointer, rvalue_ref, const)


class CppNONE(CppType):
    '''CppNONE - ?????? ????????????????. ?????????????????? ?????? ?????????????????????????? ?? ?????????????????????????? ????????????'''


    def __init__(self):
        super().__init__('')


class CppVariable():
    '''?????????? CppVariable ???????????????? ???????????????????????????? ???????????????? ???????????????????? ?? C++'''


    def __init__(self, type: CppType, name: str, value=None, static=False) -> None:
        self._type = type
        self._name = name
        self._static = static
        self._value = value


    @property
    def var_type(self):
        return self._type


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value: bool):
        self._value = value


    @property
    def name(self):
        return self._name


    @property
    def static(self):
        return self._static


    @static.setter
    def static(self, val: bool):
        self._static = val


    @property
    def var_static(self) -> str:
        return f'static {self._type.type} {self._name}'


    @property
    def var(self) -> str:
        if self._static:
            return f'{self.var_static}'

        return f'{self.var_type.type} {self._name}'


    def definition(self) -> str:
        if not self._value:
            return f'{self._type.type} {self._name};'

        return f'{self._type.type} {self._name} = {str(self._value)};'


    def definition_in_class(self) -> str:
        if not self._value:
            return f'{self._type.type} {_getClassPrefixedVariableName(self._name)};'

        return f'{self._type.type} {_getClassPrefixedVariableName(self._name)} = {str(self._value)};'


    def declaration(self):
        return f'{self._type.type} {self._name};'


class CppStringVar(CppVariable):
    def __init__(self, name: str, value=None, static=False, reference=False, pointer=False, const=False) -> None:
        super().__init__(CppString(reference=reference, pointer=pointer, const=const), name, value, static)

    @property
    def value(self):
        return f'"{super().value}"'


# ???????????????????????????? ???????????? ????????????????????
CppVariableList = List[CppVariable]


class CppFunction:
    '''CppFunction - ???????? ?????????????? ???????????????????????? ?????????? ?????????????? ?? ???????????? ???? C++'''


    def __init__(self, name: str, ret_t: CppType, args: CppVariableList = [], body=None, static=False, constexpr=False, noexcept=False, const=False, override=False, virtual=False, delete=True):
        self._name = name
        self._ret_t = ret_t
        self._args = args
        self._static = static
        self._constexpr = constexpr
        self._body = body
        self._noexcept = noexcept
        self._const = const
        self._virtual = virtual
        self._override = override
        self._delete = delete


    @property
    def args_signature(self) -> str:
        if self._args:
            return ";;".join([arg.var_type.type for arg in self.args])


    @property
    def delete(self) -> bool:
        return self._delete


    @property
    def virtual(self) -> bool:
        return self._virtual


    @property
    def override(self) -> bool:
        return self._override


    @property
    def static(self) -> bool:
        return self._static


    @property
    def constexpr(self) -> bool:
        return self._constexpr


    @property
    def noexcept(self) -> bool:
        return self._noexcept


    @property
    def const(self) -> bool:
        return self._const


    @property
    def name(self) -> str:
        return self._name


    @property
    def return_type(self) -> CppType:
        return self._ret_t


    @property
    def body(self) -> str:
        return self._body


    @body.setter
    def body(self, val: str):
        self._body = val


    def get_arg_object_list(self) -> CppVariableList:
        return self._args


    def _get_arg_list(self) -> str:
        args = [x.var for x in self._args]
        return ", ".join(args)


    def definition(self) -> str:
        '''get_definition - ???????????????????? ?????????????? ???????????? ?? ???? ??????????'''

        if not self._delete:
            return self.declaration()

        fdc_str = f"<static><virtual><constexpr> {self._ret_t.type} {self._name}({self._get_arg_list()})<const><noexcept><override> {{\n<body>\n}}"

        tmp_body = None
        if not self._body and self._ret_t._name != CppVoid()._name:
            tmp_body = "return {};"

        fdc_str = fdc_str.replace("<static>", "static " if self._static else "")
        fdc_str = fdc_str.replace("<constexpr>", " constexpr " if self._constexpr else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self._noexcept else "")
        fdc_str = fdc_str.replace("<const>", " const" if self._const else "")
        fdc_str = fdc_str.replace("<virtual>", "virtual " if self._virtual else "")
        fdc_str = fdc_str.replace("<override>", " override" if self._override else "")

        if self._body:
            fdc_str = fdc_str.replace("<body>", self._body)
        else:
            fdc_str = fdc_str.replace("<body>", tmp_body if tmp_body else "")

        return fdc_str


    def declaration(self) -> str:
        fdf_str = f"<static><virtual><constexpr> {self._ret_t.type} {self._name}({self._get_arg_list()})<const><noexcept><override><deleted>;"

        fdf_str = fdf_str.replace("<static>", "static " if self._static else "")
        fdf_str = fdf_str.replace("<constexpr>", " constexpr " if self._constexpr else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self._noexcept else "")
        fdf_str = fdf_str.replace("<const>", " const" if self._const else "")
        fdf_str = fdf_str.replace("<virtual>", " virtual" if self._virtual else "")
        fdf_str = fdf_str.replace("<override>", " override" if self._override else "")
        fdf_str = fdf_str.replace("<deleted>", " = 0" if not self._delete else "")

        return fdf_str


    def __str__(self) -> str:
        return self.definition()


CppFunctionList = List[CppFunction]


class CppConstructor(CppFunction):
    def __init__(self, args: CppVariableList = [], body=None, constexpr=False, deleted=False, default=False):
        super().__init__('', CppNONE(), args, body, constexpr)
        self._deleted = deleted
        self._default = default
        self._args = args


    @property
    def deleted(self) -> bool:
        return self._deleted


    @property
    def default(self) -> bool:
        return self._default


    def arg_count(self):
        return len(self._args)


    def definition(self) -> str:
        if self._deleted or self._default:
            return self.declaration()

        fdc_str = f"<constexpr> <class_name>({self._get_arg_list()})<noexcept> <initializer_list>{{\n<body>\n}}"

        fdc_str = fdc_str.replace("<constexpr>", "constexpr" if self._constexpr else "")
        fdc_str = fdc_str.replace("<body>", self._body if self._body else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self._noexcept else "")

        initializer_list = [x for x in self._args if x.init_on_constructor]

        if initializer_list:
            init_list_str = " : "
            # todo: ?????????????????????? ?????????????????????????? ???????????????????????? ???????????????? ????????????

            var_init_list = []
            for init_var in self._args:
                var_init_list.append(f'{init_var.name}{{{init_var.name}}}')

            init_list_str += ", ".join(var_init_list)
            fdc_str = fdc_str.replace("<initializer_list>", init_list_str)
        else:
            fdc_str = fdc_str.replace("<initializer_list>", "")

        return fdc_str


    def declaration(self) -> str:
        fdf_str = f"<constexpr> <class_name>({self._get_arg_list()})<noexcept><deleted><default>;"

        fdf_str = fdf_str.replace("<constexpr>", "constexpr" if self._constexpr else "")
        fdf_str = fdf_str.replace("<deleted>", " = deleted" if self.deleted else "")
        fdf_str = fdf_str.replace("<default>", " = default" if self.default else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self._noexcept else "")

        return fdf_str


    def __str__(self) -> str:
        return self.definition


CppConstructorList = List[CppConstructor]


class CppClassScope:
    def __init__(self, contained_class) -> None:
        self._contained_class = contained_class
        self._methods: CppFunctionList = []
        self._variables: CppVariableList  = []
        self._constructors: CppConstructorList = []
        self._custom_body: str = None


    def set_custom_body(self, body):
        self._custom_body = body


    def _contains_variable(self, var):
        if isinstance(var, str):
            for varobj in self._variables:
                if varobj.name == var:
                    return True

        return var in self._variables


    def _get_variable(self, var_name: str):
        for varobj in self._variables:
            if varobj.name == var_name:
                return varobj

        return None


    def _add_variable(self, var: CppVariable):
        self._variables.append(var)
        return self


    def add_variable(self, type: CppType, name: str, value=None, static=False):
        var = CppVariable(type, name, value, static)
        self._variables.append(var)
        return self


    def add_getter(self, variable):
        '''Add getter method for target variable'''

        if isinstance(variable, str):
            getter = CppFunction(_getGetterPrfixForVariable(variable), CppAuto(reference=True), body=f'return {_getClassPrefixedVariableName(variable)};', noexcept=True)
            const_gettter = CppFunction(_getGetterPrfixForVariable(variable), CppAuto(reference=True, const=True), body=f'return {_getClassPrefixedVariableName(variable)};', noexcept=True, const=True)

            self._methods.append(getter)
            self._methods.append(const_gettter)
        elif isinstance(variable, CppVariable):
            ret_t_const_ref = CppType(variable.var_type.type_clear, reference=True, const=True)
            ret_t_ref = CppType(variable.var_type.type_clear, reference=True)

            getter = CppFunction(_getGetterPrfixForVariable(variable), ret_t_ref, body=f'return {_getClassPrefixedVariableName(variable)};', noexcept=True)
            const_getter = CppFunction(_getGetterPrfixForVariable(variable), ret_t_const_ref, body=f'return {_getClassPrefixedVariableName(variable)};', noexcept=True, const=True)
            self._methods.append(getter)
            self._methods.append(const_getter)
        else:
            raise Exception(f'Error add {variable} in CppClass.add_getter, function allow only string and CppVariable types.')

        return self


    def add_setter(self, variable):
        '''Add setter method for target variable'''

        var_obj: CppVariable = None
        if isinstance(variable, str):
            var_obj: CppVariable = self._contained_class.find_variable_by_name(variable)
            if var_obj == None:
                raise Exception(f'Variable {variable} not exists for create setter.')

        setter = CppFunction(_getSetterPrefixForVariable(var_obj.name), CppVoid()
                , [CppVariable(CppType(var_obj.var_type._name, const=True, reference=True), _getPrefixedVariableArgument(var_obj.name))]
                , f'{_getClassPrefixedVariableName(var_obj.name)} = {_getPrefixedVariableArgument(var_obj.name)};')

        self._methods.append(setter)
        return self


    def add_method(self, name: str, ret_t: CppType, args: CppVariableList = [], body=None, static=False, constexpr=False, noexcept=False, const=False, override=False, virtual=False, impl=True):
        method = CppFunction(name, ret_t, args, body, static, constexpr, noexcept, const, override, virtual, impl)
        self._methods.append(method)
        return self


    def add_virtual_method(self, name: str, ret_t: CppType, args: CppVariableList = [], body=None, static=False, constexpr=False, noexcept=False, const=False):
        '''Its wrapped function add_method'''

        method = CppFunction(name, ret_t, args, body, static, constexpr, noexcept, const, False, True, True)
        self._methods.append(method)
        return self


    def add_override_method(self, name: str, body: str = None):
        methods: CppFunctionList = self._contained_class.find_methods_in_base_classes({"virtual": True, "name": name})
        if not methods:
            return self

        method = methods[0]
        if not method:
            return self

        overrided = CppFunction(method.name, method.return_type, method._args, body, static=method.static
                                , constexpr=method.constexpr, noexcept=method.noexcept, const=method.const
                                , override=True, virtual=False, delete=True)

        self._methods.append(overrided)
        return self


    def add_overload_base_method(self, name: str, args: CppVariableList = [], body: str = None):
        methods: CppFunctionList = self._contained_class.find_methods_in_base_classes({"name": name})
        if not methods:
            return self

        method = methods[0]
        if not method:
            return self

        overloaded = CppFunction(method.name, method.return_type, args, body, method.static, method.constexpr, method.noexcept
                                 , method.const, method.override, method.virtual, method.delete)

        self._methods.append(overloaded)
        return self


    def add_deleted_virtual_method(self, name: str, ret_t: CppType, args: CppVariableList = [], body=None, static=False, constexpr=False, noexcept=False, const=False):
        '''Its wrapped function add_method'''

        method = CppFunction(name, ret_t, args, body, static, constexpr, noexcept, const, False, True, False)
        self._methods.append(method)
        return self


    def set_body(self, body_text: str):
        self._custom_body = body_text
        return self


    def _add_method(self, method: CppFunction):
        self._methods.append(method)
        return self


    def add_constructor(self, args: CppVariableList = [], body=None, constexpr=False, deleted=False, default=False):
        constr = CppConstructor(args, body, constexpr, deleted, default)
        self._constructors.append(constr)
        return self


    def _add_constructor(self, constructor: CppConstructor):
        self._constructors.append(constructor)
        return self


    def empty(self):
        if not self._methods and not self._variables and not self._constructors:
            return True
        return False


def _basic_mach_object_by_attributes(object, attributes: dict) -> bool:
    return all([getattr(object, attr_name) == attributes[attr_name] for attr_name in attributes])


class CppClass:
    def __init__(self, name: str, class_type="class") -> None:
        self._class_name = name
        self._class_type = class_type
        self._public_scope = CppClassScope(self)
        self._protected_scope = CppClassScope(self)
        self._private_scope = CppClassScope(self)
        self._base_classes = {}


    def find_methods_in_base_classes(self, search_tags: dict):
        result = []
        for base_class_name in self._base_classes:
            result += self._find_methods_in_class(self._base_classes[base_class_name]["class"], search_tags)
        return result


    def find_methods_in_base_class(self, class_name: str, search_tags: dict):
        if not class_name in self._base_classes:
            return []

        return self._find_methods_in_class(self._base_classes[class_name]["class"], search_tags)


    def find_methods(self, search_tags: dict):
        return self._find_methods_in_class(self, search_tags)


    def _find_methods_in_class(self, class_obj, search_tags: dict):
        '''
        ?????????????? ?????????????????? ?????????? ?????????????? ????????????, ???????????????????? ?????? ???????????????? ????????????.
        ?????????????? search_tags ?????????? ?????????????????? ??????: {"tag_name": "value"}}.

        ???????????? ?????????????? 1: {"name": "foo", "virtual": True}.
        ???????????? ?????????????? 2: {"name": "foo", "virtual": True, "const": True}}
        '''

        result = []

        scope_list = [class_obj._public_scope, class_obj._private_scope, class_obj._protected_scope]
        for scope in scope_list:
            method_list = scope._methods
            for method in method_list:
                if _basic_mach_object_by_attributes(method, search_tags):
                    result.append(method)
        return result


    def find_constructor_in_base_classes(self, search_tags: dict):
        result = []

        for base_class_name in self._base_classes:
            result += self.find_constructor_in_base_class(base_class_name, search_tags)

        return result


    def find_constructor_in_base_class(self, class_name: str, search_tags: dict):
        if not class_name in self._base_classes:
            return []

        return self._find_constructor_in_class(self._base_classes[class_name]["class"], search_tags)


    def _find_constructor_in_class(self, class_obj, search_tags: dict):
        result = []

        scope_list = [class_obj._public_scope, class_obj._private_scope, class_obj._protected_scope]
        for scope in scope_list:
            constructor_list = scope._constructors
            for constructor in constructor_list:
                if _basic_mach_object_by_attributes(constructor, search_tags):
                    result.append(constructor)

        return result


    def get_class_type(self):
        return CppType(self._class_name, ['User class type'])


    @property
    def name(self):
        return self._class_name


    @property
    def public(self):
        return self._public_scope


    @property
    def protected(self):
        return self._protected_scope


    @property
    def private(self):
        return self._private_scope


    def find_variable_by_name(self, name: str):
        scope_list = [self._private_scope, self._public_scope, self._protected_scope]
        for scope in scope_list:
            variable_list = scope._variables
            for var in variable_list:
                if _basic_mach_object_by_attributes(var, {"name": name}):
                    return var
        return None


    def add_base_class(self, base_class, inheritance_type="public"):
        if isinstance(base_class, str):
            bcl = CppClass(base_class)
            self._base_classes[base_class] = {"class": bcl, "inheritance_type": inheritance_type}
            return self

        self._base_classes[base_class.name] = {"class": base_class, "inheritance_type": inheritance_type}
        return self


    def get_base_class(self, class_name: str):
        if not class_name in self._base_classes:
            return None
        return self._base_classes[class_name]


    def gen_definition_str(self):
        def gen_from_scope(scope: CppClassScope) -> str:
            if scope.empty():
                return ""

            result_str = ""

            if scope._custom_body:
                result_str += f"\n{scope._custom_body}\n"

            constructor_list = scope._constructors
            method_list = scope._methods
            variable_list = scope._variables

            # constructor
            result_str += "\n".join([constructor.definition().replace("<class_name>", self._class_name) for constructor in constructor_list])

            # methods
            result_str += "\n".join([method.definition() for method in method_list])

            # variables
            result_str += "\n".join([var.definition_in_class() for var in variable_list])
            result_str += '\n'
            return result_str

        class_str = f'{self._class_type} {self._class_name}'
        if self._base_classes:
            class_str += " : "
            b_class_list = [f'{self._base_classes[x]["inheritance_type"]} {x}' for x in self._base_classes]
            class_str += ", ".join(b_class_list)

        class_str += ' { '

        # public scope
        if not self._public_scope.empty():
            class_str += "\npublic:\n"
            class_str += gen_from_scope(self.public)

        # protected scope
        if not self._protected_scope.empty():
            class_str += "\nprotected:\n"
            class_str += gen_from_scope(self.protected)

        # private scope
        if not self._private_scope.empty():
            class_str += "\nprivate:\n"
            class_str += gen_from_scope(self.private)

        # end genereation
        class_str += " }; "
        return class_str


    def get_declaration_str(self):
        return ""


from enum import Enum

class DumpType(Enum):
    DECLARATION = 0
    DEFINITION = 1


class DumpScopeType(Enum):
    INSIDE_CLASS = 0
    OUTSIDE_CLASS = 1


def __dumpCppType(object: CppType) -> str:
    return object.type


def __dumpCppVariable(object: CppVariable, type: DumpType, scopeType: DumpScopeType):
    result_str = ""
    if object.static:
        result_str += "static "

    result_str += f'{__dumpCppType(object.var_type)} {object.name}'
    if type == DumpType.DECLARATION and object.value:
        result_str += str(object.value)
    result_str += ";"

    return result_str


def __dumpCppVariableAsArg(object: CppVariable) -> str:
    return f'{__dumpCppType(object.var_type)} {object.name}'


def __dumpCppVariableInClass(object: CppVariable, type: DumpType, scopeType: DumpScopeType) -> str:
    result_str = ""
    if object.static:
        result_str += "static "

    result_str += f'{__dumpCppType(object.var_type)} '
    if type == DumpType.DEFINITION and scopeType.INSIDE_CLASS:
        result_str += f'{_getClassPrefixedVariableName(object.name)};'
    elif type == DumpType.DECLARATION and scopeType.INSIDE_CLASS:
        result_str += f'{_getClassPrefixedVariableName(object.name)}'
        if object.value:
            result_str += f" = {object.value};"
        else:
            result_str += ";"
    elif scopeType.OUTSIDE_CLASS:
        result_str += f'<class_name>::{_getClassPrefixedVariableName(object.name)}'
        if object.value:
            result_str += f" = {object.value};"
        else:
            result_str += ";"

    return result_str


def __dumpCppFunction(object: CppFunction, type: DumpType, scopeType: DumpScopeType) -> str:
    pass


def __dumpCppFunctionInClass(object: CppFunction, type: DumpType, scopeType: DumpScopeType) -> str:
    pass


def CppDump(object, type: DumpType = DumpType.DEFINITION, scopeType: DumpScopeType = DumpScopeType.INSIDE_CLASS) -> str:
    if isinstance(object, CppType):
        return __dumpCppType(object)

    if isinstance(object, CppVariable):
        return __dumpCppVariable(object, type, scopeType)

    raise Exception("Unknown type for dump!")
