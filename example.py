from src.cppchips import *

animalClass = CppClass('Animal')
animalClass.private \
                .add_variable(CppString(), 'var1') \

animalClass.public \
                .add_virtual_method('say', CppVoid(), [], 'std::cout << "---\\n";', noexcept=True) \
                .add_virtual_method('pay', CppInt(), [CppVariable(CppDouble(), 'cost')], '// pay to win!') \
                .add_constructor() \
                .add_getter('var1') \
                .add_setter('var1')

print(animalClass.gen_definition_str())


catClass = CppClass('Cat')
catClass.add_base_class(animalClass).public \
                                    .add_override_method('say') \
                                    .add_constructor() \
                                    .add_override_method('pay')

print(catClass.gen_definition_str())
