# howdoi

# 基本介绍

howdoi 基本流程如下：

- step1：利用 site 语法组装搜索语句 (默认指定搜索 stackoverflow 网站)
- step2：利用 google 搜索接口获取搜索引擎第一页排名第一的链接
- step3：访问该链接，根据排名从高到底，提取代码块文本
- step4：提取到就显示到终端，没有提取到就提示未找到答案

`howdoi`也做了一些其他的工作：

- 代理设置
- 既往问题进行缓存，提高下次查询的速度
- 查询的目标网站可配置
- 做成 Python script 脚本命令，方便快捷
- 代码高亮格式化输出

# 使用方法

# 一些 imports

## `__future__`

如果某个版本中出现了某个新的功能特性，而且这个特性和当前版本中使用的不兼容，也就是它在该版本中不是语言标准，那么我如果想要使用的话就需要从 `__future__` 模块导入。

```python
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
# ... 
# __future__模块的 all_feature_names 列表中指明了所有的兼容方法

# 加上这些，如果你的python版本是 python2.X，你也得按照 python3.X 那样使用这些函数。
print("Hello world")  # python2.x & python3.x
```



## gc

- 笔记来源:  https://www.cnblogs.com/franknihao/p/7326849.html

### python 垃圾回收机制

Python中，主要依靠 gc（garbage collector）模块的引用计数技术来进行垃圾回收。

- 所谓引用计数，就是考虑到Python中变量的本质不是内存中一块存储数据的区域，而是对一块内存数据区域的引用。
- 所以python可以给所有的对象（内存中的区域）维护一个引用计数的属性，在一个引用被创建或复制的时候，让python 把相关对象的引用计数+1；相反当引用被销毁的时候就把相关对象的引用计数-1。
- 当对象的引用计数减到0时，自然就可以认为整个python中不会再有变量引用这个对象，所以就可以把这个对象所占据的内存空间释放出来了。 

引用计数的不足:

- 引用计数技术在每次引用创建和销毁时都要多做一些操作，这可能是一个小缺点，当创建和销毁很频繁的时候难免带来一些效率上的不足。但是其最大的好处就是实时性，其他语言当中，垃圾回收可能只能在一些固定的时间点上进行，比如当内存分配失败的时候进行垃圾回收，而引用计数技术可以动态地进行内存的管理。 
-  引用计数的致命缺点:  基于引用计数的垃圾回收机制因为循环引用的存在可能会导致内存泄露 

### 循环引用

在Python中有一些类型比如 tuple, list, dict 等，其作为容器类型可以包含若干个对象。如果某个对象就是它本身，或者两个对象中互相包含对方，那么就构成了一个循环引用。 

```python
import sys
class Test: pass

k = Test()
print(sys.getrefcount(k))    # 2

t = Test()
t._self = t
print(sys.getrefcount(t))    # 3

# sys.getrefcount() 函数用来查看一个对象有几个引用
```

一般状态下的普通变量如上面的k，返回值都是 2,  不是1,  是因为把 k 作为参数传递给函数的时候，要先复制一份引用，然后把这个引用赋给形式参数供函数运行，在函数运行过程中，会保持这个引用始终升高为 2。 

### 内存泄漏

del 语句可以消除一个引用关系。对于没有 `_self` 这样的自我引用的情况下，del k 相当于销毁了变量名到内存地址的这一层引用关系，自 getrefcount 执行完成之后，这部分内存就可以得到释放了。但是如果存在 `_self` 这个自我引用的话，即使消除了del t 这个引用关系，这个对象的引用计数仍然是 1。得不到销毁，所以会造成 **内存泄露**。 



### 标记-清除的回收机制

　　针对循环引用这个问题，比如有两个对象互相引用了对方，当外界没有对他们有任何引用，也就是说他们各自的引用计数都只有1的时候，如果可以识别出这个循环引用，把它们属于循环的计数减掉的话，就可以看到他们的真实引用计数了。基于这样一种考虑，有一种方法，比如从对象A出发，沿着引用寻找到对象B，把对象B的引用计数减去1；然后沿着B对A的引用回到A，把A的引用计数减1，这样就可以把这层循环引用关系给去掉了。

　　不过这么做还有一个考虑不周的地方。假如A对B的引用是单向的， 在到达B之前我不知道B是否也引用了A，这样子先给B减1的话就会使得B称为不可达的对象了。

　　为了解决这个问题，python中常常把内存块一分为二，将一部分用于保存真的引用计数，另一部分拿来做为一个引用计数的副本，在这个副本上做一些实验。比如在副本中维护两张链表，一张里面放不可被回收的对象合集，另一张里面放被标记为可以被回收（计数经过上面所说的操作减为0）的对象，然后再到后者中找一些被前者表中一些对象直接或间接单向引用的对象，把这些移动到前面的表里面。这样就可以让不应该被回收的对象不会被回收，应该被回收的对象都被回收了。

### 分代回收

　　分代回收策略着眼于提升垃圾回收的效率。研究表明，任何语言，任何环境的编程中，对于变量在内存中的创建/销毁，总有频繁和不那么频繁的。比如任何程序中总有生命周期是全局的、部分的变量。

　　而在垃圾回收的过程中，其实在进行垃圾回收之前还要进行一步垃圾检测，即检查某个对象是不是垃圾，该不该被回收。当对象很多，垃圾检测将耗费大量的时间而真的垃圾回收花不了多久。对于这种多对象程序，我们可以把一些进行垃圾回收频率相近的对象称为“同一代”的对象。垃圾检测的时候可以对频率较高的“代”多检测几次，反之，进行垃圾回收频率较低的“代”可以少检测几次。这样就可以提高垃圾回收的效率了。至于如何判断一个对象属于什么代，python中采取的方法是通过其 **生存时间** 来判断。如果在好几次垃圾检测中，该变量都是 reachable 的话，那就说明这个变量越不是垃圾，就要把这个变量往高的代移动，要减少对其进行垃圾检测的频率。



### 总结: python 垃圾回收

 python对于垃圾回收，采取的是引用计数为主，标记-清除+分代回收为辅的回收策略 



###  gc 模块介绍

python对于垃圾回收，采取的是引用计数为主，标记-清除+分代回收为辅的回收策略。对于循环引用的情况，一般的自动垃圾回收方式肯定是无效了，这时候就需要显式地调用一些操作来保证垃圾的回收和内存不泄露。这就要用到python内建的垃圾回收模块 gc 模块了。 

#### gc.collect()

专门用来处理循环引用，返回处理这些循环引用一共释放掉的对象个数

```python
import sys
import gc

a = [1]
b = [2]
a.append(b)
b.append(a)
# 此时a和b之间存在循环引用
sys.getrefcount(a)    #结果应该是3
sys.getrefcount(b)    #结果应该是3
del a
del b
# 删除了变量名a，b到对象的引用，此时引用计数应该减为1，即只剩下互相引用
try:
    sys.getrefcount(a)
except NameError:
     print('a is invalid')
# 此时，原来 a 指向的那个对象引用不为 0，python不会自动回收它的内存空间
# 但是我们又没办法通过变量名 a 来引用它了，这就导致了内存泄露
unreachable_count = gc.collect()  # 2,  处理这些循环引用一共释放了 2 个对象

```

####  gc.get_threshold()

　　这个方法涉及到之前说过的分代回收的策略。python中默认把所有对象分成三代。第0代包含了最新的对象，第2代则是最早的一些对象。在一次垃圾回收中，所有未被回收的对象会被移到高一代的地方。

　　这个方法返回的是(700,10,10)，这也是 gc 的默认值。这个值的意思是说，在第0代对象数量达到700个之前，不把未被回收的对象放入第一代；而在第一代对象数量达到10个之前也不把未被回收的对象移到第二代。可以使用 gc.set_threshold(threashold0,threshold1,threshold2) 来手动设置这组阈值。



## appdirs

提供一些方法,  用于快速获取或生成本地的一些路径,  如app数据存储路径、缓存路径......

详见 appdirs 的源码分析



## cachelib

通过相同的接口调用各种不同的 缓存库.

详见 cachelib 源码分析



## pygments

 It is a **generic syntax highlighter** written in Python that supports over 500 languages and text formats, for use in code hosting, forums, wikis or other applications that need to prettify source code. 



## pyquery

pyquery库是jQuery的Python实现，能够以jQuery的语法来操作解析 HTML 文档，易用性和解析速度都很好，和它差不多的还有BeautifulSoup 

## codecs

 codecs专门用作编码转换 



# 代码结构

```
howdoi
howdoi # 核心代码目录
    init.py
    howdoi.py # 核心代码
    LICENSE.txt
    README.rst
    setup.py
    requirements.txt
    test_howdoi.py # 测试文件
    其他文件
```



## py 兼容处理

### unicode 字符串兼容

```python
python2和python3处理unicode的方式不同
# Handle Unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
	import codecs
	def u(x):
		return codecs.unicode_escape_decode(x)[0]
else:
	def u(x):
		return x
```





## 更多

TODO...