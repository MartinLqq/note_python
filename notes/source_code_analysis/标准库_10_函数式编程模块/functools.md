# functools

# 资源

- 官方文档:  https://docs.python.org/zh-cn/3.6/library/functools.html
- 脚本之家:  https://www.jb51.net/article/108195.htm

# 基本介绍与使用方法

functools 模块提供用于调整或扩展函数和其他可调用对象的工具，而无需完全重写它们。 



## cmp_to_key()

```python
cmp_to_key(func) 
```

该函数用于将旧式的比较函数转换为关键字函数。

旧式的比较函数：接收两个参数，返回比较的结果。返回值小于零则前者小于后者，返回值大于零则相反，返回值等于零则两者相等。

关键字函数：接收一个参数，返回其对应的可比较对象。例如 sorted(), min(), max(), heapq.nlargest(), heapq.nsmallest(), itertools.groupby() 都可作为关键字函数。

在 Python 3 中，有很多地方都不再支持旧式的比较函数，此时可以使用 cmp_to_key() 进行转换。

```python
sorted(iterable, key=cmp_to_key(cmp_func))
```



## total_ordering()

```python
total_ordering(cls)
```

这是一个类装饰器，用于自动实现类的比较运算。

我们只需要在类中实现 `__eq__()` 方法和以下方法中的任意一个 `__lt__()`, `__le__()`, `__gt__()`, `__ge__()`，那么 total_ordering() 就能自动帮我们实现余下的几种比较运算。

```python
@total_ordering
class Student: 
  def __eq__(self, other):
    return ((self.lastname.lower(), self.firstname.lower()) ==
        (other.lastname.lower(), other.firstname.lower()))
  def __lt__(self, other):
    return ((self.lastname.lower(), self.firstname.lower()) <
        (other.lastname.lower(), other.firstname.lower()))
```



## reduce()

```python
reduce(function, iterable[, initializer])
```

 该函数与 Python 内置的 reduce() 函数相同，主要用于编写兼容 Python 3 的代码。 



## partial()

```python
partial(func[, args][, *keywords])
```

该函数返回一个 partial 对象，调用该对象的效果相当于调用 func 函数，并传入位置参数 args 和关键字参数 keywords 。如果调用该对象时传入了位置参数，则这些参数会被添加到 args 中。如果传入了关键字参数，则会被添加到 keywords 中。 

 partial() 函数的等价实现大致如下： 

```python
def partial(func, *args, **keywords): 
  def newfunc(*fargs, **fkeywords):
    newkeywords = keywords.copy()
    newkeywords.update(fkeywords)
    return func(*(args + fargs), **newkeywords)
  newfunc.func = func
  newfunc.args = args
  newfunc.keywords = keywords
  return newfunc
```

 partial() 函数主要用于“冻结”某个函数的部分参数，返回一个参数更少、使用更简单的函数对象。 

```python
>>> from functools import partial
>>> basetwo = partial(int, base=2)
>>> basetwo.__doc__ = 'Convert base 2 string to an int.'
>>> basetwo('10010')
18
```



## update_wrapper()

```python
update_wrapper(wrapper, wrapped[, assigned][, updated])
# 默认情况下, 装饰器的被装饰对象没有 __name__ 和 __doc__ 属性。 这样不利于被装饰的函数进行调试。可以使用 update_wrapper() 从原函数复制或新增属性到 被装饰对象。
```

该函数用于更新包装函数（wrapper），使它看起来像原函数一样。可选的参数是一个元组，assigned 元组指定要直接使用原函数的值进行替换的属性，updated 元组指定要对照原函数进行更新的属性。这两个参数的默认值分别是模块级别的常量：WRAPPER_ASSIGNMENTS 和 WRAPPER_UPDATES。前者指定了对包装函数的 `__name__`, `__module__`, __doc__ 属性进行直接赋值，而后者指定了对包装函数的 `__dict__` 属性进行更新。

该函数主要用于装饰器函数的定义中，置于包装函数之前。如果没有对包装函数进行更新，那么被装饰后的函数所具有的元信息就会变为包装函数的元信息，而不是原函数的元信息。



## wraps()

```python
wraps(wrapped[, assigned][, updated])
```

wraps() 简化了 update_wrapper() 函数的调用。它等价于 partial(update_wrapper, wrapped=wrapped, assigned, updated=updated)。 

```python
>>> from functools import wraps
>>> def my_decorator(f):
...   @wraps(f)
...   def wrapper(*args, **kwds):
...     print('Calling decorated function')
...     return f(*args, **kwds)
...   return wrapper
 
>>> @my_decorator
... def example():
...   """Docstring"""
...   print('Called example function')
 
>>> example()
Calling decorated function 
Called example function 
>>> example.__name__
'example'
>>> example.__doc__
'Docstring'
```

 如果不使用这个函数，示例中的函数名就会变成 wrapper ，并且原函数 example() 的说明文档（docstring）就会丢失。 

# 对外接口

## `__all__`

```python
__all__ = [
    'update_wrapper', 
    'wraps', 
    'WRAPPER_ASSIGNMENTS', 
    'WRAPPER_UPDATES',
    'total_ordering',
    'cmp_to_key',
    'lru_cache',
    'reduce',
    'partial',
    'partialmethod',
    'singledispatch'
]
```



