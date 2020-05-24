# sympy

sympy是一个Python的科学计算库，用一套强大的符号计算体系完成诸如多项式求值、求极限、解方程、求积分、微分方程、级数展开、矩阵运算等等计算问题。

- 虽然Matlab的类似科学计算能力也很强大，但是Python以其语法简单、易上手、异常丰富的三方库生态，可以更优雅地解决日常遇到的各种计算问题.

# 资源

- Python科学计算利器——SymPy库:  https://www.jianshu.com/p/339c91ae9f41
- python学习园:  http://liao.cpython.org

# 安装sympy库

```
pip install sympy
```

# 常用的sympy内置符号

### 虚数单位i

```css
In [13]: import sympy

In [14]: sympy.I
Out[14]: I

In [15]: sympy.I ** 2
Out[15]: -1

# 求-1的平方根
In [16]: sympy.sqrt(-1)
Out[16]: I
```

### 自然对数的底e

```css
In [18]: sympy.E
Out[18]: E

# 求对数
In [20]: sympy.log(sympy.E)
Out[20]: 1
```

### 无穷大oo

```undefined
In [26]: 1/sympy.oo
Out[26]: 0

In [27]: 1 + sympy.oo
Out[27]: oo
```

### 圆周率pi

```cpp
In [60]: sympy.pi
Out[60]: pi

In [61]: sympy.sin(sympy.pi/2)
Out[61]: 1
```

# 用sympy进行初等运算

Python 2.x中用除号`/`做两个整数的除法，实际上是整除运算，为了防止这种情况的发生，避免不必要的麻烦，下文的所有示例一开始都加上一句：`from __future__ import division`，这个时候除号`/`本身就变成了真实除法，而`//`才是整除，比如：

```csharp
# 导入division包之前
In [1]: 1/2
Out[1]: 0

In [2]: from __future__ import division

# 导入division包之后
In [3]: 1/2
Out[3]: 0.5

In [4]: 1//2
Out[4]: 0
```

### 求对数

```css
# 自然对数
In [10]: sympy.log(sympy.E)
Out[10]: 1

In [11]: sympy.log(sympy.E ** 3)
Out[11]: 3

# 以10为底1000的对数
In [12]: sympy.log(1000,10)
Out[12]: 3
```

### 求平方根

```css
In [13]: sympy.sqrt(4)
Out[13]: 2

In [14]: sympy.sqrt(-1)
Out[14]: I
```

### 求n次方根

```css
# 求8的3次方根
In [15]: sympy.root(8,3)
Out[15]: 2
```

### 求k次方

```undefined
In [21]: 2 ** 3
Out[21]: 8

In [22]: 16 ** (1/2)
Out[22]: 4.0
```

### 求阶乘

```css
In [35]:  sympy.factorial(4)
Out[35]: 24
```

### 求三角函数

```cpp
In [86]: sympy.sin(sympy.pi)
Out[86]: 0

In [87]: sympy.sin(sympy.pi/2)
Out[87]: 1
```

# 表达式与表达式求值

sympy可以用一套符号系统来表示一个表达式，如函数、多项式等，并且可以进行求值，比如：

```bash
# 首先定义x为一个符号，表示一个变量
In [96]: x = sympy.Symbol('x')

In [97]: fx = 2*x + 1

# 可以看到fx是一个sympy.core.add.Add类型的对象，也就是一个表达式
In [98]: type(fx)
Out[98]: sympy.core.add.Add

# 用evalf函数，传入变量的值，对表达式进行求值
In [101]: fx.evalf(subs={x:2})
Out[101]: 5.00000000000000
```

还支持多元表达式：

```bash
In [102]: x,y = sympy.symbols('x y')

In [103]: f = 2 * x + y

# 以字典的形式传入多个变量的值
In [104]: f.evalf(subs = {x:1,y:2})
Out[104]: 4.00000000000000

# 如果只传入一个变量的值，则原本输出原来的表达式
In [105]: f.evalf(subs = {x:1})
Out[105]: 2.0*x + y
```

# 用sympy解方程（组）

使用`sympy.solve`函数解方程，该函数通常传入两个参数，第1个参数是方程的表达式（把方程所有的项移到等号的同一边形成的式子），第2个参数是方程中的未知数。函数的返回值是一个列表，代表方程的所有根（可能为复数根）。

### 解最简单的方程

比如下面我们来求两个方程：

```bash
# 首先定义 `x`为一个符号，代表一个未知数
In [24]: x = sympy.Symbol('x')

# 解方程：x - 1 = 0
In [25]: sympy.solve(x - 1,x)
Out[25]: [1]

# 解方程：x ^ 2 - 1 = 0
In [26]: sympy.solve(x ** 2 - 1,x)
Out[26]: [-1, 1]

# 解方程：x ^ 2 + 1 = 0
In [27]: sympy.solve(x ** 2 + 1,x)
Out[27]: [-I, I]
```

### 把函数式赋给一个变量

有时候为了书写起来简洁，可以把一个函数式起个名字，比如：

```dart
In [30]: x = sympy.Symbol('x')

In [31]: f = x + 1

In [32]: sympy.solve(f,x)
Out[32]: [-1]
```

### 解方程组

比如要解这么个二元一次方程组：

![img](https:////upload-images.jianshu.io/upload_images/8819542-72c7beb45226ccf9.png?imageMogr2/auto-orient/strip|imageView2/2/w/157/format/webp)

代码如下：

```bash
# 一次性定义多个符号
In [28]: x,y = sympy.symbols('x y')

In [29]: sympy.solve([x + y - 1,x - y -3],[x,y])
Out[29]: {x: 2, y: -1}
```

# 计算求和式

计算求和式可以使用`sympy.summation`函数，其函数原型为：`sympy.summation(f, *symbols, **kwargs)`。

话不多少，举个栗子，比如求下面这个求和式子的值：
 

![img](https:////upload-images.jianshu.io/upload_images/8819542-e779aa77893798bd.png?imageMogr2/auto-orient/strip|imageView2/2/w/114/format/webp)

下面用代码来求：

```dart
In [37]: n = sympy.Symbol('n')

In [38]: sympy.summation(2 * n,(n,1,100))
Out[38]: 10100
```

可见结果是正确的。

如果`sympy.summation`函数无法计算出具体的结果，那么会返回求和表达式。

# 解带有求和式的方程

比如求这么一个方程：

![img](https:////upload-images.jianshu.io/upload_images/8819542-b7b391f37657a927.png?imageMogr2/auto-orient/strip|imageView2/2/w/232/format/webp)

代码如下：

```dart
In [43]: x = sympy.Symbol('x')

In [44]: i = sympy.Symbol('i',integer = True)

In [46]: f =  sympy.summation(x,(i,1,5)) + 10 * x - 15

In [47]: sympy.solve(f,x)
Out[47]: [1]
```

# 求极限

求极限用`sympy.limit`函数，其函数文档如下：

```csharp
Signature: sympy.limit(e, z, z0, dir='+')
Docstring:
Compute the limit of e(z) at the point z0.

z0 can be any expression, including oo and -oo.

For dir="+" (default) it calculates the limit from the right
(z->z0+) and for dir="-" the limit from the left (z->z0-).  For infinite
z0 (oo or -oo), the dir argument is determined from the direction
of the infinity (i.e., dir="-" for oo).
```

函数文档中已经说得很清楚了，下面用代码示例来求几个极限。

如果学过微积分，就会知道微积分中有3个重要的极限：

![img](https:////upload-images.jianshu.io/upload_images/8819542-184b70faf3c1275b.png?imageMogr2/auto-orient/strip|imageView2/2/w/171/format/webp)

![img](https:////upload-images.jianshu.io/upload_images/8819542-ee5d3990a0dc59ae.png?imageMogr2/auto-orient/strip|imageView2/2/w/220/format/webp)

![img](https:////upload-images.jianshu.io/upload_images/8819542-feb0fef92aa4cd0b.png?imageMogr2/auto-orient/strip|imageView2/2/w/224/format/webp)

下面就用`sympy.limit`函数来分别求这3个极限：

```cpp
In [53]: x = sympy.Symbol('x')

In [54]: f1 = sympy.sin(x)/x

In [55]: sympy.limit(f1,x,0)
Out[55]: 1

In [56]: f2 = (1+x)**(1/x)

In [57]: sympy.limit(f2,x,0)
Out[57]: E

In [58]: f3 = (1+1/x)**x

In [59]: sympy.limit(f3,x,sympy.oo)
Out[59]: E
```

可见三个极限的计算结果都完全正确。

# 求导

求导使用`sympy.diff`函数，传入2个参数：函数表达式和变量名，举例如下：

```cpp
In [63]: x = sympy.Symbol('x')

In [64]: f = x ** 2 + 2 * x + 1

In [65]: sympy.diff(f,x)
Out[65]: 2*x + 2

In [66]: f2 = sympy.sin(x)

In [67]: sympy.diff(f2,x)
Out[67]: cos(x)

# 多元函数求偏导
In [68]: y = sympy.Symbol('y')

In [70]: f3 = x**2 + 2*x + y**3

In [71]: sympy.diff(f3,x)
Out[71]: 2*x + 2

In [72]: sympy.diff(f3,y)
Out[72]: 3*y**2
```

# 求定积分

使用`sympy.integrate`函数求定积分，其功能比较复杂，非常强大，下面仅仅举几个比较简单的例子。

先来求一个最简单的积分：

![img](https:////upload-images.jianshu.io/upload_images/8819542-aabc41f9bfe28f1d.png?imageMogr2/auto-orient/strip|imageView2/2/w/121/format/webp)


 用可以立马口算出上面这个式子的结果是1，用代码计算如下：

```bash
n [74]: x = sympy.Symbol('x')

n [75]: f = 2 * x

# 传入函数表达式和积分变量、积分下限、上限
n [76]: sympy.integrate(f,(x,0,1))
ut[76]: 1
```

下面来算一个复杂一点的多重积分：

![img](https:////upload-images.jianshu.io/upload_images/8819542-fed1bbd18cde1427.png?imageMogr2/auto-orient/strip|imageView2/2/w/138/format/webp)

其中：

![img](https:////upload-images.jianshu.io/upload_images/8819542-7de76f6e53c71ec7.png?imageMogr2/auto-orient/strip|imageView2/2/w/208/format/webp)

我们通过口算可以求出`f(x)`：

![img](https:////upload-images.jianshu.io/upload_images/8819542-95c54a9c5647a7ca.png?imageMogr2/auto-orient/strip|imageView2/2/w/280/format/webp)

所以：

![img](https:////upload-images.jianshu.io/upload_images/8819542-77ea58537b677f66.png?imageMogr2/auto-orient/strip|imageView2/2/w/460/format/webp)

下面用代码来计算上述过程：

```bash
In [82]: t,x = sympy.symbols('t x')

In [83]: f = 2 * t

In [84]: g = sympy.integrate(f,(t,0,x))

In [85]: sympy.integrate(g,(x,0,3))
Out[85]: 9
```

# 求不定积分

同样也是使用`sympy.integrate`函数求不定积分，下面仅仅举几个比较简单的例子。

比如求下面这个不定积分：

![img](https:////upload-images.jianshu.io/upload_images/8819542-cd7eb2ff2d91a49e.png?imageMogr2/auto-orient/strip|imageView2/2/w/199/format/webp)

通过观察我们知道它的结果是：

![img](https:////upload-images.jianshu.io/upload_images/8819542-b1268da5b014caed.png?imageMogr2/auto-orient/strip|imageView2/2/w/109/format/webp)

下面用代码来计算这个不定积分的结果：

```cpp
In [79]: x = sympy.Symbol('x')

In [80]: f = sympy.E ** x + 2 * x

In [81]: sympy.integrate(f,x)
Out[81]: x**2 + exp(x)
```

# 总结

从上面的一系列计算可以看出，sympy是个非常强大的科学计算库，本文所讲到的用法仅仅是它强大功能的冰山一角，还需以后在实际使用中进一步发掘。