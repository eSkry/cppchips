from src.CppType import CppType
from src import CppBaseTypes
from src.CppFunction import CppFunction
from src.CppVariable import CppVariable
from src.CppClass import CppClass


# CppType
cppType1 = CppType('MyClassName', const=True)
print(cppType1) # const MyClassName
cppType1.is_pointer = True
print(cppType1) # const MyClassName*


# CppVariable
cppVar = CppVariable(cppType1, 'myVar', value="fdsf")
print(cppVar) # const MyClassName* myVar = fdsf


print(CppFunction('HelloFunction'
                        , CppBaseTypes.CppInt()
                        , [CppVariable(CppBaseTypes.CppFloat(const=True, reference=True), name='arg1')]
                        , body='auto shrd = std::make_shared<int>();').get_declaration_string())



clB = CppClass('BaseClass')
cl = CppClass('HelloClass')
cl.add_base_class(clB, "public")


print(str(cl))