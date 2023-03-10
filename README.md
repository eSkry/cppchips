# cppchips: C++17 code generator

#### :exclamation: Early development stage :vertical_traffic_light:

![a](https://img.shields.io/github/commit-activity/y/eSkry/cppchips?style=flat-square) ![license](https://img.shields.io/github/license/eSkry/cppchips?style=flat-square)

--------------------------------------

#### :capital_abcd: Languages: **EN** [RU](docs/README.ru.md)

#### :four_leaf_clover: Supported C++ constructions
- **class** and **struct**.
- **class constructors**.
- **class member fields** - with autogeneration getter and setter.
- **initializer list** in constructor (withoout initialize base class).
- **class member functions**.
- **virtual** functions and **override in child classes**.
- simple functions, variables.
- **method overloading**


## :rocket: Simple start

**cppchips input**:
```python
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
```

**C++ result**:
```cpp
class Animal {
public:
  Animal() {}
  virtual void say() noexcept { std::cout << "---\n"; }
  virtual int pay(double cost) {
    // pay to win!
  }
  auto &getvar1() noexcept { return mvar1; }
  const auto &getvar1() const noexcept { return mvar1; }
  void setvar1(const std::string &avar1) { mvar1 = avar1; }

private:
  std::string mvar1;
};

class Cat : public Animal {
public:
  Cat() {}
  void say() noexcept override {}
  int pay(double cost) override { return {}; }
};
```