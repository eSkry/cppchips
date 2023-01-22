# cppchips: Автогенератор кода C++17

![a](https://img.shields.io/github/commit-activity/y/eSkry/cppchips?style=flat-square) ![license](https://img.shields.io/github/license/eSkry/cppchips?style=flat-square)

--------------------------------------

Языки: [EN](../README.md) **RU**


## Поддерживаемые конструкции C++
- **class** и **struct**.
- **class constructors**.
- **Переменные класса** - with autogeneration getter and setter.
- **initializer list** in constructor (withoout initialize base class).
- **Методы класса**.
- функции, переменные


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