

目录

# abc

abstract base class,  抽象基类

# base64





# bisect 排序

 使用这个模块的函数前先确保操作的列表是已排序的 

```python
import bisect

items = [3, 2, 5]
# 先确保操作的列表是已排序的
items.sort()

# 插入一个数据
bisect.insort(items, item)   # 插入的结果是不会影响原有的排序。

# 查找某数值将会插入的位置并返回，而不会插入
bisect.bisect(items, item)

# 处理将会插入重复数值的情况，返回将会插入的位置
# 对应的插入函数是 insort_left  和 insort_right 
bisect.bisect_left()
bisect.bisect_right()

```







# calendar

calendar 是与日历相关的模块，calendar模块文件里定义了很多类型，主要有 Calendar，TextCalendar以及HTMLCalendar 类型 

calender 还提供了一些函数,  如:

```python
isleap(year)
leapdays(y1, y2)
weekday(year, month, day)
monthrange(year, month)
```



# collections

collections是Python内建的一个集合模块，提供了许多有用的集合类。

## namedtuple

`tuple`可以表示不变集合，例如，一个点的二维坐标就可以表示成：

```python
>>> p = (1, 2)
```

但是，看到`(1, 2)`，很难看出这个`tuple`是用来表示一个坐标的。

定义一个class又小题大做了，这时，`namedtuple` 命名元组就派上了用场：

```python
>>> from collections import namedtuple
>>> Nt = namedtuple('Point', ['x', 'y'])
>>> nt = Nt(1, 2)
>>> nt.x
1
>>> nt.y
2
```

`namedtuple`是一个函数，它用来创建一个自定义的`tuple`对象，并且规定了`tuple`元素的个数，并可以用属性而不是索引来引用`tuple`的某个元素。

这样一来，我们用`namedtuple`可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。

可以验证创建的`Point`对象是`tuple`的一种子类：

```python
>>> isinstance(p, Point)
True
>>> isinstance(p, tuple)
True
```

类似的，如果要用坐标和半径表示一个圆，也可以用`namedtuple`定义：

```python
# namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])
```

## deque

使用`list`存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为`list`是线性存储，数据量大的时候，插入和删除效率很低。

deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：

```python
>>> from collections import deque
>>> q = deque(['a', 'b', 'c'])
>>> q.append('x')
>>> q.appendleft('y')
>>> q
deque(['y', 'a', 'b', 'c', 'x'])
```

`deque`除了实现list的`append()`和`pop()`外，还支持`appendleft()`和`popleft()`，这样就可以非常高效地往头部添加或删除元素。

```python
In [22]: from collections import deque                                
                                                                      
In [23]: deque.                                                       
    deque.append     deque.count      deque.insert     deque.popleft  
    deque.appendleft deque.extend     deque.maxlen     deque.remove   
    deque.clear      deque.extendleft deque.mro        deque.reverse  
    deque.copy       deque.index      deque.pop        deque.rotate  

In [36]: list.
               list.append  list.count   list.insert  list.remove
               list.clear   list.extend  list.mro     list.reverse
               list.copy    list.index   list.pop     list.sort
```



## defaultdict

```python
data = collections.defaultdict(dict)
data = collections.defaultdict(list)
...
```





使用`dict`时，如果引用的Key不存在，就会抛出`KeyError`。如果希望key不存在时，返回一个默认值，就可以用`defaultdict`：

```python
>>> from collections import defaultdict
>>> dd = defaultdict(lambda: 'N/A')
>>> dd['key1'] = 'abc'
>>> dd['key1'] 			# key1存在
'abc'
>>> dd['key2'] 			# key2不存在，返回默认值
'N/A'
```

**注意默认值是调用函数返回的，而函数在创建`defaultdict`对象时传入。**

除了在Key不存在时返回默认值，`defaultdict`的其他行为跟`dict`是完全一样的。

## OrderedDict

使用`dict`时，Key是无序的。在对`dict`做迭代时，我们无法确定Key的顺序。

如果要保持Key的顺序，可以用`OrderedDict`：

```python
>>> from collections import OrderedDict
>>> d = dict([('a', 1), ('b', 2), ('c', 3)])
>>> d # dict的Key是无序的
{'a': 1, 'c': 3, 'b': 2}
>>> od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
>>> od # OrderedDict的Key是有序的
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

注意，`OrderedDict`的Key会按照插入的顺序排列，不是Key本身排序：

```python
>>> od = OrderedDict()
>>> od['z'] = 1
>>> od['y'] = 2
>>> od['x'] = 3
>>> od.keys() # 按照插入的Key的顺序返回
['z', 'y', 'x']
```

`OrderedDict`可以实现一个FIFO（先进先出, First In First Out）的dict，当容量超出限制时，先删除最早添加的Key：

```python
from collections import OrderedDict

class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print 'remove:', last
        if containsKey:
            del self[key]
            print 'set:', (key, value)
        else:
            print 'add:', (key, value)
        OrderedDict.__setitem__(self, key, value)
```

## Counter

`Counter`是一个简单的计数器，例如，统计字符出现的个数：

```python
>>> from collections import Counter
>>> c = Counter()
>>> for i in 'programming':
...     c[i] = c[i] + 1
...
>>> c
Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})
```

`Counter`实际上也是`dict`的一个子类，上面的结果可以看出，字符`'g'`、`'m'`、`'r'`各出现了两次，其他字符各出现了一次。





# contextlib

contextlib 模块提供了3个对象：装饰器 contextmanager、函数 nested 和上下文管理器 closing。使用这些对象，可以对已有的生成器函数或者对象进行包装，加入对上下文管理协议的支持，避免了专门编写上下文管理器来支持 with 语句。

## @contextmanager

contextmanager 用于对生成器函数进行装饰，生成器函数被装饰以后，返回的是一个上下文管理器，其 __enter__() 和 __exit__() 方法由 contextmanager 负责提供，而不再是之前的迭代子。被装饰的生成器函数只能产生一个值，否则会导致异常 RuntimeError；产生的值会赋值给 as 子句中的 target，如果使用了 as 子句的话。下面看一个简单的例子。

**装饰器 contextmanager 使用示例**

```python
from contextlib import contextmanager

@contextmanager
def demo():
    print('Code before yield-statement executes in __enter__')
    yield '*** contextmanager demo ***'
    print('Code after yield-statement executes in __exit__')

with demo() as value:
    print('Assigned Value: %s' % value)
```

运行后可以看到，生成器函数中 yield 之前的语句在 __enter__() 方法中执行，yield 之后的语句在 __exit__() 中执行，而 yield 产生的值赋给了 as 子句中的 value 变量。

需要注意的是，contextmanager 只是省略了 __enter__() / __exit__() 的编写，但并不负责实现资源的“获取”和“清理”工作；“获取”操作需要定义在 yield 语句之前，“清理”操作需要定义 yield 语句之后，这样 with 语句在执行 __enter__() / __exit__() 方法时会执行这些语句以获取/释放资源，即生成器函数中需要实现必要的逻辑控制，包括资源访问出现错误时抛出适当的异常。



## nested 函数

nested 可以将多个上下文管理器组织在一起，避免使用嵌套 with 语句。

**nested 语法**

```python
with nested(A(), B(), C()) as (X, Y, Z):
    # with-body code here
```

**nested 执行过程**

```python
with A() as X:
    with B() as Y:
        with C() as Z:
            # with-body code here
```

需要注意的是，发生异常后，如果某个上下文管理器的 __exit__() 方法对异常处理返回 False，则更外层的上下文管理器不会监测到异常。



## closing 上下文管理器

**上下文管理 closing 实现**

```python
class closing(object):
    # help doc here
    def __init__(self, thing):
        self.thing = thing
    
    def __enter__(self):
        return self.thing
    
    def __exit__(self, *exc_info):
        self.thing.close()
```

上下文管理器会将包装的对象赋值给 as 子句的 target 变量，同时保证打开的对象在 with-body 执行完后会关闭掉。closing 上下文管理器包装起来的对象必须提供 close() 方法的定义，否则执行时会报 AttributeError 错误。

**自定义支持 closing 的对象**

```python
class ClosingDemo(object):
    def __init__(self):
        self.acquire()
        
    def acquire(self):
        print('Acquire resources.')
        
    def free(self):
        print('Clean up any resources acquired.')
        
    def close(self):
        self.free()


with closing(ClosingDemo()):
	print('Using resources')
```

结果输出如下：

```python
Acquire resources.
Using resources
Clean up any resources acquired.
```

closing 适用于提供了 close() 实现的对象，比如网络连接、数据库连接等，也可以在自定义类时通过接口 close() 来执行所需要的资源“清理”工作。



# datetime

# functools

## functools.partial

## @functools.total_ordering

# hashlib

MD5加密

```
import hashlib
str = 'this is a md5 test.'
# 创建md5对象
md5 = hashlib.md5()
# Tips
# 此处必须声明encode
# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
md5.update(str.encode(encoding="utf-8"))

print('MD5加密前为 ：' + str)
print('MD5加密后为 ：' + md5.hexdigest())
```



# hmac

# inspect

## inspect.signature()

使用 `inspect.signature()` 函数,  从一个可调用对象中提取参数签名信息



# itertools

itertools.groupby()  分组函数

```
先排序, 
然后 groupby, 
然后 operator.itemgetter, 用来取 dict 中的 key, 省去了用 lambda函数

例如:
dict_list.sort(key=itemgetter('country'))
# list_group = groupby(dict_list, key=lambda x: x['country'])
list_group = groupby(dict_list, itemgetter('country'))
for key, group in list_group:
    for g in group:   # group 是迭代器,包含所有分组列表
        print key, g

ret = [(key, list(group)) for key, group in list_group]
```

# io

使用操作类文件对象的程序来操作文本或二进制字符串:

## io.StringIO()

```
>>> s = io.StringIO()
>>> s.write('Hello World\n')
12
>>> print('This is a test', file=s)
15
>>> # Get all of the data written so far
>>> s.getvalue()
'Hello World\nThis is a test\n'
>>>

>>> # Wrap a file interface around an existing string
>>> s = io.StringIO('Hello\nWorld\n')
>>> s.read(4)
'Hell'
>>> s.read()
'o\nWorld\n'
>>>
```

## io.BytesIO()

```
>>> s = io.BytesIO()
>>> s.write(b'binary data')
>>> s.getvalue()
b'binary data'
>>>
```

当你想**模拟一个普通的文件**的时候 `StringIO` 和 `BytesIO` 类是很有用的。 比如，在**单元测试**中，你可以使用 `StringIO` 来创建一个包含测试数据的类文件对象， 这个对象可以被传给某个参数为普通文件对象的函数。

需要注意的是， `StringIO` 和 `BytesIO` 实例并没有正确的整数类型的文件描述符。 因此，它们不能在那些需要使用真实的系统级文件如文件、管道或者是套接字的程序中使用。



# json

## json.loads参数

object_pairs_hook

object_hook

解码JSON数据并在一个OrderedDict中保留其顺序:

```python
>>> s = '{"name": "ACME", "shares": 50, "price": 490.1}'
>>> from collections import OrderedDict
>>> data = json.loads(s, object_pairs_hook=OrderedDict)
>>> data
OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])
>>>
```

将JSON字典转换为Python对象：

```python
>>> class JSONObject:
...     def __init__(self, d):
...         self.__dict__ = d
...
>>>
>>> data = json.loads(s, object_hook=JSONObject)
>>> data.name
'ACME'
>>> data.shares
50
>>> data.price
490.1
>>>

# JSON解码后的字典作为一个单个参数传递给 __init__() 。 然后，你就可以随心所欲的使用它了，比如作为一个实例字典来直接使用它。
```





# os

os.sep	根据所处平台,  自动采用相应的文件路径分隔符号





# pathlib

## pathlib.Path

可以使用 `pathlib.Path` 替代使用 `os.path` 的一系列操作

```python
# path = pathlib.Path("/home/1.txt")
# path = pathlib.Path("/home")
# 在Windows上返回`WindowsPath`, 在Linux上返回`..`

path.home()  		# os.path.expanduser('~')
path.cwd()  		# os.getcwd()
path.samefile()  	# os.path.samefile()
path.iterdir()
path.glob()
path.rglob()  # l -> link
path.match()  # Return True if this path matches the given pattern.
path.absolute()
path.resolve()
path.expanduser()  # os.path.expanduser

path.stat()  # os.stat()
path.lstat()  # link stat
path.owner()
path.group()
path.chmod()
path.unlink()  # Remove this file or link. If the path is a directory, use rmdir() instead.
path.symlink_to()
path.rmdir()  # The directory must be empty
path.rename()
path.replace()

path.exists()
path.is_dir()
path.is_file()
path.is_symlink()

path.open()  # open()
path.read_bytes()
path.read_text()
path.write_bytes()
path.write_text()

path.touch(mode=0o666, exist_ok=True)
mode=0o777, parents=False, exist_ok=False   # 递归创建: parents=True
```

## 两种路径字符串的获取

1. 本地文件/目录路径:  `str(path)`

2. URL路径:  `path.as_posix()`





# shutil

## shutil.rmtree

```python
# shutil.rmtree 无法删除 文件/目录的软连接
```





# struct

# sys

#subprocess

## subprocess.Popen

在python代码中执行shell cmd

```python
# 注意 cwd 参数指定 cmd 在哪个路径下执行
# 传入cwd参数, 则不需要使用 os.chdir(target) 来回切换工作目录
subprocess.Popen(cmd="ls", cwd="/home/")
```





# tempfile

# types



# tarfile









# weakref

