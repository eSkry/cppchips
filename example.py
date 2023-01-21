from src.CppType import CppType
from src import CppBaseTypes
from src.CppFunction import CppFunction
from src.CppVariable import CppVariable
from src.CppClass import CppClass

print(CppType('int', description="hhh", reference=True))
print(CppType('int', pointer=True))
print(CppType('int', const=True, pointer=True))
print(CppBaseTypes.CppDouble())


print(CppFunction('HelloFunction'
                        , CppBaseTypes.CppInt()
                        , [CppVariable(CppBaseTypes.CppFloat(const=True, reference=True), name='arg1')]
                        , body='auto shrd = std::make_shared<int>();').get_declaration_string())



clB = CppClass('BaseClass')
cl = CppClass('HelloClass')
cl.add_base_class(clB, "public")


print(str(cl))