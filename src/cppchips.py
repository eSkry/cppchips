from typing import List

CLASS_MEMBER_PREFIX='m'
FUNCTION_ARGUMENT_PREFIX='a'
GETTER_PREFIX="get"
SETTER_PREFIX="set"
DEFAULT_STRING_TYPE="std::string"


class CppDefDeclInterface:
    '''Класс интерфейс для всех типов которые имеют декларацию и дефиницию.'''
    def __init__(self) -> None:
        pass


    def declaration(self) -> str:
        return 'Error: Declaration not implemented.'


    def definition(self) -> str:
        return 'Error: Definition not implemented.'


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


    def __str__(self) -> str:
        return self.type


class CppVoid(CppType):
    def __init__(self, pointer=False):
        super().__init__(name='void', description='void type', reference=False, pointer=pointer)


    def valid(self) -> bool:
        if self._reference or not self._pointer:
            return False

        return True


class TypeWithUnsigned(CppType):
    def __init__(self, name: str, description=None, reference=False, pointer=False, unsigned=False):
        super().__init__(name, description, reference, pointer)
        self._unsigned = unsigned


    @property
    def _unsigned(self):
        return self._unsigned


    @_unsigned.setter
    def _unsigned(self, value: bool):
        self._unsigned = value


    @property
    def type_unsigned(self):
        return f'unsigned {self.type}'


    @property
    def type_signed(self):
        return f'{self.type}'


    @property
    def type(self) -> str:
        if self._unsigned:
            return self.type_unsigned
        return self.type_signed


class CppChar(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False):
        super().__init__(name='char', description='char type', reference=reference, pointer=pointer, unsigned=unsigned)


class CppInt(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False) -> None:
        super().__init__(name='int', description='int type', reference=reference, pointer=pointer, unsigned=unsigned)


class CppFloat(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False):
        super().__init__(name='float', description='float type', reference=reference, pointer=pointer, unsigned=unsigned)


class CppDouble(TypeWithUnsigned):
    def __init__(self, reference=False, pointer=False, unsigned=False):
        super().__init__(name='double', description='double type', reference=reference, pointer=pointer, unsigned=unsigned)


class CppString(CppType):
    def __init__(self, reference=False, pointer=False):
        super().__init__(DEFAULT_STRING_TYPE, 'C++ string type', reference, pointer)


class CppAuto(CppType):
    def __init__(self, reference=False, pointer=False, rvalue_ref=False):
        super().__init__('auto', 'c++ auto type', reference, pointer, rvalue_ref)


class CppNONE(CppType):
    '''CppNONE - Тип заглушка. Необходим для использования в конструкторах класса'''
    def __init__(self):
        super().__init__('')


class CppVariable():
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
    def var_static_const(self) -> str:
        return f'static const {self._type.type} {self._name}'


    @property
    def var(self) -> str:
        if self._static:
            return f'{self.var_static}'

        return f'{self._type.type} {self._name}'


    @property
    def definition(self) -> str:
        if not self._value:
            return f'{self._type.type} {self._name};'

        return f'{self._type.type} {self._name} = {str(self._value)};'


    @property
    def declaration(self):
        return f'{self._type.type} {self._name};'


# Типизированный список переменных
CppVariableList = List[CppVariable]


class CppFunction:
    '''CppFunction - Клас который представляет собой функции и методы из C++'''


    def __init__(self, name: str, ret_t: CppType, args: CppVariableList = [], body=None, static=False, constexpr=False, noexcept=False, const=False):
        self._name = name
        self._ret_t = ret_t
        self._args = args
        self._static = static
        self._constexpr = constexpr
        self._body = body
        self._noexcept = noexcept
        self._const = const


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
        '''get_definition - Определяет функцию вместе с ее телом'''


        fdc_str = f"<static><constexpr>{str(self._ret_t)} {self._name}({self._get_arg_list()})<const><noexcept> {{\n<body>\n}}"

        fdc_str = fdc_str.replace("<static>", "static " if self._static else "")
        fdc_str = fdc_str.replace("<constexpr>", "constexpr " if self._constexpr else "")
        fdc_str = fdc_str.replace("<body>", self._body if self._body else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self._noexcept else "")
        fdc_str = fdc_str.replace("<const>", " const" if self._const else "")

        return fdc_str


    def declaration(self) -> str:
        fdf_str = f"<static><constexpr>{str(self._ret_t)} {self._name}({self._get_arg_list()})<const><noexcept>;"

        fdf_str = fdf_str.replace("<static>", "static " if self._static else "")
        fdf_str = fdf_str.replace("<constexpr>", "constexpr " if self._constexpr else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self._noexcept else "")
        fdf_str = fdf_str.replace("<const>", " const" if self._const else "")

        return fdf_str


    def __str__(self) -> str:
        return self.definition()


CppFunctionList = List[CppFunction]


class CppConstructor(CppFunction):
    def __init__(self, args: CppVariableList = [], body=None, constexpr=False, deleted=False, default=False, initializer_list: CppVariableList = []):
        super().__init__('', CppNONE(), args, body, constexpr)
        self.deleted = deleted
        self.default = default
        self.initializer_list = initializer_list


    def arg_count(self):
        return len(self._args)


    def definition(self) -> str:
        if self.deleted or self.default:
            return ""

        fdc_str = f"<constexpr>{str(self._ret_t)} <class_name>({self._get_arg_list()})<noexcept> <initializer_list>{{\n<body>\n}}"

        fdc_str = fdc_str.replace("<constexpr>", "constexpr" if self._constexpr else "")
        fdc_str = fdc_str.replace("<body>", self._body if self._body else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self._noexcept else "")

        if len(self.initializer_list) > 0:
            init_list = " : "
            # todo: Релазиовать инициализацию конструктора базового класса
            init_strs = []
            for arg in self._args:
                if arg in self.initializer_list:
                    init_strs.append(f'{arg.name}{{{arg.name}}}')

            init_list += ", ".join(init_strs)

            fdc_str = fdc_str.replace("<initializer_list>", init_list)
        else:
            fdc_str = fdc_str.replace("<initializer_list>", "")

        return fdc_str


    def declaration(self) -> str:
        fdf_str = f"<constexpr> <class_name>({self._get_arg_list()})<noexcept><deleted><default>;"

        fdf_str = fdf_str.replace("<constexpr>", "constexpr" if self._constexpr else "")
        fdf_str = fdf_str.replace("<deleted>", " = deleted;" if self.deleted else "")
        fdf_str = fdf_str.replace("<default>", " = default;" if self.default else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self._noexcept else "")

        return fdf_str


    def __str__(self) -> str:
        return self.definition


CppConstructorList = List[CppConstructor]


class CppClassVariable(CppVariable):
    def __init__(self, type: CppType, name: str, value=None, static=False, with_getter=False, with_setter=False) -> None:
        super().__init__(type, name, value, static)
        self._with_getter = with_getter
        self._with_setter = with_setter


    @property
    def setter(self):
        return self._with_setter


    @property
    def getter(self):
        return self._with_getter


CppClassVariableList = List[CppClassVariable]


class CppClassScope:
    def __init__(self) -> None:
        self.methods: CppFunctionList = []
        self.variables: CppClassVariableList  = []
        self.constructors: CppConstructorList = []


    def contains_variable(self, var: CppClassVariable):
        return var in self.variables


    def empty(self):
        if not self.methods and not self.variables and not self.constructors:
            return True
        return False


class CppClass:
    def __init__(self, name: str, base_classes={}, class_type="class") -> None:
        self._name = name
        self._base_classes = base_classes
        self._type = CppType(name=name)
        self._class_type = class_type

        self._scope = {"public": CppClassScope()
                    , "protected": CppClassScope()
                    , "private": CppClassScope()}


    @property
    def type(self):
        return self._type


    def add_variable(self, var: CppClassVariable, scope="public"):
        self._scope[scope].variables.append(var)
        if var.getter:
            ret_const_ref_t = CppType(var.var_type._name, reference=True, const=True)
            ret_ref_t = CppType(var.var_type._name, reference=True)
            self.add_method(CppFunction(GETTER_PREFIX + var.name, ret_const_ref_t, body=f'return {var.name};', noexcept=True, const=True))
            self.add_method(CppFunction(GETTER_PREFIX + var.name, ret_ref_t, body=f'return {var.name};', noexcept=True))
        if var.setter:
            set_ref_t = CppType(var.var_type._name, reference=True)
            arg = CppVariable(set_ref_t, 'value')
            self.add_method(CppFunction(SETTER_PREFIX + var.name, CppVoid(), [arg], f'this->{var.name} = {arg.name};'))


    def add_method(self, method: CppFunction, scope="public"):
        self._scope[scope].methods.append(method)


    def add_base_class(self, class_name, inheritance="public"):
        if isinstance(class_name, str):
            self._base_classes[class_name] = {"class_name": class_name, "inheritance": inheritance}
        else:
            # Предполагается что передается тип CppClass
            self._base_classes[class_name._name] = {"class_name": class_name._name, "class": class_name, "inheritance": inheritance}


    # def remove_method(self, name: str):
    #     self._methods.pop(name, None)

    def remove_variable(self, var: str):
        if isinstance(var, str):
            for scope in self._scope:
                for var in self._scope[scope].variables:
                    if var.name == var:
                        self._scope[scope].pop(var, None)
                        return

        if isinstance(var, CppClassVariable):
            name = var.name
            for scope in self._scope:
                for var in self._scope[scope].variables:
                    if var.name == var:
                        self._scope[scope].pop(var, None)
                        return


    def has_variable(self, var: CppClassVariable):
        for scope in self._scope:
            if self._scope[scope].contains_variable(var):
                return True
        return False


    def remove_base_class(self, name: str):
        self._base_classes.pop(name, None)


    def add_constructor(self, constructor: CppConstructor, scope="public"):
        self._scope[scope].constructors.append(constructor)


    def add_empty_constructor(self, scope="public"):
        self._scope[scope].constructors.append(CppConstructor())


    def add_full_constructor(self, scope="public"):
        '''Добавляет конструктор у которого количество аргументов равно количеству переменных'''

        vars = []
        vars += self._scope["public"].variables
        vars += self._scope["protected"].variables
        vars += self._scope["private"].variables

        constr = CppConstructor(args=vars, initializer_list=vars)
        self._scope[scope].constructors.append(constr)


    def get_definition(self):
        class_str = f'{self._class_type} {self._name}'
        if self._base_classes:
            class_str += " : "
            b_class_list = [f'{str(self._base_classes[x]["inheritance"])} {self._base_classes[x]["class_name"]}' for x in self._base_classes]
            class_str += ", ".join(b_class_list)

        class_str += ' { '


        for scope_name in self._scope:
            cur_scope = self._scope[scope_name]
            if cur_scope.empty():
                continue

            class_str += f'\n{scope_name}:\n'

            # constructors
            class_str += "\n".join([constructor.definition().replace("<class_name>", self._name) for constructor in cur_scope.constructors])
            class_str += '\n'

            # methods
            class_str += "\n".join([method.definition() for method in cur_scope.methods])
            class_str += '\n'

            # variables
            class_str += "\n".join([variable.definition for variable in cur_scope.variables])
            class_str += '\n'


        class_str += "\n};"

        return class_str


    def get_declaration(self):
        pass


    def __str__(self) -> str:
        return self.get_definition()

