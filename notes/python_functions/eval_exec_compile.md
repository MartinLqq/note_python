# [Python中的eval()、exec()及其相关函数](http://www.cnblogs.com/yyds/p/6276746.html)

## 1. eval函数

------

#### 函数的作用：

计算指定表达式的值。也就是说它要执行的Python代码只能是单个运算表达式（注意eval不支持任意形式的赋值操作），而不能是复杂的代码逻辑，这一点和lambda表达式比较相似。

#### 函数定义：

```
eval(expression, globals=None, locals=None)
```

#### 参数说明：

- expression：必选参数，可以是字符串，也可以是一个任意的code对象实例（可以通过compile函数创建）。如果它是一个字符串，它会被当作一个（使用globals和locals参数作为全局和本地命名空间的）Python表达式进行分析和解释。
- globals：可选参数，表示全局命名空间（存放全局变量），如果被提供，则必须是一个字典对象。
- locals：可选参数，表示当前局部命名空间（存放局部变量），如果被提供，可以是任何映射对象。如果该参数被忽略，那么它将会取与globals相同的值。
- 如果globals与locals都被忽略，那么它们将取eval()函数被调用环境下的全局命名空间和局部命名空间。

#### 返回值：

- 如果expression是一个code对象，且创建该code对象时，compile函数的mode参数是'exec'，那么eval()函数的返回值是None；
- 否则，如果expression是一个输出语句，如print()，则eval()返回结果为None；
- 否则，expression表达式的结果就是eval()函数的返回值；

#### 实例：

```
x = 10

def func():
    y = 20
    a = eval('x + y')
    print('a: ', a)
    b = eval('x + y', {'x': 1, 'y': 2})
    print('b: ', b)
    c = eval('x + y', {'x': 1, 'y': 2}, {'y': 3, 'z': 4})
    print('c: ', c)
    d = eval('print(x, y)')
    print('d: ', d)

func()
```

**输出结果：**

```
a:  30
b:  3
c:  4
10 20
d:  None
```

**对输出结果的解释：**

- 对于变量a，eval函数的globals和locals参数都被忽略了，因此变量x和变量y都取得的是eval函数被调用环境下的作用域中的变量值，即：x = 10, y = 20，a = x + y = 30
- 对于变量b，eval函数只提供了globals参数而忽略了locals参数，因此locals会取globals参数的值，即：x = 1, y = 2，b = x + y = 3
- 对于变量c，eval函数的globals参数和locals都被提供了，那么eval函数会先从全部作用域globals中找到变量x, 从局部作用域locals中找到变量y，即：x = 1, y = 3, c = x + y = 4
- 对于变量d，因为print()函数不是一个计算表达式，没有计算结果，因此返回值为None

## 2. exec函数

------

#### 函数的作用：

动态执行Python代码。也就是说exec可以执行复杂的Python代码，而不像eval函数那么样只能计算一个表达式的值。

#### 函数定义：

```
exec(object[, globals[, locals]])
```

#### 参数说明：

- object：必选参数，表示需要被指定的Python代码。它必须是字符串或code对象。如果object是一个字符串，该字符串会先被解析为一组Python语句，然后在执行（除非发生语法错误）。如果object是一个code对象，那么它只是被简单的执行。
- globals：可选参数，同eval函数
- locals：可选参数，同eval函数

#### 返回值：

exec函数的返回值永远为None.

> 需要说明的是在Python 2中exec不是函数，而是一个内置语句(statement)，但是Python 2中有一个execfile()函数。可以理解为Python 3把exec这个statement和execfile()函数的功能够整合到一个新的exec()函数中去了：

#### eval()函数与exec()函数的区别：

- eval()函数只能计算单个表达式的值，而exec()函数可以动态运行代码段。
- eval()函数可以有返回值，而exec()函数返回值永远为None。

#### 实例1：

我们把实例1中的eval函数换成exec函数试试：

```
x = 10

def func():
    y = 20
    a = exec('x + y')
    print('a: ', a)
    b = exec('x + y', {'x': 1, 'y': 2})
    print('b: ', b)
    c = exec('x + y', {'x': 1, 'y': 2}, {'y': 3, 'z': 4})
    print('c: ', c)
    d = exec('print(x, y)')
    print('d: ', d)

func()
```

**输出结果：**

```
a:  None
b:  None
c:  None
10 20
d:  None
```

因为我们说过了，exec函数的返回值永远为None。

#### 实例2：

```
x = 10
expr = """
z = 30
sum = x + y + z
print(sum)
"""
def func():
    y = 20
    exec(expr)
    exec(expr, {'x': 1, 'y': 2})
    exec(expr, {'x': 1, 'y': 2}, {'y': 3, 'z': 4})
    
func()
```

**输出结果：**

```
60
33
34
```

**对输出结果的解释：**

前两个输出跟上面解释的eval函数执行过程一样，不做过多解释。关于最后一个数字34，我们可以看出是：x = 1, y = 3是没有疑问的。关于z为什么还是30而不是4，这其实也很简单，我们只需要在理一下代码执行过程就可以了，其执行过程相当于：

```
x = 1
y = 2

def func():
    y = 3
    z = 4
    
    z = 30
    sum = x + y + z
    print(sum)

func()
```

## 3. globals()与locals()函数

------

#### 函数定义及功能说明：

先来看下这两个函数的定义和文档描述

```
print( globals() )
```

**描述：** Return a dictionary representing the current global symbol table. This is always the dictionary of the current module (inside a function or method, this is the module where it is defined, not the module from which it is called).

**翻译：** 返回一个表示当前全局标识符表的字典。这永远是当前模块的字典（在一个函数或方法内部，这是指定义该函数或方法的模块，而不是调用该函数或方法的模块）

```
print( locals() )
```

**描述：** Update and return a dictionary representing the current local symbol table. Free variables are returned by locals() when it is called in function blocks, but not in class blocks.

> **Note** The contents of this dictionary should not be modified; changes may not affect the values of local and free variables used by the interpreter.

**翻译：** 更新并返回一个表示当前局部标识符表的字典。自由变量在函数内部被调用时，会被locals()函数返回；自由变量在类累不被调用时，不会被locals()函数返回。

> **注意：** locals()返回的字典的内容不应该被改变；如果一定要改变，不应该影响被解释器使用的局部变量和自由变量。

#### 总结：

- globals()函数以字典的形式返回的定义该函数的模块内的全局作用域下的所有标识符（变量、常量等）
- locals()函数以字典的形式返回当前函数内的局域作用域下的所有标识符
- 如果直接在模块中调用globals()和locals()函数，它们的返回值是相同的

#### 实例1：

```
name = 'Tom'
age = 18

def func(x, y):
    sum = x + y
    _G = globals()
    _L = locals()
    print(id(_G), type(_G),  _G)
    print(id(_L), type(_L), _L)

func(10, 20)
```

输出结果：

```
2131520814344 <class 'dict'> {'__builtins__': <module 'builtins' (built-in)>, 'func': <function func at 0x000001F048C5E048>, '__doc__': None, '__file__': 'C:/Users/wader/PycharmProjects/LearnPython/day04/func5.py', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x000001F048BF4C50>, '__spec__': None, 'age': 18, '__name__': '__main__', 'name': 'Tom', '__package__': None, '__cached__': None}
2131524302408 <class 'dict'> {'y': 20, 'x': 10, '_G': {'__builtins__': <module 'builtins' (built-in)>, 'func': <function func at 0x000001F048C5E048>, '__doc__': None, '__file__': 'C:/Users/wader/PycharmProjects/LearnPython/day04/func5.py', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x000001F048BF4C50>, '__spec__': None, 'age': 18, '__name__': '__main__', 'name': 'Tom', '__package__': None, '__cached__': None}, 'sum': 30}
```

#### 实例2：

```
name = 'Tom'
age = 18

G = globals()
L = locals()
print(id(G), type(G), G)
print(id(L), type(L), L)
```

输出结果：

```
2494347312392 <class 'dict'> {'__file__': 'C:/Users/wader/PycharmProjects/LearnPython/day04/func5.py', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x00000244C2E44C50>, 'name': 'Tom', '__spec__': None, '__builtins__': <module 'builtins' (built-in)>, '__cached__': None, 'L': {...}, '__package__': None, '__name__': '__main__', 'G': {...}, '__doc__': None, 'age': 18}
2494347312392 <class 'dict'> {'__file__': 'C:/Users/wader/PycharmProjects/LearnPython/day04/func5.py', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x00000244C2E44C50>, 'name': 'Tom', '__spec__': None, '__builtins__': <module 'builtins' (built-in)>, '__cached__': None, 'L': {...}, '__package__': None, '__name__': '__main__', 'G': {...}, '__doc__': None, 'age': 18}
```

上面打印出的G和L的内存地址是一样的，说明在模块级别locals()的返回值和globals()的返回值是相同的。

## 4. compile函数

------

#### 函数的作用：

将source编译为code对象或AST对象。code对象能够通过exec()函数来执行或者通过eval()函数进行计算求值。

#### 函数定义：

```
compile(source, filename, mode[, flags[, dont_inherit]])
```

#### 参数说明：

- source：字符串或AST（Abstract Syntax Trees）对象，表示需要进行编译的Python代码
- filename：指定需要编译的代码文件名称，如果不是从文件读取代码则传递一些可辨认的值（通常是用'<string>'）
- mode：用于标识必须当做那类代码来编译；如果source是由一个代码语句序列组成，则指定mode='exec'；如果source是由单个表达式组成，则指定mode='eval'；如果source是由一个单独的交互式语句组成，则指定mode='single'。
- 另外两个可选参数暂不做介绍

#### 实例：

```
s = """
for x in range(10):
    print(x, end='')
print()
"""
code_exec = compile(s, '<string>', 'exec')
code_eval = compile('10 + 20', '<string>', 'eval')
code_single = compile('name = input("Input Your Name: ")', '<string>', 'single')

a = exec(code_exec)
b = eval(code_eval)

c = exec(code_single)
d = eval(code_single)

print('a: ', a)
print('b: ', b)
print('c: ', c)
print('name: ', name)
print('d: ', d)
print('name; ', name)
```

输出结果：

```
0123456789
Input Your Name: Tom
Input Your Name: Jerry
a:  None
b:  30
c:  None
name:  Jerry
d:  None
name;  Jerry
```

## 5. 这几个函数的关系

------

comiple()函数、globals()函数、locals()函数的返回结果可以当作eval()函数与exec()函数的参数使用。

另外，我们可以通过判断globals()函数的返回值中是否包含某个key来判断，某个全局变量是否已经存在（被定义）。