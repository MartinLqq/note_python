# fnmatch

- 推荐使用 glob

# 基本介绍

此模块的主要作用是文件名称的匹配，并且匹配的模式使用的 unix shell 风格。

> filename match

fnmatch 比较简单就4个方法分别是：

1. fnmatch：判断文件名是否符合特定的模式。
2. fnmatchcase：判断文件名是否符合特定的模式，区分大小写。
3. filter：返回输入列表中，符合特定模式的文件名列表。
4. translate：将通配符模式转换成正则表达式。

## fnmatch支持的通配符

| 通配符 | 含义                    |
| ------ | ----------------------- |
| *      | 匹配任何数量的字符      |
| ？     | 匹配单个字符            |
| [seq]  | 匹配seq中的字符         |
| [!seq] | 匹配除seq以外的任何字符 |

# 资源

- https://www.cnblogs.com/dachenzi/p/7993401.html

# 使用方法

## fnmatchcase、fnmatch

```python
>>> from fnmatch import fnmatch, fnmatchcase

>>> assert fnmatchcase(name='a.txt', pat='[A].txt') == False
>>> assert fnmatch(name='1.txt', pat='*.txt') == True


>>> os.listdir(os.curdir)
['A1.jpg', 'a1.txt', 'a2.txt', 'aA.txt', 'b3.jpg', 'b2.jpg', 'b1.jpg']

>>> [ name for name in os.listdir(os.curdir) if fnmatch.fnmatchcase(name,"A?.jpg") ]
['A1.jpg']

>>> [ name for name in os.listdir(os.curdir) if fnmatch.fnmatch(name,'*.jpg') ]
['A1.jpg', 'b3.jpg', 'b2.jpg', 'b1.jpg']

>>> [ name for name in os.listdir(os.curdir) if fnmatch.fnmatch(name,"[ab]*") ]
['a1.txt', 'a2.txt', 'aA.txt', 'b3.jpg', 'b2.jpg', 'b1.jpg']

>>> [ name for name in os.listdir(os.curdir) if fnmatch.fnmatch(name,"[!a]*") ]
['A1.jpg', 'b3.jpg', 'b2.jpg', 'b1.jpg']

>>> [ name for name in os.listdir(os.curdir) if fnmatch.fnmatch(name,"b?.jpg") ]
['b3.jpg', 'b2.jpg', 'b1.jpg']
```

## filter

filter 和 fnmatch 类似，只不过 filter 接受的第一个参数是一个文件名列表，返回符合表达式的列表(即：筛选) 

```python
from fnmatch import filter

names = ['a.txt', 'b.txt']
assert filter(names, pat='[ab].txt') == names
```

## translate

将通配符模式转换成正则表达式。

```python
from fnmatch import translate

assert translate('*.txt') == "(?s:.*\.txt)\Z"
```

# 扩展内容

## glob

fnmatch 和 glob 模块都是用来做字符串匹配文件名的标准库。 

- glob的作用就相当于 os.listdir 加上 fnmatch。使用 glob 以后就不用使用 os.listdir 获取文件列表了。
-  glob 同样支持通配符和 fnmatch 相同，并且在通配符表达式中支持路径 

- glob内部调用了 fnmatch 的函数,  glob 比 fnmatch 更简单，只有三个函数:

1. glob
2. iglob
3. escape



### glob.glob、glob.iglob

glob 和 iglob 的区别在于 glob 返回的是一个列表，iglob 返回的是一个生成器对象 

```python
import glob
import collections

assert isinstance(
    glob.iglob('*.md'),
    collections.Generator
)
print(glob.glob('*.md'))

```

### glob.escape





### 细节

判断是否是隐藏文件/文件夹

```python
def _ishidden(path):
    return path[0] in ('.', b'.'[0])
```

