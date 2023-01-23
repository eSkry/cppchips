from src.cppchips import *


# print(dir(CppConstructor()))

# print(CppDump(CppVariable(CppInt(), 'hehe')))

animalClass = CppClass('Animal')
animalClass.private \
                .add_variable(CppString(), 'var1') \

animalClass.public \
                .add_virtual_method('say', CppVoid(), [], 'std::cout << "---\\n";', noexcept=True) \
                .add_virtual_method('pay', CppInt(), [CppVariable(CppDouble(), 'cost')], '// pay to win!') \
                .add_constructor(default=True) \
                .add_getter('var1') \
                .add_setter('var1') \
                .add_deleted_virtual_method('good_virtual_method', CppInt(), [CppVariable(CppInt(), 'good_var')]) \
                .add_method('method1', CppChar(), [CppVariable(CppString(True), 'arg1'), CppVariable(CppBool(), 'arg2')])

print(animalClass.gen_definition_str())


catClass = CppClass('Cat')
catClass.add_base_class(animalClass).public \
                                    .add_override_method('say') \
                                    .add_constructor() \
                                    .add_override_method('pay') \
                                    .add_override_method('good_virtual_method') \
                                    .add_overload_base_method('method1', [], '// sey hello')

print(catClass.gen_definition_str())
