# cppchips: Автогенератор кода C++17

#### :exclamation: В ранней стадии разработки :vertical_traffic_light:

![a](https://img.shields.io/github/commit-activity/y/eSkry/cppchips?style=flat-square) ![license](https://img.shields.io/github/license/eSkry/cppchips?style=flat-square)

--------------------------------------

#### :capital_abcd: Языки: [EN](../README.md) **RU**


## :four_leaf_clover: Поддерживаемые конструкции C++
- **class** и **struct**.
- **class constructors**.
- **Переменные класса** - with autogeneration getter and setter.
- **initializer list** in constructor (withoout initialize base class).
- **Методы класса**.
- функции, переменные.
- виртуальные функции и их перегрузка.


## :rocket: Быстрый старт
**Описание на cppchips**:
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

**Получаемый код на C++**:
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

## Интерфейс и классы Python

### class CppType
Определяет тип данных. Например `bool` или `int`.

**Пример использования:**
```python
myType = CppType('MyClassName', const=True, reference=False, pointer=False, rvalue_ref=False)
```


### class CppVariable
Представляет собой переменую типа `CppType`

**Пример использования:**
```python
myVariable = CppVariable(myType, 'myVarName', value="fdsf", static=False)
```

### class CppFunction

Представляет функцию С++
**Пример использования:**
```python
myFunc = CppFunction('HelloFunction'
                        , CppInt()
                        , [myVariable]
                        , body='auto shrd = std::make_shared<int>();')

print(myFunc) # int HelloFunction(const MyClassName* myVar = fdsf) { auto shrd = std::make_shared<int>(); }
print(func.get_declaration()) # int HelloFunction(const MyClassName* myVar = fdsf);
print(func.get_definition()) # int HelloFunction(const MyClassName* myVar = fdsf) { auto shrd = std::make_shared<int>(); }
```