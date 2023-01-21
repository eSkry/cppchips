

MEMBER_PREFIX='m'
ARGUMENT_PREFIX='a'
GETTER_PREFIX="get"
SETTER_PREFIX="set"


class CppType:

    def __init__(self, name: str, description=None, const=False, reference=False, pointer=False, rvalue_ref=False):
        self._name = name
        self._const = const
        self._reference = reference
        self._pointer = pointer
        self._description = description
        self._rvalue_ref = rvalue_ref

    @property
    def is_rvalue(self):
        return self._rvalue_ref

    @is_rvalue.setter
    def is_rvalue(self, value: bool):
        self._rvalue_ref = value


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

    def __str__(self) -> str:
        type_str = f'{"const " if self._const else ""}{self._name}'

        if self._rvalue_ref:
            type_str += "&&"
        elif self._reference:
            type_str += "&"
        elif self._pointer:
            type_str += "*"

        return type_str



class CppVoid(CppType):
    def __init__(self, const=False, pointer=False):
        super().__init__(name='void', description='void type', const=const, reference=False, pointer=pointer)

    def __str__(self) -> str:
        return super().__str__()

    def valid(self) -> bool:
        if self._reference or (self._const and not self._pointer):
            return False

        return True



class TypeWithUnsigned(CppType):
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


class CppString(CppType):
    def __init__(self, const=False, reference=False, pointer=False):
        super().__init__('std::string', 'C++ string type', const, reference, pointer)

    def __str__(self) -> str:
        return super().__str__()


class CppNONE(CppType):
    def __init__(self, const=False, reference=False, pointer=False):
        super().__init__('', const, reference, pointer)


class CppVariable:
    def __init__(self, type: CppType, name: str, value=None, static=False) -> None:
        self._type = type
        self._name = name
        self._static = static
        self._value = value


    @property
    def name_on_args(self):
        return f'{ARGUMENT_PREFIX}{self.name}'

    @property
    def name_on_clas(self):
        return f'{MEMBER_PREFIX}{self.name}'


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
    '''CppFunction - Клас который представляет собой функции и методы из C++'''

    def __init__(self, name: str, ret_t: CppType, args=[], body=None, static=False, constexpr=False, noexcept=False, const=False):
        self.name = name
        self.ret_t = ret_t
        self.args = args
        self.static = static
        self.constexpr = constexpr
        self.body = body
        self.noexcept = noexcept
        self.const = const


    def _get_arg_list(self) -> str:
        args = [str(x) for x in self.args]
        return ", ".join(args)


    def get_definition(self) -> str:
        '''get_definition - Определяет функцию вместе с ее телом'''
        fdc_str = f"<static><constexpr>{str(self.ret_t)} {self.name}({self._get_arg_list()})<const><noexcept> {{\n<body>\n}}"

        fdc_str = fdc_str.replace("<static>", "static " if self.static else "")
        fdc_str = fdc_str.replace("<constexpr>", "constexpr " if self.constexpr else "")
        fdc_str = fdc_str.replace("<body>", self.body if self.body else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self.noexcept else "")
        fdc_str = fdc_str.replace("<const>", " const" if self.const else "")

        return fdc_str


    def get_declaration(self) -> str:
        fdf_str = f"<static><constexpr>{str(self.ret_t)} {self.name}({self._get_arg_list()})<const><noexcept>;"

        fdf_str = fdf_str.replace("<static>", "static " if self.static else "")
        fdf_str = fdf_str.replace("<constexpr>", "constexpr " if self.constexpr else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self.noexcept else "")
        fdf_str = fdf_str.replace("<const>", " const" if self.const else "")

        return fdf_str


    def __str__(self) -> str:
        return self.get_definition()



class CppConstructor(CppFunction):
    def __init__(self, args=[], body=None, constexpr=False, deleted=False, default=False, initializer_list=[]):
        super().__init__('', CppNONE(), args, body, constexpr)
        self.deleted = deleted
        self.default = default
        self.initializer_list = initializer_list

    def arg_count(self):
        return len(self.args)

    def get_definition(self) -> str:
        if self.deleted or self.default:
            return ""

        fdc_str = f"<constexpr>{str(self.ret_t)} <class_name>({self._get_arg_list()})<noexcept> <initializer_list>{{\n<body>\n}}"

        fdc_str = fdc_str.replace("<constexpr>", "constexpr" if self.constexpr else "")
        fdc_str = fdc_str.replace("<body>", self.body if self.body else "")
        fdc_str = fdc_str.replace("<noexcept>", " noexcept" if self.noexcept else "")

        if len(self.initializer_list) > 0:
            init_list = " : "
            # todo: Релазиовать инициализацию конструктора базового класса
            init_strs = []
            for arg in self.args:
                if arg in self.initializer_list:
                    init_strs.append(f'{arg.name}{{{arg.name}}}')

            init_list += ", ".join(init_strs)

            fdc_str = fdc_str.replace("<initializer_list>", init_list)
        else:
            fdc_str = fdc_str.replace("<initializer_list>", "")

        return fdc_str


    def get_declaration(self) -> str:
        fdf_str = f"<constexpr> <class_name>({self._get_arg_list()})<noexcept><deleted><default>;"

        fdf_str = fdf_str.replace("<constexpr>", "constexpr" if self.constexpr else "")
        fdf_str = fdf_str.replace("<deleted>", " = deleted;" if self.deleted else "")
        fdf_str = fdf_str.replace("<default>", " = default;" if self.default else "")
        fdf_str = fdf_str.replace("<noexcept>", " noexcept" if self.noexcept else "")

        return fdf_str


    def __str__(self) -> str:
        return self.get_definition()



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


class CppClassScope:
    def __init__(self) -> None:
        self.methods = []
        self.variables = []
        self.constructors = []

    def contains_variable(self, var: CppClassVariable):
        return var in self.variables

    def empty(self):
        if not self.methods and not self.variables and not self.constructors:
            return True
        return False


class CppClass:
    def __init__(self, name: str, base_classes={}) -> None:
        self._name = name
        self._base_classes = base_classes
        self._type = CppType(name=name)

        self._scope = {"public": CppClassScope()
                    , "protected": CppClassScope()
                    , "private": CppClassScope()}


    @property
    def type(self):
        return self._type


    def add_variable(self, var: CppClassVariable, scope="public"):
        self._scope[scope].variables.append(var)
        if var.getter:
            ret_const_ref_t = CppType(var.type._name, reference=True, const=True)
            ret_ref_t = CppType(var.type._name, reference=True)
            self.add_method(CppFunction(GETTER_PREFIX + var.name, ret_const_ref_t, body=f'return {var.name};', noexcept=True, const=True))
            self.add_method(CppFunction(GETTER_PREFIX + var.name, ret_ref_t, body=f'return {var.name};', noexcept=True))
        if var.setter:
            set_ref_t = CppType(var.type._name, reference=True)
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
        class_str = f'class {self._name}'
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
            class_str += "\n".join([constructor.get_definition().replace("<class_name>", self._name) for constructor in cur_scope.constructors])
            class_str += '\n'

            # methods
            class_str += "\n".join([method.get_definition() for method in cur_scope.methods])
            class_str += '\n'

            # variables
            class_str += "\n".join([variable.get_declaration() for variable in cur_scope.variables])
            class_str += '\n'


        class_str += "\n};"

        return class_str


    def get_declaration(self):
        pass


    def __str__(self) -> str:
        return self.get_definition()



class CppEnvironment:
    def __init__(self) -> None:
        self.classes = {}
        self.functions = {}
        self.namespaces = {}
        self.variables = {}


    def add_class(self, class_t: CppClass):
        self.classes[class_t._name] = class_t


    def add_function(self, function: CppFunction):
        self.functions[function.name] = function


    def add_variable(self, variable: CppVariable):
        self.variables[variable.name] = variable