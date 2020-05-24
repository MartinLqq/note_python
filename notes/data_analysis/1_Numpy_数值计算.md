# 【Numpy快速入门】

NumPy(Numerical Python) 是一个运行速度非常快的数学库。 主要用于数组计算，包含：

- NumPy提供了一个**N维数组类型ndarray**，它描述了**相同类型**的“items”的集合。 
- 广播功能函数
- 整合 C/C++/Fortran 代码的工具
- 线性代数、傅里叶变换、随机数生成等功能
- 众多机器学习框架的基础库 (Scipy/Pandas/scikit-learn/Tensorflow)

**安装**

使用Anaconda环境，安装：

```shell
conda create -n data_analysis python=3.5 numpy pandas matplotlib sympy
```

**应用**

NumPy 通常与 SciPy（Scientific Python）和 Matplotlib（绘图库）一起使用， 这种组合广泛用于替代 MatLab。

SciPy 是一个开源的 Python 算法库和数学工具包。SciPy 包含的模块有最优化、线性代数、积分、插值、特殊函数、快速傅里叶变换、信号处理和图像处理、常微分方程求解和其他科学与工程中常用的计算。

Matplotlib 是 Python 编程语言及其数值数学扩展包 NumPy 的可视化操作界面。它为利用通用的图形用户界面工具包，如 Tkinter, wxPython, Qt 或 GTK+ 向应用程序嵌入式绘图提供了应用程序接口（API）。

- NumPy 官网 http://www.numpy.org/
- NumPy 源代码：https://github.com/numpy/numpy
- SciPy 官网：https://www.scipy.org/
- SciPy 源代码：https://github.com/scipy/scipy
- Matplotlib 官网：https://matplotlib.org/
- Matplotlib 源代码：https://github.com/matplotlib/matplotlib



## 与Python数组的区别

NumPy数组 和 原生Python Array（数组）之间有几个重要的区别：

- NumPy 数组大小固定，与Python的原生数组对象（可以动态增长）不同。更改ndarray的大小将创建一个新数组并删除原来的数组。
- NumPy 数组中的数据类型相同，因此在内存中的大小相同。 例外：Python的原生数组里包含了NumPy的对象的时候，这种情况下就允许不同大小元素的数组。
- NumPy 数组有助于对大量数据进行高级数学和其他类型的操作。通常，这些操作的执行效率更高，比使用Python原生数组的代码更少。



## NumPy 为什么快？

### 1. Numpy数组的内存块风格

Numpy在存储数据的时候，内存分布连续，数据处理速度快。(python列表的存储地址不连续)

Numpy数组在计算机内存里是存储在一个连续空间上的，而对于这个连续空间，我们如果创建 Array 的方式不同，在这个连续空间上的排列顺序也有不同。

- 创建array的默认方式是 “C-type”,  以 row 为主在内存中连续排列
- 如果是 “Fortran” 的方式创建的，就是以 column 为主在内存中连续排列

**查看ndarray 对象的内存布局信息:**

```python
import numpy as np
a = np.array([[1,2,3], [4,5,6]])
print(a.flags)
"""
  C_CONTIGUOUS : True		# 默认C风格, 即以 row 为主在内存中连续排列
  F_CONTIGUOUS : False		# Fortran风格, 即以 column 为主在内存中连续排列
  OWNDATA : True
  WRITEABLE : True
  ALIGNED : True
  WRITEBACKIFCOPY : False
  UPDATEIFCOPY : False
"""
```







### 2. Numpy的并行化运算

Numpy 支持并行化运算，也叫矢量化运算。 

**1、矢量化**

矢量化描述了代码中没有任何显式的循环、索引等 - 这些当然是预编译的C代码中“幕后”优化的结果。矢量化代码有许多优点，其中包括：

- 矢量化代码更简洁易读
- 更少的代码行通常意味着更少的错误
- 矢量化导致产生更多 “Pythonic” 代码。减少可见的`for`循环。



**2、广播**

广播是用于描述操作的隐式逐元素行为的术语; 一般来说，在NumPy中，所有操作，不仅仅是算术运算，而是逻辑，位，功能等，都以这种隐式的逐元素方式表现，即它们进行广播。 

当涉及到 *ndarray* 时，NumPy 数组逐个元素的操作是“默认模式” 。

广播相关链接：

- https://www.numpy.org.cn/user/basics/broadcasting.html
- https://numpy.org/devdocs/user/theory.broadcasting.html
- https://numpy.org/devdocs/reference/generated/numpy.broadcast.html





# 文档

- 快速入门教程：https://www.numpy.org.cn/user/quickstart.html
- Runoob 教程:  https://www.runoob.com/numpy/numpy-tutorial.html
- 常用 API：https://www.numpy.org.cn/reference/routines/
- **NumPy 基础知识**：https://www.numpy.org.cn/user/basics/
- **NumPy 数据分析练习**：https://www.numpy.org.cn/article/advanced/numpy_exercises_for_data_analysis.html
- **machinelearningplus网站**上的Numpy等资料：https://www.machinelearningplus.com/python/numpy-tutorial-part1-array-python-examples/





# Ndarray 对象

- `ndarray` 即 `numpy.array`
- `numpy.array`与标准Python库类`array.array`不同，后者只处理一维数组并提供较少的功能。

**初始化参数**

```python
numpy.array(p_object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
```

| 名称     | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| p_object | array_like，数组或嵌套的数列                                 |
| dtype    | 数组元素的数据类型，可选                                     |
| copy     | 对象是否需要复制，可选                                       |
| order    | {'K', 'A', 'C', 'F'}, optional,  创建数组的样式，C为行方向，F为列方向 |
| subok    | 默认返回一个与基类类型一致的数组                             |
| ndmin    | 指定生成数组的最小维度                                       |



## 数组属性

比较重要的 ndarray 对象属性：

| 属性             | 说明                                                         |
| :--------------- | :----------------------------------------------------------- |
| ndarray.ndim     | 秩，即轴的数量或维度的数量                                   |
| ndarray.shape    | 数组的维度，对于矩阵，n 行 m 列                              |
| ndarray.size     | 数组元素的总个数，相当于 .shape 中 n*m 的值                  |
| ndarray.dtype    | ndarray 对象的元素类型                                       |
| ndarray.itemsize | ndarray 对象中每个元素的大小，以字节为单位                   |
| ndarray.flags    | ndarray 对象的内存布局信息                                   |
| ndarray.real     | ndarray元素的实部                                            |
| ndarray.imag     | ndarray 元素的虚部                                           |
| ndarray.data     | 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。 |

- **ndarray.ndim** - 数组的轴（维度）的个数。在Python世界中，维度的数量被称为rank。

  ```
  # 以下数组有2个轴, 第一轴的长度为2, 第二轴的长度为3。
  [[ 1., 0., 0.],
   [ 0., 1., 2.]]
  ```

- **ndarray.shape** - `shape` 元组的长度就是rank或维度的个数 `ndim`。 

  - ndarray.shape 也可以用于调整数组大小。 

    ```python
    a = np.array([[1,2,3],[4,5,6]]) 
    a.shape = (3, 2)
    ```

  - NumPy 也提供了 reshape 函数来调整数组大小。 

    ```python
    np.array([[1,2,3],[4,5,6]]).reshape(3,2)
    ```

- **ndarray.dtype** - 一个描述数组中元素类型的对象。可以使用标准的Python类型创建或指定dtype。另外NumPy提供它自己的类型。例如 `numpy.int32`、`numpy.int16` 和 `numpy.float64`。

- **ndarray.itemsize** - 数组中每个元素的字节大小。例如，元素为 `float64` 类型的数组的 `itemsize` 为8（=64/8），而 `complex32` 类型的数组的 `itemsize` 为4（=32/8）。它等于 `ndarray.dtype.itemsize` 。





# 多维数组的理解

## 二维

![img](https://img-blog.csdn.net/20170427214909616?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcGlwaXNvcnJ5/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

## 三维

![三维数组](https://img-blog.csdn.net/20180111201812607?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTmlhbnp1X0V0aGFuX1poZW5n/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



## 四维

![四维数组](https://img-blog.csdn.net/20180111201936394?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvTmlhbnp1X0V0aGFuX1poZW5n/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)





# 数据类型

numpy 支持的数据类型比 Python 内置的类型要多很多，基本上可以和 C 语言的数据类型对应上，其中部分类型对应为 Python 内置的类型。

## 常用基本类型

numpy 的数值类型实际上是 `dtype` 对象的实例，并对应唯一的字符，包括 np.bool_，np.int32，np.float32，等等。

|     名称      |                       描述                        | 简写(字符代码) |
| :-----------: | :-----------------------------------------------: | :------------: |
|    np.bool    |      用一个字节存储的布尔类型（True或False）      |      'b'       |
|    np.int8    |             一个字节大小，-128 至 127             |      'i'       |
|   np.int16    |               整数，-32768 至 32767               |      'i2'      |
|   np.int32    |            整数，-2 **31 至 2** 32 -1             |      'i4'      |
|   np.int64    |            整数，-2 **63 至 2** 63 - 1            |      'i8'      |
|   np.uint8    |               无符号整数，0 至 255                |      'u'       |
|   np.uint16   |              无符号整数，0 至 65535               |      'u2'      |
|   np.uint32   |           无符号整数，0 至 2 ** 32 - 1            |      'u4'      |
|   np.uint64   |           无符号整数，0 至 2 ** 64 - 1            |      'u8'      |
|  np.float16   | 半精度浮点数：16位，正负号1位，指数5位，精度10位  |      'f2'      |
|  np.float32   | 单精度浮点数：32位，正负号1位，指数8位，精度23位  |      'f4'      |
|  np.float64   | 双精度浮点数：64位，正负号1位，指数11位，精度52位 |      'f8'      |
| np.complex64  |     复数，分别用两个32位浮点数表示实部和虚部      |      'c8'      |
| np.complex128 |     复数，分别用两个64位浮点数表示实部和虚部      |     'c16'      |
|  np.object_   |                    python对象                     |      'O'       |
|  np.string_   |                      字符串                       |      'S'       |
|  np.unicode_  |                    unicode类型                    |      'U'       |



## 数据类型对象np.dtype

dtype是用来描述与数组对应的内存区域如何使用，这依赖如下几个方面：

- 数据的类型（整数，浮点数或者 Python 对象）
- 数据的大小（例如， 整数使用多少个字节存储）
- 数据的字节顺序（小端法或大端法）
- 在结构化类型的情况下，字段的名称、每个字段的数据类型和每个字段所取的内存块的部分
- 如果数据类型是子数组，它的形状和数据类型

> 字节顺序是通过对数据类型预先设定"<"或">"来决定的。"<"意味着小端法(最小值存储在最小的地址，即低位组放在最前面)。">"意味着大端法(最重要的字节存储在最小的地址，即高位组放在最前面)。

构造 dtype 对象：

```python
numpy.dtype(obj, align=False, copy=False)

# obj	要转换为的数据类型对象
# align	如果为 true，填充字段使其类似 C 的结构体。
# copy	复制 dtype 对象 ，如果为 false，则是对内置数据类型对象的引用
```



示例:

```python
# 使用标量类型
dt = np.dtype(np.int32)	# int32

# int8, int16, int32, int64 四种数据类型可以使用字符串 'i1', 'i2','i4','i8' 代替
dt = np.dtype('i4')	# int32

# 字节顺序标注
dt = np.dtype('<i4')	# int32

```

### >自定义结构化数据类型

通常对于numpy数组来说，存储的都是同一类型的数据。但其实也可以通过np.dtype实现 **数据类型对象表示数据结构**。 

- 自定义结构化数据类型,   类型字段和对应的实际类型将被创建
- 元素类型可以不相同

```python
# [栗子1]
# 1. 创建结构化数据类型
dt = np.dtype([('age',np.int8)])	# [('age', 'i1')]
# 2. 将数据类型应用于 ndarray 对象
a = np.array([(10,),(20,),(30,)], dtype=dt)		# [(10,) (20,) (30,)]
# 3. 类型字段名可以用于存取实际的 age 列
print(a['age'])		# [10 20 30]

# [栗子2]
# 定义一个结构化数据类型 student
student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')])
a = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype=student)

# [栗子3]
>>> mytype = np.dtype([('name', np.string_, 10), ('height', np.float64)])
>>> mytype
dtype([('name', 'S10'), ('height', '<f8')])

>>> arr = np.array([('Sarah', (8.0)), ('John', (6.0))], dtype=mytype)
>>> arr
array([(b'Sarah', 8.), (b'John', 6.)],
      dtype=[('name', 'S10'), ('height', '<f8')])
>>> arr[0]['name']

```

对于存储复杂关系的数据，其实选择 Pandas 更加方便.





## 修改类型 .astype()

要转换数组的类型，首选 .astype() 方法，或用类型本身作为函数。例如：

```python
>>> z.astype(float)                 
array([  0.,  1.,  2.])
>>> np.int8(z)
array([0, 1, 2], dtype=int8)
```



## 修改小数位数  .round()

ndarray.round(arr, out)

Return a with each element rounded to the given number of decimals.





# 创建数组

- 从常规Python列表或元组转换数组
  - **np.array**
- 创建具有初始占位符内容的数组
  - **np.zeros**
  - **np.ones**
  - np.empty
  - np.repeat
- 从数值范围创建数组
  - **np.arange**
  - **np.linspace**
  - np.logspace
- 从已有的数组创建数组
  - np.asarray
  - np.frombuffer
  - np.fromiter
- 创建随机数组:  np.random模块 
  - 均匀分布
    - np.random.rand(10)
    - np.random.uniform(0,100)
    - np.random.randint(100)
  - **正态分布**
    - 给定均值／标准差／维度的正态分布
    - np.random.normal(1.75, 0.2, (3,4))
    - np.random.standard_normal(size=(3,4))     标准正态分布: 平均值0, 标准差1

```python
# ---------- 从常规Python列表或元组中创建数组 ----------
np.array([2,3,4])
# array 还可以将序列的序列转换成二维数组，将序列的序列的序列转换成三维数组，等等。
np.array([(1.5,2,3), (4,5,6)])
# 也可以在创建时显式指定数组的类型
np.array([ [1,2], [3,4] ], dtype=complex)

# ---------- 创建具有初始占位符内容的数组 ----------
"""
数组的元素最初未知，但它的大小已知
np.zeros 创建一个由0组成的数组
np.ones  创建指定形状的数组，数组元素以 1 来填充：
np.empty 创建一个数组，其初始内容是随机的，取决于内存的状态
np.repeat(a, repeats, axis): Repeat elements of an array.
"""
>>> np.zeros( (3,4) )
array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
>>> np.ones( (2,3,4), dtype=np.int16 )  # dtype can also be specified
array([[[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]],
       [[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]]], dtype=int16)
>>> np.empty( (2,3) )  # uninitialized, output may vary
array([[  3.73603959e-262,   6.02658058e-154,   6.55490914e-260],
       [  5.30498948e-313,   3.14673309e-307,   1.00000000e+000]])

# ---------- 从数值范围创建数组 ----------
# np.arange 从数值范围创建数组.	(限制步长step)
# arange(start=None, stop=None, step=None, dtype=None)
>>> np.arange( 10, 30, 5 )
array([10, 15, 20, 25])
>>> np.arange( 0, 2, 0.3 ) # it accepts float arguments
array([ 0. ,  0.3,  0.6,  0.9,  1.2,  1.5,  1.8])

# np.linspace 从数值范围创建数组.  (限制元素个数num)
# linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
"""
    start		序列的起始值
    stop		序列的终止值，如果endpoint为true，该值包含于序列中
    num			要生成的等间隔样例数量，默认为50
    endpoint	序列中是否包含stop值，默认为ture
    retstep		如果为true，返回样例， 以及连续数字之间的步长
    dtype		输出ndarray的数据类型
"""
>>> np.linspace( 0, 2, 9 )                 # 9 numbers from 0 to 2
array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ,  1.25,  1.5 ,  1.75,  2.  ])
>>> x = np.linspace( 0, 2*np.pi, 100 )        # useful to evaluate function at lots of points
>>> f = np.sin(x)

# np.logspace 用于创建一个于等比数列
# np.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
np.logspace(1.0, 2.0, num=10)
np.logspace(0,9,10, base=2)

# ---------- 从已有的数组创建数组 ----------
np.asarray    	np.asarray引用原来的数组;
				np.array创建一个新的数组:
        		>>> a = np.array([ [1,2,3], [4,5,6] ])
            	>>> arr1 = np.array(a)  # 效果等同于 np.copy(a)
                >>> arr2 = np.asarray(a)
                >>> a[1] = 10  # 结果: arr1不变化, arr2变化


np.frombuffer 用于实现动态数组
np.fromiter   从可迭代对象中建立 ndarray 对象，返回一维数组

```



## 案例：随机生成500个股票两年的交易日涨幅数据

500只股票，**两年(504天)**的涨跌幅数据，如何获取？

- 两年的交易日数量为：2 X 252 = 504
- 随机生成涨跌幅在某个正态分布内，比如均值0，方差1

股票涨跌幅数据的创建

```python
# 创建一个符合正态分布的500个股票504天的涨跌幅数据
stock_day_rise = np.random.normal(0, 1, (500, 504))
stock_day_rise.shape
```





# 打印数组

当您打印数组时，NumPy以与嵌套列表类似的方式显示它，但具有以下布局：

- 最后一个轴从左到右打印，
- 倒数第二个从上到下打印，
- 其余部分也从上到下打印，每个切片用空行分隔。

然后将一维数组打印为行，将二维数据打印为矩阵，将三维数据打印为矩数组表。

```python
>>> a = np.arange(6)                         # 1d array
>>> print(a)
[0 1 2 3 4 5]
>>>
>>> b = np.arange(12).reshape(4,3)           # 2d array
>>> print(b)
[[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
>>>
>>> c = np.arange(24).reshape(2,3,4)         # 3d array
>>> print(c)
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]
 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
```

如果数组太大而无法打印，NumPy默认会跳过数组的中心部分并仅打印角点：

```python
>>> print(np.arange(10000))
[   0    1    2 ..., 9997 9998 9999]
>>>
>>> print(np.arange(10000).reshape(100,100))
[[   0    1    2 ...,   97   98   99]
 [ 100  101  102 ...,  197  198  199]
 [ 200  201  202 ...,  297  298  299]
 ...,
 [9700 9701 9702 ..., 9797 9798 9799]
 [9800 9801 9802 ..., 9897 9898 9899]
 [9900 9901 9902 ..., 9997 9998 9999]]
```

要禁用此行为并强制NumPy打印整个数组，可以使用更改打印选项 `set_printoptions`。

```python
>>> np.set_printoptions(threshold=sys.maxsize)       # sys module should be imported
```



# 数组操作

## 算术运算

数组的算术运算符会应用到 ***元素*** 级别。

```python
>>> a = np.array( [20,30,40,50] )
>>> b = np.arange( 4 )

# 减法
>>> a-b
array([20, 29, 38, 47])

# 次方
>>> b**2
array([0, 1, 4, 9])

# 乘法、三角函数运算
>>> 10*np.sin(a)
array([ 9.12945251, -9.88031624,  7.4511316 , -2.62374854])

# 比大小
>>> a<35
array([ True, True, False, False])
```



###  `@` 运算符、`dot` 方法

与许多矩阵语言不同，乘积运算符`*`在NumPy数组中按元素进行运算。矩阵乘积可以使用 **`@` 运算符**（在python> = 3.5中）或 **`dot` 方法**

```python
>>> A = np.array( [[1,1],
...             [0,1]] )
>>> B = np.array( [[2,0],
...             [3,4]] )
>>> A * B                       # elementwise product
array([[2, 0],
       [0, 4]])
>>> A @ B                       # matrix product
array([[5, 4],
       [3, 4]])
>>> A.dot(B)                    # another matrix product
array([[5, 4],
       [3, 4]])
```



### `+=`、`-=` 操作

某些操作（例如`+=`和 `*=`）会更直接更改被操作的矩阵数组而不会创建新矩阵数组。

```python
>>> a = np.ones((2,3), dtype=int)
>>> b = np.random.random((2,3))
>>> a *= 3
>>> a
array([[3, 3, 3],
       [3, 3, 3]])
>>> b += a
>>> b
array([[ 3.417022  ,  3.72032449,  3.00011437],
       [ 3.30233257,  3.14675589,  3.09233859]])
>>> a += b                  # b is not automatically converted to integer type
Traceback (most recent call last):
  ...
TypeError: Cannot cast ufunc add output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```





## 逻辑运算

```python
tmp = np.array([ [1, 2, 3], [0.1, 0.2, 0.3] ])

# 逻辑判断
tmp > 0.5

# 取满足条件的值
tmp[tmp > 0.5]

# 替换满足条件的值
tmp[tmp > 0.5] = 1

# 通用判断
np.all(tmp > 1)	# 判断是否满足条件, 返回一个 True/False
np.unique(tmp)	# 将序列中不重复的值组成新的序列

# 更加复杂的逻辑运算
# 1. np.where（）
np.where(tmp > 0)
np.where(tmp > 0, 1, 0)	# 三元运算: tmp > 0的值替换为1, 其他替换为0
# 2. 复合逻辑需要结合 np.logical_and 和 np.logical_or 使用
np.where(np.logical_and(tmp > 0.5, tmp < 1), 1, 0)
np.where(np.logical_or(tmp > 0.5, tmp < -0.5), 1, 0)
```



## 不同类型的数组进行操作

当使用不同类型的数组进行操作时，结果数组的类型对应于更一般或更精确的数组（称为向上转换的行为）。

```python
>>> a = np.ones(3, dtype=np.int32)
>>> b = np.linspace(0,pi,3)
>>> b.dtype.name
'float64'
>>> c = a+b
>>> c
array([ 1.        ,  2.57079633,  4.14159265])
>>> c.dtype.name
'float64'
>>> d = np.exp(c*1j)
>>> d
array([ 0.54030231+0.84147098j, -0.84147098+0.54030231j,
       -0.54030231-0.84147098j])
>>> d.dtype.name
'complex128'
```



## 统计运算

许多一元操作，例如计算数组中所有元素的总和，都是作为`ndarray`类的方法实现的。

- ndarray.sum()
- ndarray.max()
- ndarray.min()
- ndarray.median()
- ndarray.mean()
- ndarray.std()  标准差
- ndarray.var()  方差variance

返回位置:

- np.argmax()
- np.argmin()



## `axis`参数指定轴

指定 `axis` 参数，可以沿数组的指定轴应用操作：

```python
>>> b = np.arange(12).reshape(3,4)
>>> b
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>>
>>> b.sum(axis=0)                            # sum of each column
array([12, 15, 18, 21])
>>>
>>> b.min(axis=1)                            # min of each row
array([0, 4, 8])
>>>
>>> b.cumsum(axis=1)                         # cumulative sum along each row
array([[ 0,  1,  3,  6],
       [ 4,  9, 15, 22],
       [ 8, 17, 27, 38]])
```

**通函数**

NumPy提供熟悉的数学函数，例如sin，cos和exp。在NumPy中，这些被称为 “通函数”（`ufunc`）。在NumPy中，这些函数在数组上按元素进行运算，产生一个数组作为输出。



## 修改数组形状

一个数组的形状是由每个轴的元素数量决定的：

```python
>>> a = np.floor(10*np.random.random((3,4)))
>>> a
array([[ 2.,  8.,  0.,  6.],
       [ 4.,  5.,  1.,  1.],
       [ 8.,  9.,  3.,  6.]])
>>> a.shape
(3, 4)

# 技巧: 自动整形, a.shape = 3, -1
```



| 函数                     | 描述                                                         |
| :----------------------- | :----------------------------------------------------------- |
| numpy.reshape( )         | 返回一个修改后的数组，不会更改原始数组. <br />对比:<br />numpy.ndarray.reshape()<br />numpy.ndarray.resize() |
| numpy.ndarray.flat       | 数组元素迭代器                                               |
| numpy.ndarray.flatten( ) | 降维, 返回一份数组拷贝                                       |
| numpy.ravel( )           | 返回展开数组，不会更改原始数组                               |
|                          |                                                              |

- **numpy.reshape( )**

**(1) numpy.reshape** 函数可以在不改变数据的条件下修改形状，格式如下： 

```python
numpy.reshape(arr, newshape, order='C')
# arr：要修改形状的数组
# newshape：整数或者整数数组，新的形状应当兼容原有形状
# order：'C' -- 按行，'F' -- 按列，'A' -- 原顺序，'K' -- 元素在内存中的出现顺序。
```

**(2) ndarray.reshape** 将 size 指定为-1，则会自动计算其他的 size 大小:

```python
# numpy.ndarray.reshape的定义:
# def reshape(self, shape, *shapes, order='C'): ...

a = np.arange(8).reshape(2, -1)
"""
[[0 1 2 3]
 [4 5 6 7]]"""
```

**(3) ndarray.resize** 方法会修改数组本身：

```python
>>> a
array([[ 2.,  8.,  0.,  6.],
       [ 4.,  5.,  1.,  1.],
       [ 8.,  9.,  3.,  6.]])
>>> a.resize((2,6))
>>> a
array([[ 2.,  8.,  0.,  6.,  4.,  5.],
       [ 1.,  1.,  8.,  9.,  3.,  6.]])
```



- **numpy.ndarray.flat**

numpy.ndarray.flat 是一个数组元素迭代器 

- **numpy.ndarray.flatten( )**

numpy.ndarray.flatten 返回一份数组拷贝，对拷贝所做的修改不会影响原始数组.

```python
a = np.arange(8).reshape(2,4)
"""
[[0 1 2 3]
 [4 5 6 7]]"""
print (a.flatten())	# [0 1 2 3 4 5 6 7]
print (a.flatten(order = 'F'))	# [0 4 1 5 2 6 3 7]
```

- **numpy.ravel( )**

numpy.ravel() 展平的数组元素，顺序通常是"C风格"，返回的是数组视图（view，有点类似 C/C++引用reference的意味），修改会影响原始数组。

```python
numpy.ravel(a, order='C')
```



## 翻转数组

| 函数               | 描述                       |
| :----------------- | :------------------------- |
| numpy.transpose( ) | 对换数组的维度             |
| numpy.ndarray.T    | 和 `self.transpose()` 相同 |
| numpy.rollaxis( )  | 向后滚动指定的轴           |
| numpy.swapaxes( )  | 对换数组的两个轴           |

- ### **numpy.transpose**、**numpy.ndarray.T**

numpy.transpose 函数用于对换数组的维度， numpy.ndarray.T 类似 numpy.transpose。

```python
numpy.transpose(arr, axes)
# arr：要操作的数组
# axes：整数列表，对应维度，通常所有维度都会对换。

a = np.arange(12).reshape(3,4)
# 转置数组:
print(np.transpose(a))
print(a.T)
```

- **numpy.rollaxis**

numpy.rollaxis 函数向后滚动特定的轴到一个特定位置，格式如下：

```python
numpy.rollaxis(arr, axis, start)
# arr：数组
# axis：要向后滚动的轴，其它轴的相对位置不会改变
# start：默认为零，表示完整的滚动。会滚动到特定位置。
```

实例

```python
# 创建了三维的 ndarray
a = np.arange(8).reshape(2,2,2)
"""
[[[0 1]
  [2 3]]

 [[4 5]
  [6 7]]]"""

# 将轴 2 滚动到轴 0（宽度到深度）
print (np.rollaxis(a,2))
"""
[[[0 2]
  [4 6]]

 [[1 3]
  [5 7]]]"""

# 将轴 0 滚动到轴 1：（宽度到高度）
print (np.rollaxis(a,2,1))
"""
[[[0 2]
  [1 3]]

 [[4 6]
  [5 7]]]"""
```



- **numpy.swapaxes**

numpy.swapaxes 函数用于交换数组的两个轴，格式如下：

```python
numpy.swapaxes(arr, axis1, axis2)
# arr：输入的数组
# axis1：对应第一个轴的整数
# axis2：对应第二个轴的整数
```

实例

```python
# 创建了三维的 ndarray
a = np.arange(8).reshape(2,2,2)
"""
[[[0 1]
  [2 3]]

 [[4 5]
  [6 7]]]"""
# 现在交换轴 0（深度方向）到轴 2（宽度方向）
print(np.swapaxes(a, 2, 0))
"""
[[[0 4]
  [2 6]]

 [[1 5]
  [3 7]]]"""
```



## 反序列化

- ndarray.tostring([order]) 或者 ndarray.tobytes([order]):   Construct Python bytes containing the raw data bytes in the array. 



## 修改数组维度

| 维度         | 描述                       |
| :----------- | :------------------------- |
| broadcast    | 产生模仿广播的对象         |
| broadcast_to | 将数组广播到新形状         |
| expand_dims  | 扩展数组的形状             |
| squeeze      | 从数组的形状中删除一维条目 |



## 连接数组

| 函数        | 描述                           |
| :---------- | :----------------------------- |
| concatenate | 连接沿现有轴的数组序列         |
| stack       | 沿着新的轴加入一系列数组。     |
| hstack      | 水平堆叠序列中的数组（列方向） |
| vstack      | 竖直堆叠序列中的数组（行方向） |



## 分割数组

| 函数     | 数组及操作                             |
| :------- | :------------------------------------- |
| `split`  | 将一个数组分割为多个子数组             |
| `hsplit` | 将一个数组水平分割为多个子数组（按列） |
| `vsplit` | 将一个数组垂直分割为多个子数组（按行） |



## 添加/删除数组元素

| 函数     | 元素及描述                               |
| :------- | :--------------------------------------- |
| `resize` | 返回指定形状的新数组                     |
| `append` | 将值添加到数组末尾                       |
| `insert` | 沿指定轴将值插入到指定下标之前           |
| `delete` | 删掉某个轴的子数组，并返回删除后的新数组 |
| `unique` | 查找数组内的唯一元素                     |



# 索引、切片和迭代

数组可以进行索引、切片和迭代操作的，就像 列表 和其他Python序列类型一样。 

ndarray 数组可以基于 0~n 的下标进行索引，切片对象可以通过内置的 slice 函数，并设置 start, stop 及 step 参数进行，从原数组中切割出一个新数组。



**多维**的数组每个轴可以有一个索引。这些索引以逗号分隔的元组给出： 

```python
>>> def f(x,y):
...     return 10*x+y
...
>>> b = np.fromfunction(f,(5,4),dtype=int)
>>> b
array([[ 0,  1,  2,  3],
       [10, 11, 12, 13],
       [20, 21, 22, 23],
       [30, 31, 32, 33],
       [40, 41, 42, 43]])
>>> b[2,3]
23
>>> b[0:5, 1]                       # each row in the second column of b
array([ 1, 11, 21, 31, 41])
>>> b[ : ,1]                        # equivalent to the previous example
array([ 1, 11, 21, 31, 41])
>>> b[1:3, : ]                      # each column in the second and third row of b
array([[10, 11, 12, 13],
       [20, 21, 22, 23]])
```

当提供的索引少于轴的数量时，缺失的索引被认为是完整的切片`冒号:` 。

```python
>>> b[-1]                                  # the last row. Equivalent to b[-1,:]
array([40, 41, 42, 43])
```



## 切片使用省略号 …

切片还可以包括省略号 **…**，来使选择元组的长度与数组的维度相同。如果在行位置使用省略号，它将返回包含行中元素的 ndarray。 

```python
a = np.array([[1,2,3],[3,4,5],[4,5,6]])
print(a[...,1])   # 第2列元素
print(a[1,...])   # 第2行元素
print(a[...,1:])  # 第2列及剩下的所有元素
```

输出结果为：

```
[2 4 5]
[3 4 5]
[[2 3]
 [4 5]
 [5 6]]
```



三个点（ `...` ）表示产生完整索引元组所需的冒号。例如，如果 `x` 是rank为的5数组（即，它具有5个轴），则：

- `x[1,2,...]` 相当于 `x[1,2,:,:,:]`，
- `x[...,3]` 等效于 `x[:,:,:,:,3]`
- `x[4,...,5,:]` 等效于 `x[4,:,:,5,:]`。

```python
>>> c = np.array( [[[  0,  1,  2],               # a 3D array (two stacked 2D arrays)
...                 [ 10, 12, 13]],
...                [[100,101,102],
...                 [110,112,113]]])
>>> c.shape
(2, 2, 3)
>>> c[1,...]                                   # same as c[1,:,:] or c[1]
array([[100, 101, 102],
       [110, 112, 113]])
>>> c[...,2]                                   # same as c[:,:,2]
array([[  2,  13],
       [102, 113]])
```





## 高级索引

### 整数数组索引（花式索引）

- **花式索引根据索引数组的值作为目标数组的某个轴的下标来取值。**

- **对于使用一维整型数组作为索引，如果目标是一维数组，那么索引的结果就是对应位置的元素；如果目标是二维数组，那么就是对应下标的行。**

- **花式索引跟切片不一样，它总是将数据复制到新数组中。**

#### 1、一维数组索引，一维数组目标

传入一维整型数组，取的是一维数组对应位置的元素，结果仍是**一维数组**。

```PYTHON
x=np.arange(12)		# [ 0  1  2  3  4  5  6  7  8  9 10 11]
print (x[[4,2,1,7]])	# [4 2 1 7]
```

#### 2、一维数组索引，二维数组目标

传入一维整型数组，取二维数组对应下标的行，结果仍是**二维数组**。

```PYTHON
x=np.arange(32).reshape((8,4))
"""
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]
 [16 17 18 19]
 [20 21 22 23]
 [24 25 26 27]
 [28 29 30 31]]
"""
# 传入顺序索引数组
print (x[[4,2,1,7]])  # 传入一个索引数组：[4,2,1,7]
"""
[[16 17 18 19]
 [ 8  9 10 11]
 [ 4  5  6  7]
 [28 29 30 31]]"""

# 传入倒序索引数组
print (x[[-3,-2,-7]])
"""
[[20 21 22 23]
 [24 25 26 27]
 [ 4  5  6  7]]"""
```

#### 3、使用`np.ix_`传入行、列数组索引

传入行索引、列索引组成的数组（**使用 `np.ix_`**），取行索引、列索引 **交叉对应** 的点，结果仍是**二维数组**。

```python
x=np.arange(32).reshape((8,4))
print (x[np.ix_([1,5,7,2],[0,3,1,2])])
"""
[[ 4  7  5  6]
 [20 23 21 22]
 [28 31 29 30]
 [ 8 11  9 10]]"""
```

查看 `np.ix_` 的定义可知:

```python
    Using `ix_` one can quickly construct index arrays that will index
    the cross product. ``a[np.ix_([1,3],[2,5])]`` returns the array
    ``[[a[1,2] a[1,5]], [a[3,2] a[3,5]]]``.
```

#### 4、使用 `np.array`传入行、列数组索引

传入行索引、列索引数组（**使用 `np.array`**），取行索引、列索引 **平行对应** 的点，结果仍是**二维数组**。

```python
# 获取 4X3 数组中的四个角的元素。 行索引是 [0,0] 和 [3,3]，列索引是 [0,2] 和 [0,2]。
x = np.arange(12).reshape((4,3))
"""
[[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]
"""
rows = np.array([[0,0],[3,3]])
cols = np.array([[0,2],[0,2]])
y = x[rows,cols]
(0,0) (0,2) (3,0) (3,2)
"""
[[ 0  2]
 [ 9 11]]
"""
```

#### 5、直接传入行、列数组索引

传入由行索引、列索引组成的二维整型数组（**不使用 `np.ix_`**），取行索引、列索引 **平行对应** 的点，结果是**一维数组**。

```python
# 获取数组中(0,0)，(1,1)和(2,0)位置处的元素
x = np.arange(12).reshape(4,3)
"""
[[ 0  1  2]
 [ 3  4  5]
 [ 6  7  8]
 [ 9 10 11]]"""

y = x[[0,1,2], [0,1,0]]
# 取的是：(0,0)、(1,1)、(2,0)三处的值
# [0 4 6]
```





### 布尔索引

可以通过一个布尔数组来索引目标数组。布尔索引通过布尔运算来获取符合指定条件的元素的数组。

 **比较运算符**

```PYTHON
# 获取大于 5 的元素
x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])  
print (x[x > 5])
# [ 6  7  8  9 10 11]
```

 **取补运算符 `~` **

```PYTHON
# 使用了 ~（取补运算符）来过滤 NaN
a = np.array([np.nan, 1, 2, np.nan])
print (a[~np.isnan(a)])
# [1. 2.]
```



#### 替换满足条件的元素项

```PYTHON
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# 1.会改变原数组
arr[arr % 2 == 1] = -1
print(arr)
# [ 0, -1,  2, -1,  4, -1,  6, -1,  8, -1]

# 2.不改变原数组
out = np.where(arr % 2 == 1, -1, arr)
print(arr)
# [0 1 2 3 4 5 6 7 8 9]
print(out)
# [ 0, -1,  2, -1,  4, -1,  6, -1,  8, -1]
```





### 字符串索引（结构化数组）





## 迭代多维数组

### 默认迭代第一个轴

对多维数组进行迭代是相对于**第一个轴**完成的：

```python
>>> for row in b:
...     print(row)
...
[0 1 2 3]
[10 11 12 13]
[20 21 22 23]
[30 31 32 33]
[40 41 42 43]
```

### 迭代数组对象的`flat`属性

但是，如果想要对数组中的每个元素执行操作，可以使用`flat`属性，该属性是数组的所有元素的[迭代器](https://docs.python.org/tutorial/classes.html#iterators)：

```python
>>> for element in b.flat:
...     print(element)
...
0
1
2
3
10
11
。。。
42
43
```

另见

[Indexing](https://www.numpy.org.cn/user/basics.indexing.html#basics-indexing), [Indexing](https://numpy.org/devdocs/reference/arrays.indexing.html#arrays-indexing) (reference), [`newaxis`](https://numpy.org/devdocs/reference/constants.html#numpy.newaxis), [`ndenumerate`](https://numpy.org/devdocs/reference/generated/numpy.ndenumerate.html#numpy.ndenumerate), [`indices`](https://numpy.org/devdocs/reference/generated/numpy.indices.html#numpy.indices)



### 迭代`np.nditer()`

- NumPy **迭代器对象 numpy.nditer** 提供了一种灵活访问一个或者多个数组元素的方式。 
-  默认是**行序优先**（row-major order，或者说是 C-order） 

```python
a = np.arange(6).reshape(2,3)
for x in np.nditer(a):
    print (x, end=", " )
# 0, 1, 2, 3, 4, 5,
```



#### 1、控制迭代顺序：order参数

- order: str，可传 'C'，'F'， 强制 nditer 对象使用某种顺序。

```PYTHON
# 行序优先
    for i in np.nditer(a):
	for i in np.nditer(a, order='C'):
    for i in np.nditer(a.T, order='C'):
    for x in np.nditer(a.T.copy(order='C')):

# 列序优先
	for i in np.nditer(a.T):	# a.T --> 转置
	for i in np.nditer(a, order='F'):
```

**注意：**

- a 和 a.T 的遍历顺序是一样的，也就是他们在内存中的存储顺序也是一样的，但是 **a.T.copy(order = 'C')** 的遍历结果是不同的，那是因为它和前两种的存储方式是不一样的，默认是按行访问。 

#### 2、允许迭代时修改元素值：op_flags参数

- op_flags: List[str]，可传'read-only'、'readwrite'、'write-only'，默认'read-only'模式。

```PYTHON
a = np.arange(0, 60, 5).reshape(3,4)
"""
[[ 0  5 10 15]
 [20 25 30 35]
 [40 45 50 55]]
"""
for i in np.nditer(a, op_flags=['readwrite']): 
    i[...]=2*i
"""
修改后的数组是
[[  0  10  20  30]
 [ 40  50  60  70]
 [ 80  90 100 110]]"""
```



#### 3、使用外部循环： flags参数

- flags: List[str]，可以接受下列值：

| 参数            | 描述                                           |
| :-------------- | :--------------------------------------------- |
| `c_index`       | 可以跟踪 C 顺序的索引                          |
| `f_index`       | 可以跟踪 Fortran 顺序的索引                    |
| `multi-index`   | 每次迭代可以跟踪一种索引类型                   |
| `external_loop` | 给出的值是具有多个值的一维数组，而不是零维数组 |

例： 迭代器遍历对应于每列，并组合为一维数组。 

```PYTHON
a = np.arange(0,60,5).reshape(3,4) 
"""
[[ 0  5 10 15]
 [20 25 30 35]
 [40 45 50 55]]
"""
for x in np.nditer(a, flags= ['external_loop'], order='F'):  
   print (x, end=", " )
"""
[ 0 20 40], [ 5 25 45], [10 30 50], [15 35 55], 
每一列得到了一个一维数组
"""
```



#### 4、广播迭代

- 如果两个数组是可广播的，nditer 组合对象能够同时迭代它们。

 假设数组 a 的维度为 3X4，数组 b 的维度为 1X4 ，则使用以下迭代器（数组 b 被广播到 a 的大小）。 

```PYTHON
a = np.arange(0,60,5).reshape(3,4) 
"""
[[ 0  5 10 15]
 [20 25 30 35]
 [40 45 50 55]]
"""
b = np.array([1,  2,  3,  4], dtype=int)
for x,y in np.nditer([a,b]):  
    print ("%d-%d"  %  (x,y), end=", " )
"""
0-1, 5-2, 10-3, 15-4, 20-1, 25-2, 30-3, 35-4, 40-1, 45-2, 50-3, 55-4,
"""
```





# 广播(Broadcast)

- 数组与数组的运算存在广播机制.

- **执行 broadcast 的前提在于，两个 ndarray 执行的是 element-wise的运算，而不是矩阵乘法的运算，矩阵乘法运算时需要维度之间严格匹配。Broadcast机制的功能是为了方便不同形状的array（numpy库的核心数据结构）进行数学运算**

  当操作两个数组时，numpy会逐个比较它们的shape（构成的元组tuple），只有在下述情况之一，两个数组才能够进行数组与数组

  - 第一种情况: **维度相等**
  - 第二种情况: **两个数组的shape元组中分别相对应的索引上的两个值相等,  或至少有一个为1**

```python
Image (3d array):  256 x 256 x 3
Scale (1d array):              3
Result (3d array): 256 x 256 x 3

A      (4d array):  9 x 1 x 7 x 1
B      (3d array):      8 x 1 x 5
Result (4d array):  9 x 8 x 7 x 5

A      (2d array):  5 x 4
B      (1d array):      1
Result (2d array):  5 x 4

A      (2d array):  15 x 3 x 5
B      (1d array):  15 x 1 x 1
Result (2d array):  15 x 3 x 5
```

如果是下面这样，则不匹配：

```python
A  (2d array):      2 x 1
B  (3d array):  8 x 4 x 3
    # 2与4: 不相等, 且没有一个1
```



# 位运算

NumPy **"bitwise_"** 开头的函数是位运算函数。

NumPy 位运算包括以下几个函数：

| 函数             | 描述                                                         |
| :--------------- | :----------------------------------------------------------- |
| `np.bitwise_and` | 对数组中整数的二进制形式执行位与运算                         |
| `np.bitwise_or`  | 对数组中整数的二进制形式执行位或运算                         |
| `np.invert`      | 按位取反                                                     |
| `np.left_shift`  | 将数组元素的二进制形式向左移动二进制表示的位，右侧附加相等数量的 0 |
| `np.right_shift` | 将数组元素的二进制形式向右移动二进制表示的位，左侧附加相等数量的 0 |

**注：**也可以使用 "&"、 "~"、 "|" 和 "^" 等操作符进行计算。



# 字符串函数

以下函数用于对 dtype 为 numpy.string_ 或 numpy.unicode_ 的数组执行向量化字符串操作。 它们基于 Python 内置库中的标准字符串函数。

这些函数在字符数组类（numpy.char）中定义。

| 函数                   | 描述                                       |
| :--------------------- | :----------------------------------------- |
| `np.char.add()`        | 对两个数组的逐个字符串元素进行连接         |
| np.char.multiply()     | 返回按元素多重连接后的字符串               |
| `np.char.center()`     | 居中字符串                                 |
| `np.char.capitalize()` | 将字符串第一个字母转换为大写               |
| `np.char.title()`      | 将字符串的每个单词的第一个字母转换为大写   |
| `np.char.lower()`      | 数组元素转换为小写                         |
| `np.char.upper()`      | 数组元素转换为大写                         |
| `np.char.split()`      | 指定分隔符对字符串进行分割，并返回数组列表 |
| `np.char.splitlines()` | 返回元素中的行列表，以换行符分割           |
| `np.char.strip()`      | 移除元素开头或者结尾处的特定字符           |
| `np.char.join()`       | 通过指定分隔符来连接数组中的元素           |
| `np.char.replace()`    | 使用新字符串替换字符串中的所有子字符串     |
| `np.char.decode()`     | 数组元素依次调用`str.decode`               |
| `np.char.encode()`     | 数组元素依次调用`str.encode`               |



# 数学函数

 NumPy 包含大量的各种数学运算的函数，包括三角函数，算术运算的函数，复数处理函数等。 

## 三角函数

- np.sin()，np.cos()，np.tan()

## 算术函数

- np.around()  四舍五入，numpy.floor() 向下取整，numpy.ceil() 向上取整 

- 加减乘除：add()，subtract()，multiply() 和 divide() 
- 倒数：numpy.reciprocal()  返回参数逐元素的倒数 
- 幂：numpy.power() 将第一个输入数组中的元素作为底数，计算它与第二个输入数组中相应元素的幂 
- 余数：numpy.mod() 计算输入数组中相应元素的相除后的余数。 函数 numpy.remainder() 也产生相同的结果 

## 统计函数

NumPy 提供了很多统计函数，用于从数组中查找最小元素，最大元素，百分位标准差和方差等。 

- np.amin() 计算数组中的元素沿指定轴的最小值。

- np.amax() 计算数组中的元素沿指定轴的最大值。
- np.ptp() 计算数组中元素最大值与最小值的差（最大值 - 最小值）。
- np.percentile()  计算百分位数 
- np.median() 函数用于计算数组 a 中元素的中位数（中值）  
- np.mean() 函数返回数组中元素的算术平均值
- np.average() 函数根据在另一个数组中给出的各自的权重计算数组中元素的加权平均值。 
- np.std() 计算标准差
- np.var() 计算方差

标准差

```
标准差是一组数据平均值分散程度的一种度量。
标准差是方差的算术平方根。
标准差公式如下：
	std = sqrt(mean((x - x.mean())**2))
如果数组是 [1，2，3，4]，则其平均值为 2.5。 因此，差的平方是 [2.25,0.25,0.25,2.25]，并且其平均值的平方根除以 4，即 sqrt(5/4) ，结果为 1.1180339887498949。
```

方差

```
统计中的方差（样本方差）是每个样本值与全体样本值的平均数之差的平方值的平均数，即 mean((x - x.mean())** 2)。
换句话说，标准差是方差的平方根。
```



# 排序、条件刷选函数

## np.sort()

 numpy.sort() 函数返回输入数组的排序副本 

```
numpy.sort(a, axis, kind, order)

a: 要排序的数组
axis: 沿着它排序数组的轴，如果没有数组会被展开，沿着最后的轴排序， axis=0 按列排序，axis=1 按行排序
kind: 默认为'quicksort'（快速排序）
order: 如果数组包含字段，则是要排序的字段
```

## np.argsort()

 numpy.argsort() 函数返回的是数组值从小到大的索引值。

## np.lexsort()

numpy.lexsort() 用于对多个序列进行排序。把它想象成对电子表格进行排序，每一列代表一个序列，排序时优先照顾靠后的列。

## msort、sort_complex、partition、argpartition

| 函数                                      | 描述                                                         |
| :---------------------------------------- | :----------------------------------------------------------- |
| msort(a)                                  | 数组按第一个轴排序，返回排序后的数组副本。np.msort(a) 相等于 np.sort(a, axis=0)。 |
| sort_complex(a)                           | 对复数按照先实部后虚部的顺序进行排序。                       |
| partition(a, kth[, axis, kind, order])    | 指定一个数，对数组进行分区                                   |
| argpartition(a, kth[, axis, kind, order]) | 可以通过关键字 kind 指定算法沿着指定轴对数组进行分区         |

## np.argmax() 和 numpy.argmin()

numpy.argmax() 和 numpy.argmin()函数分别沿给定轴返回最大和最小元素的索引。 

## np.nonzero()

numpy.nonzero() 函数返回输入数组中非零元素的索引。

## np.where() 三元运算

numpy.where() 函数返回输入数组中满足给定条件的元素的索引。 

1. np.where（）

```python
np.where(arr > 0)
np.where(arr > 0, 1, 0)	# 三元运算: tmp > 0的值替换为1, 其他替换为0
```

2. 复合逻辑需要结合 np.logical_and 和 np.logical_or 使用

```python
np.where(np.logical_and(arr > 0.5, arr < 1), 1, 0)
np.where(np.logical_or(arr > 0.5, arr < -0.5), 1, 0)
```

## np.extract()

numpy.extract() 函数根据某个条件从数组中抽取元素，返回满条件的元素。


 

# 字节交换




# 副本和视图

副本是一个数据的完整的拷贝，如果我们对副本进行修改，它不会影响到原始数据，物理内存不在同一位置。

视图是数据的一个别称或引用，通过该别称或引用亦便可访问、操作原有数据，但原有数据不会产生拷贝。如果我们对视图进行修改，它会影响到原始数据，物理内存在同一位置。

**视图一般发生在：**

- 1、numpy 的切片操作返回原数据的视图。
- 2、调用 ndarray 的 view() 函数产生一个视图。

**副本一般发生在：**

- Python 序列的切片操作，调用deepCopy()函数。
- 调用 ndarray 的 copy() 函数产生一个副本。



# 矩阵运算

 大部分机器学习算法需要用到矩阵运算

## 什么是矩阵?

矩阵，英文matrix，**矩阵必须是2维的, array可以是多维的。**

- np.mat( )
  - 将数组转换成矩阵类型
  - 默认会强制把传入的数组转换成 二维 矩阵

```python
a = np.array([[80,86],
[82,80],
[85,78],
[90,90],
[86,82],
[82,90],
[78,80],
[92,94]])  # (8, 2), 二维
b = np.array([ [0.7, 0.3] ])  # (1, 2), 二维

np.mat(a)
```



## 矩阵乘法

 **矩阵乘法必须符合下面的式子，否则运算出错.** 

```
(M行,N列) * (N行,L列) = (M行,L列)
#    N列     N行
```

- mp.matmul( )
  - 矩阵乘法
  - 默认会强制把传入的数组转换成 二维 矩阵

```python
a = np.array([[80,86],
[82,80],
[85,78],
[90,90],
[86,82],
[82,90],
[78,80],
[92,94]])
b = np.array([[0.7],[0.3]])

# (8,2) * (2, 1)
np.matmul(a, b)
```



# 线性代数

NumPy 提供了线性代数函数库 **linalg**，该库包含了线性代数所需的所有功能，可以看看下面的说明：

| 函数          | 描述                             |
| :------------ | :------------------------------- |
| `dot`         | 两个数组的点积，即元素对应相乘。 |
| `vdot`        | 两个向量的点积                   |
| `inner`       | 两个数组的内积                   |
| `matmul`      | 两个数组的矩阵积                 |
| `determinant` | 数组的行列式                     |
| `solve`       | 求解线性矩阵方程                 |
| `inv`         | 计算矩阵的乘法逆矩阵             |



# NumPy IO

```
# Numpy数据导出与导入
np.save(file, arr, allow_pickle=True, fix_imports=True)
np.savez(file, *args, **kwds)
np.load()

np.loadtxt(FILENAME, dtype=int, delimiter=' ')
np.savetxt(FILENAME, a, fmt="%d", delimiter=",")

# 非Numpy数据导入 (如导入.csv数据)
np.genfromtxt()  # 结果可能存在 nan 类型数据, 对于这类缺失值处理需要使用 Pandas, 而Numpy处理起来不方便.
```





# Numpy数据分析练习

[NumPy数据分析问答](https://www.numpy.org.cn/article/advanced/numpy_exercises_for_data_analysis.html#NumPy数据分析问答)

