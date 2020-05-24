# python cookbook



# 第2章 字符串和文本

## 2.1 针对任意多的分隔符拆分字符串

- 针对一个分隔符拆分字符串:  `S.split(sep=None, maxsplit=-1) -> list of strings`
- 针对任意多的分隔符拆分字符串:  `re.split()`



## 2.2 在字符串的开头或结尾处做文本匹配

**S.startswith()**

**S.endswith()**

- 匹配一种文本, 传入字符串:  S.startswith("str")
- 匹配多种文本, 传入**元组**:  S.startswith( ("str1", "str2") )



## 2.3 利用Shell通配符做文本匹配

**fnmatch.fnmatch()**

**fnmatch.fnmatchcase()**

```python
from  fnmatch import fnmatch, fnmatchcase

# fnmatch()匹配模式所采用的大小写区分规则和底层文件系统相同 (根据操作系统不同而不同)
# On OS X (Mac)
ret = fnmatch('foo.txt', '*.TXT')  # False
ret = fnmatch('foo.txt', '?oo.txt')  # True
ret = fnmatch('Dat45.csv', 'Dat[0-9].csv')  # True

# On Windows
ret = fnmatch('foo.txt', '*.TXT')  # True


# fnmatchcase() 完全按提供的大小写方式来匹配
# On OS X (Mac)
ret = fnmatchcase('foo.txt', '*.TXT')  # False
# On Windows
ret = fnmatchcase('foo.txt', '*.TXT')  # False
```



如果实际上是想匹配文件名的代码,  那应该用 `glob` 模块来实现,  参见 5.13 节



## 2.5 查找和替换文本

- 简单文本模式,  使用 `str.replace()`

- 更复杂模式,  使用 `re.sub(r"src_pattern or str", r"dst_pattern or str", src_text)`

  ```python
  import re
  
  src_text = "Today is 11/27/2020, PyCon starts 3/13/2013."
  src_pattern = r'(\d+)/(\d+)/(\d+)'
  dst_pattern = r'\3-\1-\2'  # `\3` 表示模式中捕获组的序号
  ret = re.sub(src_pattern, dst_pattern, src_text)
  print(ret)
  """
  Today is 2020-11-27, PyCon starts 2013-3-13.
  """
  ```

- 如果准备用相同的模式执行重复的替换,  可以考虑先将模式编译,  以获得更好的性能

  ```python
  text = "Today is 11/27/2020, PyCon starts 3/13/2013."
  datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
  ret = datepat.sub(r'\3-\1-\2', text)
  ```

- 更复杂模式,  使用 `re.sub(callback, src_text)`,  callback回调函数的输入参数是 `match()` 或 `find()` 的返回值,  用`.group()` 方法来提取匹配中特定的部分,  回调函数应该返回替换后的文本

  ```python
  import calendar
  import re
  
  def change_date(match):
      mon_index = int(match.group(1))
      day = match.group(2)
      year = match.group(3)
      mon_name = calendar.month_abbr[mon_index]
      return '{day} {mon_name} {year}'.format(
          day=day, mon_name=mon_name, year=year
      )
  
  if __name__ == '__main__':
      text = "Today is 11/27/2020, PyCon starts 3/13/2013."
      datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
      ret = datepat.sub(change_date, text)
      print(ret)
      """
      Today is 27 Nov 2020, PyCon starts 13 Mar 2013.
      """
  ```

- 除了想得到替换后的文本外,  还想知道一共完成了多少次的替换,  使用 `re.subn()`

  ```python
      ret, num = datepat.subn(change_date, text)
      print(ret)
      print(num)
      """
      Today is 27 Nov 2020, PyCon starts 13 Mar 2013.
      2
      """
  ```



## 2.6 以不区分大小写的方式对文本做查找和替换

- `re` 各操作加上 `flags=re.IGNORECASE `标记



## 2.8 编写多行模式的正则

问题:  希望在匹配文本时能够跨越多行

这个问题一般出现在希望使用句点 `.` 来匹配任意字符,  但是忘记了句点并不能匹配换行符时.

假设要匹配 C语言 风格的注释:

```python
import re

comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a 
              multiline comment */
'''
ret1 = comment.findall(text1)  # [' this is a comment ']
ret2 = comment.findall(text2)  # []
```

需要添加对换行符的支持:

1. 将匹配模式修改为:  `comment = re.compile(r'/\*((?:.|\n)*?)\*/')`,  得到结果:  `[' this is a \n              multiline comment ']`
   - `(?:.|\n)` 指定了一个非捕获组,  即这个组只做匹配但不捕获结果,  也不会分配组号

2. 或增加 `flags` 参数:  `comment = re.compile(r'/\*(.*?)\*/', flags=re.DOTALL)`,  得到结果: `[' this is a \n              multiline comment ']`
   - `flags=re.DOTALL` 使句点 `.` 可以匹配包括换行符的所有字符
   - 对于简单地情况,  使用`flags=re.DOTALL`,  但对于复杂情况,  通常最好的方法是定义自己的正则表达式模式,  这样无需额外的标记也能正确工作



## 2.12 文本过滤和清理









# 第7章 函数

## 7.7 在匿名函数中绑定变量的值

问题:  我们用lambda表达式定义了一个匿名函数,  但是也希望可以在函数定义时完成对特定变量的绑定

思考 a(10) 和 b(10) 的结果:

```python
>>> x = 10
>>> a = lambda y: x + y
>>> x = 20
>>> b = lambda y: x + y
>>> a(10)
30
>>> b(10)
30
```

注意:

- 上面lambda表达式中用到的 x 是一个**自由变量**,  在运行lambda函数时才进行绑定,  而不是在定义时绑定

- **lambda函数执行时 x 是多少就是多少**

- 使用 **默认参数**,  使匿名函数在定义时绑定变量,  并保持值不变:

  ```python
  >>> x = 10
  >>> a = lambda y, x=x: x + y
  >>> x = 20
  >>> b = lambda y, x=x: x + y
  >>> a(10)
  20
  >>> b(10)
  30
  ```

- lambda表达式与列表推导式一起用时 **特别注意**:  必须设置 **迭代变量** 为 **默认参数**

  ```python
  # 错误
  funcs = [lambda x: x+n for n in range(5)]
  for func in funcs:
      print(func(0))
  """
  4
  4
  4
  4
  4
  """
  
  
  # 正确
  funcs = [lambda x, n=n: x+n for n in range(5)]
  for func in funcs:
      print(func(0))
  """
  0
  1
  2
  3
  4
  """
  ```







## 7.8 让带有N个参数的可调用对象以较少的参数形式调用

- functools.partial()
- 可以将看似不兼容的代码结合起来使用

```python
import logging
import time
from functools import partial, wraps

def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):

    def decorate(func):
        log_name = name or func.__module__
        log = logging.getLogger(log_name)
        log_msg = message or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, 'level: {}, msg: {}'.format(level, log_msg))
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(new_level):
            nonlocal level
            level = new_level

        return wrapper

    return decorate


@logged(logging.CRITICAL, "example")
def spam():
    print('Spam!')
```



自定义装饰器 `@attach_wrapper` 起作用的过程:

1. 执行 `partial_ret = attach_wrapper(obj=wrapper)` 得到可调用对象: `partial(attach_wrapper, obj)` 
2. 执行 `set_level = partial_ret(func=set_level)`  # obj参数已经结合到partial中



## 7.10 在回调函数中携带额外的状态

问题:  我们正在编写需要使用回调函数的代码,  但是希望回调函数的可以携带额外的状态以便在回调函数内部使用

涉及:

- 在类实例上携带状态,  如创建的实例总个数
- 在闭包中携带状态
- 将协程的send方法用作回调函数
- 在回调函数中传入额外的值来携带状态 (使用functools.partial())



例子,  使用回调函数

```python
def apply_async(func, args, *, callback):
    ret = func(*args)
    callback(ret)

def print_ret(ret):
    print('Got: ', ret)

def add(x, y):
    return x + y

if __name__ == '__main__':
    apply_async(add, (2, 3), callback=print_ret)
```

问题:

- 上面的`print_ret函数`仅接受一个单独的参数, 不能传其他信息,  但有时候我们希望回调函数可以同其他变量或部分环境进行交互,  缺乏这类信息就会出现问题

  

1. 使用绑定方法 (bound-method) 作回调

   ```python
   class RetHandler:
       def __init__(self):
           self.seq = 0
   
       def handler(self, ret):
           self.seq += 1
           print('[{}] Got: {}'.format(self.seq, ret))
   
   
   if __name__ == '__main__':
       # apply_async(add, (2, 3), callback=print_ret)
       r = RetHandler()
       apply_async(add, (2, 3), callback=r.handler)  # [1] Got: 5
       apply_async(add, (2, 3), callback=r.handler)  # [2] Got: 5
   ```

2. 使用闭包作回调

   ```python
   def make_handler():
       seq = 0
       def handler(ret):
           nonlocal seq
           seq += 1
           print('[{}] Got: {}'.format(seq, ret))
       return handler
   
   if __name__ == '__main__':
       handler = make_handler()
       apply_async(add, (2, 3), callback=handler)  # [1] Got: 5
       apply_async(add, (2, 3), callback=handler)  # [2] Got: 5
   ```

3. 使用协程的send方法作回调

   ```python
   def make_handler():
       seq = 0
       while True:
           ret = yield
           seq += 1
           print('[{}] Got: {}'.format(seq, ret))
   
   
   if __name__ == '__main__':
       handler = make_handler()
       next(handler)  # Advance to the yield
       apply_async(add, (2, 3), callback=handler.send)  # [1] Got: 5
       apply_async(add, (2, 3), callback=handler.send)  # [2] Got: 5
   
   ```

4. 通过额外参数在回调函数中携带状态

   ```python
   class SeqNo:
       def __init__(self):
           self.seq = 0
   
   def handler(ret, sequence):
       sequence.seq += 1
       print('[{}] Got: {}'.format(sequence.seq, ret))
   
   
   if __name__ == '__main__':
       sequence = SeqNo()
       apply_async(add, (2, 3), callback=partial(handler, sequence=sequence))
       apply_async(add, (2, 3), callback=partial(handler, sequence=sequence))
       # 或用lambda
       apply_async(add, (2, 3), callback=lambda r: handler(r, sequence))
       apply_async(add, (2, 3), callback=lambda r: handler(r, sequence))
       """
       [1] Got: 5
       [2] Got: 5
       [3] Got: 5
       [4] Got: 5
       """
   ```



## 7.11 内联回调函数







# 第8章 类与对象

## 8.1 修改类的字符串表示

定义实例方法:

- `__str__()`:  将实例转为一个字符串,  `str()` 和 `print()` 函数默认默认会调用`__str__()`方法,  其次会调用`__repr__()`
- `__repr__()`:  code representation, 标准做法是返回一个字符串,  可以通过这个字符串来重新创建这个实例,  即 `eval(repr(obj)) == obj`

```python
class Pair:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    # __repr__另一种方式, 使用 %
    def __repr__(self):
        return 'Pair(%r, %r)' % (self.x, self.y)
    
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)


if __name__ == '__main__':
    p = Pair(2, 3)
    print(repr(p))  # Pair(2, 3)
    print(str(p))   # (2, 3)
    print(p)   		# (2, 3)
    # 格式化代码 !r 表示应该使用 __repr__() 输出, 
    # 而不是默认的 __str__()
    print('p: {!r}'.format(p))  # Pair(2, 3)
```



## 8.2 自定义字符串的输出格式

定义实例方法:

- `__format__()`

```python
_formats = dict(
    ymd='{d.year}-{d.month}-{d.day}',
    mdy='{d.month}/{d.day}/{d.year}',
    dmy='{d.day}/{d.month}/{d.year}'
)
_default = 'ymd'

class Date:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        if format_spec is '':
            format_spec = _default
        fmt = _formats[format_spec]
        return fmt.format(d=self)

if __name__ == '__main__':
    d = Date(2020, 1, 28)
    print(format(d))
    print(format(d, 'mdy'))
    print('The date is {:ymd}'.format(d))
```



## 8.3 让对象支持上下文管理协议

上下文管理协议通过 `with语句` 触发, 要让对象兼容 `with语句`, 有两个方法:

### 1.定义 `__enter__()` 和`__exit__()`

第一种:  定义 `__enter__()` 和`__exit__()`

```python
from functools import partial
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:

    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already conneted')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        # __enter__如果有返回值, 会被赋给由 as 限定的变量中.
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()
        self.sock = None

if __name__ == '__main__':
    host = 'www.python.org'
    port = 80
    conn = LazyConnection(address=(host, port))
    with conn as s:
        # conn.__enter__() execute: connection opened
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'HOST: www.python.org\r\n')
        s.send(b'\r\n')
        # iter函数如果传递了第二个参数，则第一个参数source必须是一个可调用的对象,
        # 此时，iter创建了一个迭代器对象，每次调用这个迭代器对象的__next__()方法时，都会调用source。
        resp = b''.join(iter(partial(s.recv, 8192), b''))
        print(resp)
        # conn.__exit__() execute: connection closed

```



上面的代码一次只能创建一个socket链接, 即上面的with语句不支持嵌套.

可稍作修改

```python
from functools import partial
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:

    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        # self.sock = None
        self.conns = list()

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.conns.append(sock)
        return sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conns.pop().close()

if __name__ == '__main__':
    host = 'www.python.org'
    port = 80
    conn = LazyConnection(address=(host, port))
    with conn as s:
        ...
        with conn as s:
            ...
            # s1 and s2 are indepent sockets
```



### 2.使用contextmanager装饰器和yield

第二种:  使用 `@contextlib.contextmanager装饰器` 和 `yield 语句` 

- 所有位于 `yield` 之前的代码  会作为上下文管理器的 `__enter__()` 方法来执行
- 所有位于 `yield` 之后的代码  会作为上下文管理器的 `__exit__()` 方法来执行
- 如果有异常产生, 会在 `yield` 语句中抛出
- `@contextmanager` 只用于编写自给自足型的上下文管理器函数,  如果有一些函数,  比如文件、网络连接或锁， 需要支持在 with 语句中使用，还是要分别实现 `__enter__()` 和 `__exit__()` 

```python
import time
from contextlib import contextmanager

@contextmanager
def time_this(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))

if __name__ == '__main__':
    with time_this('counting'):
        n = 1000000
        while n > 0:
            n -= 1
```



更加高级的上下文管理器

- 实现只有当整个代码块执行结束且没有产生任何异常时,  对列表做出的修改才会生效

```python
from contextlib import contextmanager

@contextmanager
def list_transantion(orig_li):
    working = list(orig_li)
    yield working
    orig_li[:] = working


if __name__ == '__main__':
    items = [1, 2, 3]
    with list_transantion(items) as working:
        working.append(4)
    print('appended 4: {}'.format(working))

    try:
        with list_transantion(items) as working:
            working.append(5)
            raise RuntimeError('oops')
    except RuntimeError:
        print('appended 5, but failed: {}'.format(items))

```



### 3.嵌套上下文管理器

可以用

```
from contextlib import nested

with nested(A(), B(), C()) as (X, Y, Z):
    # with-body code here
```

代替

```
with A() as X:
    with B() as Y:
        with C() as Z:
            # with-body code here
```

避免with嵌套





## 8.4 当创建大量实例时如何节省内存

对于那些主要用作简单数据结构的类,  通常可以定义类属性 `__slots__`,  限制属性名

- `__slots__` 属性可以让每个实例不再创建 `__dict__` 字典,  仅允许创建 `__slots__` 序列中指定的属性名
- 副作用: 无法再对实例添加其他未列出的属性

```python
class Date:

    __slots__ = ['year', 'month', 'day']

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
```





## 8.8 在子类中扩展属性

问题:  需要在子类中扩展某个属性的功能,  而这个属性是在父类中定义好的

```python
class Person:

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string!')
        self.__name = value

    @name.deleter
    def name(self):
        raise AttributeError('Can`t delete attribute!')


class SubPerson(Person):

    # 想扩展属性name的 getter 方法
    @Person.name.getter
    def name(self):
        return super().name

    # 想扩展属性name的 setter 方法
    @Person.name.setter
    def name(self, value):
        # if not isinstance(value, str):
        #     raise TypeError('Expected a string!')
        super(SubPerson, SubPerson).name.__set__(self, value)

if __name__ == '__main__':
    person = SubPerson('Jerry')
    print(person.name)  # Jerry
    person.name = 'John'
    print(person.name)  # John
```

注意:

- 如果只想重新定义property属性其中的一个方法, 只重新定义@property是不够的,  因为property属性其实是被定义为 `getter`、`setter`、`deleter`方法的集合，而不仅仅只是单独的方法。

  ```python
  # Doesn`t work:  setter函数会完全消失
  class SubPerson(Person):
      @property
      def name(self):
          return super().name
  
  # Can work
  class SubPerson(Person):
      @Person.name.getter  # 父类定义过的属性方法会被拷贝过来, getter会被替换.
      def name(self):
          return super().name
  ```

- `@Person.name.getter`对父类名进行了硬编码, 没办法用更一般化的名称来替换,  可以考虑重新定义所有属性方法, 使用super()来调用之前的实现



## 8.9 创建一种新形式的类属性或实例属性

问题:  想创建一种新形式的实例属性,  它可以拥有一些额外的功能,  比如说类型检查

- 以 描述符 类 的形式定义其功能。
- 通过定义描述符,  我们可以在很底层的情况下捕获关键的实例操作,  如get、set、delete，并可以完全自定义这些操作的行为。
- **描述符：**
  - **属性访问的查找顺序**：默认行为是从一个对象的字典中获取、设置或删除属性， 例如，`a.x` 的查找顺序会从 `a.__dict__['x']`开始，然后是 `type(a).__dict__['x']`，接下来依次查找 `type(a)` 的基类，不包括元类。 如果找到的值是**定义了某个描述器方法的对象**，则 Python 可能会重载默认行为并转而发起调用描述器方法。 
  - 如果一个类中包含了三个魔术方法（`__get__()`，`__set__()`，`__delete__()`）之一或者全部的类这个类就是一个描述符。
  - 描述符的作用就是对类/对象中某个成员进行详细的管理操作。 
- 数据描述符（data descriptor）：定义了 `__get__()`，`__set__()` 的描述符
- 非数据描述符（ non-data descriptor ）：仅定义了 `__get__()`的描述符
- 发起调用描述符的方式：
  1. 直接调用描述符方法， 如 `d.__get__(obj)`. 
  2. 属性访问时调用， 如 `obj.d` 默认在`obj.__dict__`字典中查找 `d`,  如果`d`在描述符的`__get__()`方法中定义了, 就会调用 **`d.__get__(obj)`**



例1:

```python
class Descriptor:
    """描述符类."""
    # 初始化一个临时的成员属性（代替原有username的操作）
    def __init__(self):
        self.tmpvar = '匿名用户'  # 属性随便给，这个就是控制的入口

    # 定义描述符的三个成员
    def __get__(self, instance, owner):
        """
        设置当前属性获取的值，
        触发时机：在访问对象成员属性（该成员已经交给描述符管理的时候）的时候触发
        Args:
            instance: Email对象
            owner: Email类
        Returns:
            可有可无，有的话就是获取的值
        """
        # 希望获取用户名的时候仅仅返回第一个和最后一个字符 其余的都隐藏
        result = self.tmpvar[0] + '*' + self.tmpvar[-1]
        return result

    def __set__(self, instance, value):
        """
        对成员的值进行设置管理,
        触发时机：在设置对象成员属性（该成员已经交给描述符管理的时候）的时候触发
        Args:
            instance: Email对象
            value: 要设置的值
        """
        # 设置值的时候一定要设置当前描述符对象的临时变量
        # 限制用户名不能超过8个字符
        # 检测字符个数
        if len(value) > 8:
            self.tmpvar = value[0:8]
        else:
            self.tmpvar = value

    def __delete__(self, instance):
        """
        对成员的值进行删除管理,
        触发时机：在删除对象成员属性（该成员已经交给描述符管理的时候）的时候触发
        Args:
            instance: Email对象
        """
        # 删除临时变量即可
        # 删除值的时候一定要删除当前描述符对象的临时变量
        if instance.allow_del_username is True:
            del self.tmpvar


class Email:
    # 成员属性
    username = Descriptor()  # 用户名 交给描述符管理 [交接行为]
    # 设置一个是否允许删除username的标志
    allow_del_username = True


mail = Email()
# 获取
print(mail.username)
# 设置
mail.username = 'lovemybaby'
print(mail.username)
# 删除
print(mail.username)
del mail.username
print(mail.username)
```



例2:

```python
class Integer:
    """Descripe attribute for an integer type-checked attribute."""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return instance.__dict__[self.name]
        except KeyError:
            raise AttributeError(
                '{} object has no attribute "{}"'.format(owner.__name__, self.name)
            )

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int!')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Point:

    # 要使用一个`描述符`, 必须把描述符的实例定义为类属性
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    p = Point(2, 3)
    print(p.x)  # Point.x__get__(p, Point)
    p.x = 5     # Point.x__set__(p, 5)
    print(p.x)
    # p.x = 2.3  # TypeError: Expected an int!
    del p.x
    print(p.x)
    
    print(Point.x)  # Point.x__get__(None, Point)

```

- 每个描述符都会接受被操纵的实例作为输入
- 要执行所请求的操作,  底层的实例字典 ( 即`__dict__`属性 ) 会根据需要适当地进行调整.
- 描述符的 `self.name` 属性会保存字典的键,  通过这些键可以找到存储在实例字典中的实际数据

注意:

1. 要使用一个描述符,  必须把描述符的实例定义为类属性.
2. `__get__()` 的定义中应该要先判断 instance 是否为None,  因为如果是以类变量的形式访问描述符,  参数instance 应该设置为None. 这种情况下的标准做法是简单返回描述符实例本身.



例3:  

更加高级的基于描述符的代码

```python
class Typed:

    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected {}'.format(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


# class decorator that applies to selected attributes
def type_assert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate


# Example use
@type_assert(name=str, shares=int, prices=float)
class Stock:
    def __init__(self, name, shares, prices):
        self.name = name
        self.shares = shares
        self.prices = prices

```





## 8.10 让属性具有惰性求值的能力

问题:  想将一个只读的属性定义为property属性方法, 只有在访问它时才参与计算,  但是,  一旦访问了该属性,  我们希望把计算出的值缓存起来,  不要每次访问它时都重新计算.  (提升程序性能)

- 定义一个惰性属性最有效的方法就是利用 **描述符** 来完成

```python
import math

# 自定义一个property 类装饰器
class LazyProperty:

    def __init__(self, func):
        # 设置被装饰的方法的引用
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # 执行被装饰的方法, 获取结果
        value = self.func(instance)
        # 设置实例属性, 属性名为方法名, 属性值为原方法执行的结果
        setattr(instance, self.func.__name__, value)
        return value

# Example use
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @LazyProperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @LazyProperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

if __name__ == '__main__':
    circle = Circle(radius=10)
    print(circle.area)  # called: print('Computing area')
    print(circle.area)  # not called: print('Computing area')
    print(circle.perimeter)
    print(circle.perimeter)

```

注意:

- 前面的 area 在第一次计算之后就成为可变的. (mutable)

  ```python
  circle.area = None
  print(circle.area)  # None
  ```

- 如果需要考虑可变性问题,  可以使用另外一种方式实现,  但执行效率稍微降低



定义不可变惰性属性 (不可 set)

```python
# 定义一个装饰器函数
def lazy_property(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        value = func(self)
        setattr(self, name, value)
        return value

    return lazy

# Example use
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazy_property
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

if __name__ == '__main__':
    circle = Circle(radius=10)
    print(circle.area)  # called: print('Computing area')
    print(circle.area)  # not called: print('Computing area')
    circle.area = 100   # AttributeError: can't set attribute
```

缺点:

- 这种方式会让所有 get 操作都必须经由属性的 getter 函数来处理,  比直接在实例字典中查找值慢一些.



### 将方法转为惰性属性的源码例子

> flask helpers.py

```python
class locked_cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value.  Works like the one in Werkzeug but has a lock for
    thread safety.
    """

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func
        self.lock = RLock()

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        with self.lock:
            value = obj.__dict__.get(self.__name__, _missing)
            if value is _missing:
                value = self.func(obj)
                obj.__dict__[self.__name__] = value
            return value
```





## 8.11 简化数据结构的初始化过程

问题:  我们编写了许多类,  把它们当作数据结构来用,  但是不想编写高度重复且样式相同的 `__init__()`函数

- 可以将初始化数据结构的步骤归纳到一个单独的`__init__()` 函数中, 定义在一个公共的基类中
  1. 只考虑`*args`
  2. 考虑`*args` 和 `**kwargs`
  3. 考虑`*args` 和 `**kwargs`,  限制`kwargs`不能传额外参数

```python
import math

class Structure:
    _fields = list()
	# 只考虑*args
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        # 考虑另一种设置属性的方式: 更新self.__dict__
        # self.__dict__.update(zip(self._fields, args))
        # 缺点: 不安全. 如果某个子类决定使用__slots__或property或描述符, 包装了某个特定的属性,
        # 直接访问实例字典就会崩溃

class Point(Structure):
    _fields = ['x', 'y']

class Circle(Structure):
    _fields = ['radius']

    def area(self):
        return math.pi * self.radius ** 2

if __name__ == '__main__':
    p = Point(1, 2)
    c = Circle(10)
    print(c.area())
```

缺点:

- 影响`IDE`的文档和帮助功能,  缺少参数信息: 如help(Point)

- 解决:

  - 可以通过在`__init__()`中强制施行 **类型签名** 来解决

    ```
    参阅 9.16
    ```

  - 也可以采用 **frame hack** 技巧来实现自动化的实例变量初始化处理,  只要编写一个功能函数

    ```python
    def init_from_locals(self):
        locs = sys._getframe(1).f_locals
        for k, v in locs.items():
            if k != 'self':
                setattr(self, k, v)
    
    # Example use
    class Point:
        def __init__(self, x, y):
            init_from_locals(self)
    
    class Circle:
        def __init__(self, radius):
            init_from_locals(self)
    
        def area(self):
            return math.pi * self.radius ** 2
    ```



## 8.12 定义一个接口或抽象基类

问题:  想定义一个类作为接口或是抽象基类,  这样可以在此基础上执行类型检查并确保在子类中实现特定的方法

- 使用 **abc** 模块:  `ABCMeta`、`@abstractmethod`
- 抽象基类的核心特征就是不能被直接实例化
- 抽象基类是给其他类做基类使用的,  子类需要实现基类中要求的那些方法

```python
from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass


class SocketStream(IStream):

    def read(self, maxbytes=-1):
        ...

    def write(self, data):
        ...
```

注意:

- `@abstractmethod` 装饰器也可以用到 **静态方法**、**类方法**、**property属性** 上，`@abstractmethod` 要紧挨着函数定义
- 标准库中已经定义好了一些抽象基类， 可以用这些抽象基类来执行更加一般化的类型检查
  - **collections** 模块中定义了多个与这些相关的抽象基类：容器、迭代器（序列、映射、集合等）
  - **numbers** 模块中定义了和数值对象相关的抽象基类
  - **io** 库中定义了和 I/O 处理相关的抽象基类





## 8.13 实现一种数据模型或类型系统

问题:  我们想定义各种数据结构, 但对于某些特定属性, 我们想对允许赋给它们的值做一些限制

### 1.使用描述符定制属性

- 使用描述符定制属性的总体设计基于 mixin 类 (多继承)

```python
"""-----------定义描述符基类-----------"""
# base class, uses a descriptor to set a value
class Descriptor:

    def __init__(self, name=None, **opts):
        self.name = name
        for k, v in opts.items():
            setattr(self, k, v)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


"""-----------定义基础组件-----------"""
# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected {}'.format(self.expected_type))
        super().__set__(instance, value)


# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)


# Descriptor for enforcing values
class MaxSized(Descriptor):

    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('Missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) > self.size:
            raise ValueError('Size must be <= {}'.format(self.size))
        super().__set__(instance, value)


"""-----------定义不同数据类型-----------"""
class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class UnsignedInteger(Integer, Unsigned):
    pass

class UnsignedFloat(Float, Unsigned):
    pass

class SizedString(String, MaxSized):
    pass


"""-----------使用数据类型-----------"""
class Stock:

    # 初始化描述符对象, 将指定属性交给描述符管理
    stck_name = SizedString(name='stck_name', size=8)
    shares = UnsignedInteger(name='shares')
    prices = UnsignedFloat(name='prices')

    def __init__(self, stck_name, shares, prices):
        self.stck_name = stck_name
        self.shares = shares
        self.prices = prices


if __name__ == '__main__':
    s = Stock(stck_name='stock1', shares=10, prices=2.5)
    print(s.stck_name)
    s.shares = -10  # ValueError: Expected >= 0
```



简化在类中设定约束的步骤

- 使用装饰器或元类常常可以简化用户代码
- 实现装饰器或元类的代码会扫描类字典,  寻找描述符类或对象,  然后自动填入描述符的名称

1. 使用类装饰器

   ```python
   def check_attrs(**kwargs):
       def decorate(cls):
           for key, value in kwargs.items():
               if isinstance(value, Descriptor):
                   # 传入的是描述符对象
                   value.name = key
                   setattr(cls, key, value)
               else:
                   # 传入的是描述符类
                   setattr(cls, key, value(key))
           return cls
       return decorate
   
   # Use
   @check_attrs(
       stck_name=SizedString(size=8),
       shares=UnsignedInteger,
       prices=UnsignedFloat
   )
   class Stock:
       def __init__(self, stck_name, shares, prices):
           self.stck_name = stck_name
           self.shares = shares
           self.prices = prices
           
   if __name__ == '__main__':
       s = Stock(stck_name='stock1', shares=10, prices=2.5)
       print(s.stck_name)
       s.shares = -10  # ValueError: Expected >= 0
   ```

2. 使用元类

   ```python
   class CheckedMeta(type):
       def __new__(cls, clsname, bases, methods):
           for key, value in methods.items():
               if isinstance(value, Descriptor):
                   # 属性是描述符对象
                   value.name = key
           return type.__new__(cls, clsname, bases, methods)
   
   class Stock(metaclass=CheckedMeta):
       stck_name = SizedString(size=8)
       shares = UnsignedInteger()
       prices = UnsignedFloat()
   
       def __init__(self, stck_name, shares, prices):
           self.stck_name = stck_name
           self.shares = shares
           self.prices = prices
   
   if __name__ == '__main__':
       s = Stock(stck_name='stock1', shares=10, prices=2.5)
       print(s.stck_name)
       s.shares = -10  # ValueError: Expected >= 0
   ```





### 2.使用类装饰器定制属性

- 使用类装饰器定制属性可以取代 mixin 类、多继承以及对super()函数的使用
- 使用类装饰器定制属性的方案运行速度比采用 mixin类 的方案几乎快100%

```python
# base class, uses a descriptor to set a value
# Descriptor同前面的定义一致
class Descriptor:

    def __init__(self, name=None, **opts):
        self.name = name
        for k, v in opts.items():
            setattr(self, k, v)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# 定义数据类型检查装饰器函数
def typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: typed(expected_type, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('Expected {}'.format(expected_type))
        super_set(self, instance, value)

    cls.__set__  = __set__
    return cls

# 定义数值有无符号检查装饰器函数
def unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls

# 定义最大值检查装饰器函数
def max_sized(cls):
    super_init = cls.__init__

    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super_init(self, name, **opts)

    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) > self.size:
            raise ValueError('size must be <= {}'.format(self.size))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# 定义整型类型描述符类
@typed(int)
class Integer(Descriptor):
    pass

@typed(float)
class Float(Descriptor):
    pass

@typed(str)
class String(Descriptor):
    pass

@unsigned
class UnsignedInteger(Integer):
    pass

@unsigned
class UnsignedFloat(Float):
    pass

@max_sized
class SizedString(String):
    pass


class CheckedMeta(type):
    def __new__(cls, clsname, bases, methods):
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                # 属性是描述符对象
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

class Stock(metaclass=CheckedMeta):
    stck_name = SizedString(size=8)
    shares = UnsignedInteger()
    prices = UnsignedFloat()

    def __init__(self, stck_name, shares, prices):
        self.stck_name = stck_name
        self.shares = shares
        self.prices = prices


if __name__ == '__main__':
    s = Stock(stck_name='stock1', shares=10, prices=2.5)
    print(s.stck_name)
    s.stck_name = "1234566789"  # ValueError: size must be <= 8
```





## 8.14 实现自定义容器

问题:  我们想实现一个自定义类,  用来模仿普通内建容器的行为,  如列表、字典， 但是我们不完全确定需要实现哪些方法来完成

- 使用 collections 模块中的各种抽象基类
  - collections.Iterable
  - collections.Sequence
  - collections.MutableSequence
  - collections.Mapping
  - collections.MutableMapping
  - collections.Set
  - collections.MutableSet



查看需要实现哪些方法

```python
>>> import collections
>>> collections.Sequence()
"""
TypeError: Can't instantiate abstract class Sequence with abstract methods __getitem__, __len__
"""
```



例1

创建一个Sequence,  元素总是以排序后的顺序存储

```python
import bisect
from collections import Sequence


class SortedItems(Sequence):

    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is not None else []

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def add(self, item):
        bisect.insort(self._items, item)


if __name__ == '__main__':
    items = SortedItems([3, 4, 1])
    print(list(items))
    items.add(2)
    print(list(items))
```





## 8.15 委托属性访问

问题:  我们想在访问实例的属性时能够将其委托 (delegate) 到一个内部持有的对象上,  这可以: **作为继承的替代方案**或是为了 **实现一种代理机制**

最简单地委托形式

```python
class A:
    def spam(self, x):
        pass

class B:
    def __init__(self):
        self._a = A()
    def spam(self, x):
        return self._a.spam(x)
    def bar(self):
        pass
```

使用`__getattr__()`

- `__getattr__()`:  如果代码中尝试访问一个不存在的属性, 就会调用`__getattr__()`

```python
class B:
    def __init__(self):
        self._a = A()
    def bar(self):
        pass
    def __getattr__(self, name):
        return getattr(self._a, name)
```



**实现代理**

```python
class Proxy:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name: str):
        return getattr(self._obj, name)

    def __setattr__(self, name: str, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)

    def __delattr__(self, name: str):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            delattr(self._obj, name)


# Example use
class Spam:

    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('Spam.bar: ', self.x, y)
```

当使用委托实现代理时，**需要注意**：

1. `__getattr__()`方法实际上是一个回滚方法,  只会在某个属性/方法没有找到时才会调用.  **访问代理实例本身的属性/方法不会调用 `__getattr__()`**

2. `__setattr__()` 和 `__delattr__()` 方法需要添加一点额外逻辑来区分代理实例本身属性和内部对象 `_obj` 上的属性.   常用惯例是代理类只委托那些不以下划线开头的属性/方法:   **代理类只暴露内部对象中的"公有"属性/方法**

3. `__getattr__()`方法通常不适用于大部分名称以双下划线开头和结尾的特殊方法

   ```python
   class ListLike:
       def __init__(self):
           self._items = []
       def __getattr__(self, name):
           return getattr(self._items, name)
   
   if __name__ == '__main__':
       li = ListLike()
       len(li)    # TypeError: object of type 'ListLike' has no len()
   ```





委托有时可以作为继承的替代方案

- 什么时候考虑委托?
  - 想更多地控制对象之间的关系时使用委托很有用,  如只暴露特定方法、实现接口等

```python
class A:
    def spam(self, x):
        pass

# 继承
class B(A):
    def spam(self, x):
        super().spam(x)

# 委托
class B:
    def __init__(self):
        self._a = A()
    def __getattr__(self, name):
        return getattr(self._a, name)
```





## 8.16 在类中定义多个构造函数

问题:  我们在编写一个类,  但是想让用户能够以多种方式创建实例,  而不局限于 `__init__()`这一种

- 使用类方法

```python
import time

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):  # 使用类方法创建实例
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

    def __str__(self):
        return '{0.year}-{0.month}-{0.day}'.format(self)

if __name__ == '__main__':
    d1 = Date(2020, 1, 29)
    d2 = Date.today()
    print(d1)
    print(d2)
```

难以理解和不好维护的代码:

```python
class Date:
    def __init__(self, *args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
        self.year, self.month, self.day = args

d2 = Date()  # 作用不清晰
```





## 8.17 不通过调用 init 来创建实例

问题:  需要创建一个实例,  但是出于某种原因想绕过 `__init__()` 方法,  用别的方式创建

- 直接调用类的 `__new__()` 方法创建一个未初始化的实例

使用场景:

1. 反序列化数据
2. 或实现一个类方法,  将其作为备选的构造函数

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    # 备选的构造函数, 绕过init
    @classmethod
    def today(cls):
        d = cls.__new__(cls)  # 创建一个未初始化的实例
        t = time.localtime()
        d.year = t.tm_year    # 为实例添加属性
        d.month = t.tm_mon
        d.day = t.tm_mday
        return d

if __name__ == '__main__':
    d = Date.__new__(Date)
    # print(d.year)  # AttributeError: 'Date' object has no attribute 'year'

    data = {'year': 2020, 'month': 1, 'day': 29}
    for name, value in data.items():
        setattr(d, name, value)
    print(d.year)   # 2020
```



## 8.18 用 Mixin 技术来扩展类定义

问题:  我们有一些十分有用的方法,  希望用它们来扩展其他类的功能.  但是,  需要添加方法的这些类之间并不一定属于继承关系,  因此没法将这些方法直接关联到一个共同的基类上

使用场景：某个库提供了一组基础类以及一些可选的定制化方法，如果用户需要可自定添加

### 1.多重继承实现Mixin

```python
import collections

# 定义多个Mixin类
class LogedMappingMixin:
    """Add logging to get/set/delete operations for debugging."""
    __slots__ = ()
    def __getitem__(self, key):
        print('Getting {}'.format(key))
        return super().__getitem__(key)
    def __setitem__(self, key, value):
        print('Setting {}'.format(key))
        return super().__setitem__(key, value)
    def __delitem__(self, key):
        print('Deleting {}'.format(key))
        return super().__delitem__(key)

class SetOnceMappingMixin:
    """Only allow a key to be set once."""
    __slots__ = ()
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError('{} already set'.format(key))
        return super().__setitem__(key, value)

class StringKeysMappingMixin:
    """Restrict keys to strings only."""
    __slots__ = ()
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)


# 使用Mixin类进行多重继承
class LogedDict(LogedMappingMixin, dict):
    pass

class SetOnceDefaultDict(SetOnceMappingMixin, collections.defaultdict):
    pass

class StringOrderedDict(StringKeysMappingMixin,
                        SetOnceMappingMixin,
                        collections.OrderedDict):
    pass


if __name__ == '__main__':
    d = LogedDict()
    d['x'] = 23  # Setting x
    d['x']       # Getting x
    del d['x']   # Deleting x

    d = SetOnceDefaultDict(list)
    d['x'].append(2)
    print(d['x'])  # [2]
    # d['x'] = 3   # KeyError: 'x already set'

    d = StringOrderedDict()
    # d[42] = 100  # TypeError: keys must be strings
```

注意：

- 上面 Mixin 类中的 `super().__setitem__(key, value)` 、`if key in self:` 等代码要求子类在继承Mixin类时需要同时继承支持`__setitem__()`等方法的类

- 使用 super() 也是编写Mixin类的关键部分,  通过 super() 将方法的调用交给 MRO 的下一个类.

- Mixin类不是为了直接实例化而创建的，要和其他类通过 **多重继承** 的方式混合使用。

- Mixin类对已有的类增加一些可选的功能特性

- Mixin类一般没有状态:

  - 一般没有`__init__()`,  因为不知道会和哪些类混用

  - > 如果Mixin类需要定义`__init__()`:
    >
    > 1. 必须实现非常通用的参数签名,  需要使用*args, **kwargs
    > 2. 如果Mixin类的init方法本身还带参数,  参数要通过关键字来指定,  且要避免命名冲突
    >
    > 一种可能的实现方法:
    >
    > ```python
    > class RestrictKeysMixin:
    >     def __init__(self, *args, _restrict_key_type, **kwargs):
    >         # `命名关键字参数`: _restrict_key_type
    >         self._restrict_key_type = _restrict_key_type
    >         super().__init__(*args, **kwargs)
    > 
    >     def __setitem__(self, key, value):
    >         if not isinstance(key, self._restrict_key_type):
    >             raise TypeError('Keys must be {}'.format(self._restrict_key_type))
    >         super().__setitem__(key, value)
    > 
    > class RDict(RestrictKeysMixin, dict):
    >     pass
    > 
    > if __name__ == '__main__':
    >     d = RDict(_restrict_key_type=int)
    >     e = RDict([('name', 'Dave'), ('age', 26)], _restrict_key_type=str)
    >     f = RDict(name='Dave', age=26, _restrict_key_type=str)
    >     f[10] = 10  # TypeError: Keys must be <class 'str'>
    > ```

  - 没有实例变量

  - 定义`__slots__类属性` 表示Mixin类没有属于自己的实例数据

  

如写网络功能方面的代码， 通常可以使用 socketserver 模块的 ThreadingMixin 类添加对线程的支持

```python
# 多线程版的 XML-RPC 服务
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass
```





### 2.类装饰器实现Mixin

```python
def logged_mapping(cls):
    cls_getitem = cls.__getitem__
    cls_setitem = cls.__setitem__
    cls_delitem = cls.__delitem__

    def __getitem__(self, key):
        print('Getting ', key)
        return cls_getitem(self, key)

    def __setitem__(self, key, value):
        print('Setting ', key)
        return cls_setitem(self, key, value)

    def __delitem__(self, key):
        print('Deleting ', key)
        return cls_delitem(self, key)

    cls.__getitem__ = __getitem__
    cls.__setitem__ = __setitem__
    cls.__delitem__ = __delitem__
    return cls

# Example use
@logged_mapping
class LoggedDict(dict):
    pass

if __name__ == '__main__':
    d = LoggedDict()
    d['x'] = 10  # Setting  x
```

- 8.13中有一个更高级的示例, 同时用到了mixin技术和类装饰器





## 8.19 实现带有状态的对象或状态机

问题:  我们想实现一个状态机,  或者让对象可以在不同的状态中进行操作,  但不希望代码里会因此出现大量的条件判断

不优雅的实现方式:

```python
closed = 'CLOSED'
opened = 'OPENED'

class Connection:
    def __init__(self):
        self.state = closed

    def open(self):
        if self.state == opened:
            raise RuntimeError('Alraedy opened')
        self.state = opened

    def read(self):
        if self.state != opened:
            raise RuntimeError('Not open')
        print('reading')

    def write(self):
        if self.state != opened:
            raise RuntimeError('Not open')
        print('writing')

    def close(self):
        if self.state == closed:
            raise RuntimeError('Alraedy closed')
        self.state = closed
```



### <1> 继承 + 代理

- 为每种操作状态单独定义一个类,  然后在 对外接口类Connection中使用这些状态类

```python
# 状态公共父类
class ConnectionState:
    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()


# opened状态子类
class Opened(ConnectionState):
    @staticmethod
    def open(conn):
        raise RuntimeError('Already opened')

    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn):
        print('writing')

    @staticmethod
    def close(conn):
        conn.new_state(Closed)


# closed状态子类
class Closed(ConnectionState):
    @staticmethod
    def open(conn):
        conn.new_state(Opened)

    @staticmethod
    def read(conn):
        raise RuntimeError('Not opened')

    @staticmethod
    def write(conn):
        raise RuntimeError('Not opened')

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')


# 对外接口类
class Connection:
    def __init__(self):
        self._state = None
        self.new_state(Closed)

    def new_state(self, new_state):
        self._state = new_state

    def open(self):
        return self._state.open(self)

    def read(self):
        return self._state.read(self)

    def write(self):
        return self._state.write(self)

    def close(self):
        return self._state.close(self)


if __name__ == '__main__':
    conn = Connection()
    conn.open()
    conn.read()
```





### <2> 直接修改实例的`__class__`属性

```python
# 定义一个对外接口父类
class Connection:
    def __init__(self):
        self.new_state(Closed)

    def new_state(self, new_state_cls):
        # 直接修改实例的__class__属性
        self.__class__ = new_state_cls

    def open(self):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def write(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


# 定义open状态子类
class Opened(Connection):
    def open(self):
        raise RuntimeError('Already opened')

    def read(self):
        print('reading')

    def write(self):
        print('writing')

    def close(self):
        self.new_state(Closed)


# 定义close状态子类
class Closed(Connection):
    def open(self):
        self.new_state(Opened)

    def read(self):
        raise RuntimeError('Not open')

    def write(self):
        raise RuntimeError('Not open')

    def close(self):
        raise RuntimeError('Already closed')


if __name__ == '__main__':
    conn = Connection()
    conn.read()
```

注:

- 将前面的ConnectionState和Connection合为一个实现,  消除了额外的间接关系,  代码运行速度更快

- Connection作为父类和对外接口

- 随着状态的改变, 实例也会修改自己的类型

  ```python
  >>> conn = Connection()
  >>> conn
  <__main__.Closed at 0x15c75726c88>
  >>> conn.open()
  >>> conn
  <__main__.Opened at 0x15c75726c88>
  ```







## 8.20 调用对象上的方法, 方法名用字符串给出

问题:  方法名保存成了字符串,  如何调用该方法?

调用一个方法实际上有两步:  1. 查询属性,  2.  函数调用

- 简单情况用 `getattr()`,   查询属性
- 另一种方式:  `operator.methodcaller()`, 传入方法名字符串和参数,  返回可调用对象,  然后在调用这个对象时传入恰当的 self

```python
import math
import operator

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self): return 'Point({!r:}, {!r:})'.format(self.x, self.y)
    def distance(self, x, y): return math.hypot(self.x - x, self.y - y)

if __name__ == '__main__':
    point = Point(2, 3)
    # 1
    d = getattr(point, 'distance')(0, 0)
    # 2
    d = operator.methodcaller('distance', 0, 0)(point)
```

`operator.methodcaller` 适用于:  通过名称来查询方法并提供同样的参数反复调用该方法

例如,  想对一整列点对象进行排序:

```python
# 有多个对象
points = [
    Point(1, 2),
    Point(3, 0),
    Point(10, -3),
    Point(-5, -7),
    Point(-1, 8),
    Point(3, 2),
]
# 先确定方法名字符串和调用时传的参数
# 然后传入原对象
points.sort(key=operator.methodcaller('distance', 0, 0))
```





## **8.21 实现访问者模式



## **8.22 实现非递归的访问者模式



## **8.23 在环状数据结构中管理内存







## 8.24 让类支持比较操作

问题:  想在类实例之间使用比较运算符,  但不想编写大量的特殊方法:

- **>** : `__gt__()`
- **>=** : `__ge__()`
- **==** : `__eq__()`
- **<** : `__lt__()`
- **<=** : `__le__()`

如果要实现所有比较操作,  实现这么多特殊方法可能代码比较繁琐

使用装饰器简化这个过程:

- `@functools.total_ordering`

- 注意还是需要手动定义至少一个魔法方法: **must define at least one ordering operation: < > <= >=**

  - > 这一点可以从源码看出:
    >
    > ```
    > _convert = {
    >     '__lt__': [('__gt__', _gt_from_lt),  # <
    >                ('__le__', _le_from_lt),
    >                ('__ge__', _ge_from_lt)],
    >     '__le__': [('__ge__', _ge_from_le),  # <=
    >                ('__lt__', _lt_from_le),
    >                ('__gt__', _gt_from_le)],
    >     '__gt__': [('__lt__', _lt_from_gt),  # >
    >                ('__ge__', _ge_from_gt),
    >                ('__le__', _le_from_gt)],
    >     '__ge__': [('__le__', _le_from_ge),  # >=
    >                ('__gt__', _gt_from_ge),
    >                ('__lt__', _lt_from_ge)]
    > }
    > ```

```python
import functools
from typing import List, Union

class Room:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@functools.total_ordering   # 改装饰器可以简化比较操作的魔法方法的定义
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room: Union[Room, List[Room]]):
        if isinstance(room, Room):
            self.rooms.append(room)
        elif isinstance(room, list):
            self.rooms.extend(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(
            self.name,
            self.living_space_footage,
            self.style
        )

    # def __eq__(self, other):
    #     return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):  # 定义任意一个即可: < > <= >=
        return self.living_space_footage < other.living_space_footage


if __name__ == '__main__':
    r1 = Room('室1', length=4, width=4)
    r2 = Room('厅1', length=8, width=6)
    r3 = Room('厨1', length=2, width=3)
    r4 = Room('卫1', length=3, width=2)

    h1 = House('户型一', '三室一厅一厨两卫')
    h1.add_room([r1, r1, r1, r2, r3, r4, r4])
    print("h1 living_space_footage: ", h1.living_space_footage)

    h2 = House('户型二', '二室一厅一厨一卫')
    h2.add_room([r1, r1, r2, r3, r4])
    print("h2 living_space_footage: ", h2.living_space_footage)

    print(h1 > h2)   # True
    print(h1 == h2)  # False
```



## 8.25 创建缓存实例

问题:  当创建类实例时我们想返回缓存引用,  让其指向上一个用同样参数 (如果有的话) 创建出的类实例

logger例子:

```python
>>> import logging
>>> a = logging.getLogger('foo')
>>> b = logging.getLogger('bar')
>>> a is b
False
>>> c = logging.getLogger('foo')
>>> a is c
True
```



方法1:  定义一个与类本身分离的工厂函数

```python
import weakref

class Spam:
    def __init__(self, name):
        self.name = name

# Caching support
_cached = weakref.WeakValueDictionary()

def get_spam(name):
    if name not in _cached:
        s = Spam(name)
        _cached[name] = s
    else:
        s = _cached[name]
    return s

if __name__ == '__main__':
    s1 = get_spam("foo")
    s2 = get_spam("foo")
    print(s1 is s2)  # True
```

- 弱引用`weakref.WeakValueDictionary()` 保存被引用的对象, 但当实例不再被强引用时,  字典的key就会消失.  

  ```python
  >>> s1 = get_spam("foo")
  >>> s2 = get_spam("foo")
  >>> list(_cached)
  ['foo']
  >>> del s1
  >>> list(_cached)
  ['foo']
  >>> del s2
  >>> list(_cached)
  []
  ```



方法2: 更优雅的实现方式---重新定义`__new__()`

```python
import weakref

class Spam:
    _cached = weakref.WeakValueDictionary()
    def __new__(cls, name):
        if name in cls._cached:
            return cls._cached[name]
        self = super().__new__(cls)
        cls._cached[name] = self
        return self

    def __init__(self, name):
        # 缺陷: 无论对象实例有无得到缓存, 每次实例化时init方法总是会被调用
        print("Initializing Spam")
        self.name = name

if __name__ == '__main__':
    s1 = Spam("foo")  # Initializing Spam
    s2 = Spam("foo")  # Initializing Spam
```



解决缓存后仍重复初始化问题的一种考虑:

```python
import weakref

class _Spam:
    def __init__(self, *args, **kwargs):
        raise RuntimeError('Can`t instantiate directly!')

    @classmethod
    def _new(cls, name):  # 跳过__init__
        self = cls.__new__(cls)
        self.name = name
        return self

class CachedSpamManager:
    def __init__(self):
        self._cached = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cached:
            s = _Spam._new(name)
            self._cached[name] = s
        else:
            s = self._cached[name]
        return s

if __name__ == '__main__':
    manager = CachedSpamManager()
    s1 = manager.get_spam('foo')
    s2 = manager.get_spam('foo')
    print(s1 is s2)
```







# 第9章 元编程

元编程:

- 不要重复自己的工作

- 任何时候当需要创建高度重复的代码时,  通常都需要寻找一个更加优雅的解决方案,  在Python中,  这类问题归类为"元编程"
- 元编程的主要目标是创建函数和类,  并用它们来操纵代码 (修改、生成或包装已有代码)

相关特性:

- 装饰器
- 类装饰器
- 元类
- 对象签名
- ...





## 9.1 编写装饰器时如何保存函数的元数据

函数元数据:

- 函数名
- 文档字符串
- 函数注解
- 调用签名

装饰器保存函数的元数据:

- 为装饰器内层的函数添加一个装饰器:  **@functools.wraps(func)**
  1. 将被装饰函数func的元数据复制给 内层函数wrapper
  2. 给内层函数wrapper增加一个 `__wrapped__`属性指向被装饰的原函数



```python
import functools
import time


def time_this(func):

    @functools.wraps(func)  # 作用: 将func的元数据复制给 wrapper
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print("{} use time: {}".format(func.__name__, end - start))
        return ret

    print("wrapper.__name__:", wrapper.__name__)
    print("wrapper.__doc__:", wrapper.__doc__)
    print("wrapper.__annotations__:", wrapper.__annotations__)
    print("wrapper.__wrapped__:", wrapper.__wrapped__)
    return wrapper


# Example use
@time_this
def countdown(n :int):  # func.__name__, func.__annotations__
    """Counts down."""  # func.__doc__
    while n > 0:
        n -=1


if __name__ == '__main__':
    countdown(100000)
    """
    wrapper.__name__: countdown
    wrapper.__doc__: Counts down.
    wrapper.__annotations__: {'n': <class 'int'>}
    wrapper.__wrapped__: <function countdown at 0x0000018E42405378>
    countdown use time: 0.013507604598999023
    """
```





## 9.2 对装饰器进行解包装

问题:  我们已经把装饰器添加到一个函数上了,  但是想访问未经包装的原函数

- 使用了 `@functools.wraps(func)` 装饰内函数
- 访问 `__wrapped__` 属性获取原函数的引用

```python
@time_this
def countdown(n :int):
    """Counts down."""
    while n > 0:
        n -=1

if __name__ == '__main__':
    countdown.__wrapped__(100000)
```



## 9.4 定义一个可接受参数的装饰器

```python
import logging
from functools import wraps


def logged(level, name=None, message=None):

    def decorate(func):
        log_name = name or func.__module__
        log = logging.getLogger(log_name)
        log_msg = message or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, log_msg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


@logged(level=logging.ERROR, message='error')
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, message='critical')
def spam():
    print('Spam!')


if __name__ == '__main__':
    add(1, 2)
    spam()
```

带参数装饰器 装饰的过程

```python
add = logged(level=logging.ERROR, message='error')(add)
```



## 9.5 定义一个属性可由用户修改的装饰器

问题:  想编写一个装饰器来装饰函数,  但是可以需要可以调整装饰器的属性,  这样在运行时能控制装饰器的行为

- 引入访问器函数 (accessor  function),  通过 nonlocal 关键字声明变量来修改装饰器内部的属性
- 使用访问器函数可以解决多装饰器顺序问题,  详见原书的讨论

```python
import logging
import time
from functools import partial, wraps


# 定义一个访问器函数 (accessor function)
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):

    def decorate(func):
        log_name = name or func.__module__
        log = logging.getLogger(log_name)
        log_msg = message or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, 'level: {}, msg: {}'.format(level, log_msg))
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(new_level):
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)
        def set_msg(new_msg):
            nonlocal log_msg
            log_msg = new_msg

        return wrapper

    return decorate


@logged(logging.CRITICAL, "example")
def spam():
    print('Spam!')


if __name__ == '__main__':
    spam()   # level: 50, msg: spam
    spam.set_level(logging.ERROR)
    spam.set_msg('new spam')
    time.sleep(2)
    spam()   # level: 40, msg: new spam
```







## 9.6 定义一个能接收可选参数的装饰器

问题:  想编写一个单独的装饰器,  使其既可以像`@decorator` 这牙膏不带参数使用,  也可以像 `@decorator(x,y,z)` 这样接收可选参数

- 装饰器外函数使用默认参数 + functools.partial()

```python
import logging
from functools import partial, wraps


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    # 增加func=None判断, 使装饰器支持 @logged() 这种不传参数的用法, 效果等同于 @logged
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    log_name = name or func.__module__
    log_msg = message or func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log = logging.log(level, log_msg)
        return func(*args, **kwargs)

    return wrapper


@logged
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')


if __name__ == '__main__':
    add(1, 2)
    spam()
```





## 9.7 利用装饰器对函数参数强制执行类型检查

先看实现:

```python
import functools
import inspect


def type_assert(*ty_args, **ty_kwargs):

    def decorate(func):
        # if in optimized mode, disable type checking
        # if not __debug__:
        #     return func

        # map function argument names to supplied types
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs)
        bound_types = bound_types.arguments  
        # OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)])

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                ty = bound_types.get(name)
                if ty and not isinstance(value, ty):
                    raise TypeError('Argument {} must be {}'.format(name, ty))
            return func(*args, **kwargs)

        return wrapper

    return decorate


@type_assert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)


if __name__ == '__main__':
    spam(1, 2, 3)
    spam(1, 2, 'to_z')  # TypeError: Argument z must be <class 'int'>
```

分析:

- 这个装饰器非常灵活:

  - 允许指定函数参数的所有类型,  也可以仅指定一部分参数的类型
  - 参数类型可以通过位置参数来指定,  也可以通过关键字参数来指定

- 关键:  对被包装函数的参数签名做检查

  - 这里使用 `inspect.signature()` 函数,  从一个可调用对象中提取参数签名信息

  - 使用签名的 `bind_partial()` 方法来对提供的类型到参数名做部分绑定

    ```python
    sig = inspect.signature(func)
    bound_types = sig.bind_partial(int, z=int)
    bound_types = bound_types.arguments
    print(bound_types)
    """
    OrderedDict([('x', <class 'int'>), ('z', <class 'int'>)])
    """
    ```

  - 在由装饰器构建的包装函数中用到了 `sig.bind()`  方法,  如同 `bind_partial()` 方法,  只是  `sig.bind()`  不允许出现缺失的参数

    ```python
    bound_values = sig.bind(1, 2, 3)  # 调用spam()时传了 1,2,3
    print(bound_values.arguments)
    """
    OrderedDict([('x', 1), ('y', 2), ('z', 3)])
    """
    ```

  - 对于具有默认值的参数,  如果调用函数时没有传对应参数,  则断言机制不会作用在其默认值上

  - 为什么不把装饰器实现为检查函数注解?

    1. 函数的每个参数只能赋予一个单独的注解,  因此,  如果把注解用于类型断言,  则它们就不能用在别处
    2. 通过使用装饰器参数,  使装饰器变得更加通用, 可用于任何函数,  即使是使用了注解的函数







## 9.8 在类中定义装饰器



## 9.9 把装饰器定义成类









# 第10章 模块和包



# 第12章 并发