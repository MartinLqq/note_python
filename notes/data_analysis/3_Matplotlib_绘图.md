#  【Matplotlib】

 专门用于开发2D图表(包括3D图表) , 实现数据可视化。

 matplotlib能够绘制**折线图、柱状图、饼图、直方图、**散点图、热力图、K线图等 



# 文档

- **Documentation** : https://matplotlib.org/contents.html
  - **User's Guide  3.1.2 ** ：https://matplotlib.org/users/index.html
  - **API Overview** : https://matplotlib.org/api/index.html
- 菜鸟教程: https://www.runoob.com/w3cnote/matplotlib-tutorial.html



# 绘图架构

matplotlib框架分为三层，这三层构成了一个栈，上层可以调用下层。 

```
Scripting(脚本) -->  Artist(美工)  -->  Backend(后端)
pyplot         -->  figure,axes,axis  -->  后端实现绘图区域
```

## 后端层

- matplotlib的底层，实现图形元素的一个个类

- 实现绘图区域 (分配画图的资源)



## 美工层

图形中所有能看到的元素都属于Artist对象，即标题、轴标签、刻度等组成图形的所有元素都是Artist对象的实例

- Figure: 指整个图形 (包括所有的元素, 如标题、线等)
- Axes(**坐标系**): 数据的绘图区域
- Axis(**坐标轴**)：坐标系中的一条轴，包含大小限制、刻度和刻度标签

特点：

- 一个figure(图)可以包含多个axes(坐标系)，但是一个axes只能属于一个figure。
- 一个axes(坐标系)可以包含多个axis(坐标轴)，包含两个即为2d坐标系，3个即为3d坐标系

## 脚本层

主要用于可视化编程，**pyplot模块** 可以提供给我们一个与matplotlib打交道的接口。可以只通过调用pyplot模块的函数从而操作整个程序包，来绘制图形。

- 操作或者改动Figure对象，例如创建Figure对象
- 大部分工作是处理样本文件的图形与坐标的生成





# Parts of a Figure

![../../_images/anatomy.png](https://matplotlib.org/_images/anatomy.png)





# 折线图与基础绘图功能

## matplotlib.pyplot模块

matplotlib.pytplot包含了一系列类似于matlab的画图函数。 它的函数 **作用于当前图形(figure)的当前坐标系(axes)**。

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(), dpi=)
    figsize:指定图的长宽
    dpi:图像的清晰度
    返回fig对象
plt.savefig(path)

```

折线图绘制与显示

```python
plt.figure(figsize=(10, 10))
plt.plot([1, 2, 3, 4, 5, 6 ,7], [17,17,18,15,11,11,13])
plt.show()
```



## 温度变化折线图

 需求：画出某城市11点到12点(1小时)内 每分钟的温度变化折线图，温度范围在15度~18度.

### 1.构造数据、显示

```python
import matplotlib.pyplot as plt
import random

# 准备画图区域
plt.figure(figsize=(20, 8), dpi=80)

# 准备x,y轴数据
x = range(60)
y_shanghai = [random.uniform(15, 18) for i in x]

# 画折线图
plt.plot(x, y_shanghai, label="上海")
plt.show()
```

### 2.自定义x,y刻度以及中文显示

- **plt.xticks(x, **kwargs)**

  x: 要显示的刻度值

- **plt.yticks(y, **kwargs)**

  y: 要显示的刻度值

```python
# 构造中文列表的字符串
x_ch = ["11点{}分".format(i) for i in x]
y_ticks = range(40)

# 修改x,y坐标的刻度
plt.xticks(x[::5], x_ch[::5])
plt.yticks(y_ticks[::5])
```

### 3.解决中文显示问题

**a. 重载配置文件**

简单可行

```python
# Windows下重载配置文件:
# plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
# plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

# Mac下重载配置文件:
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
```

**b. 修改配置文件**

matplotlib 从配置文件 matplotlibrc 中读取配置，字体相关内容也在其中。查询当前matplotlibrc 所在目录，可以用 get_configdir()函数：

```python
`import` `matplotlib``matplotlib.get_configdir()`
```

matplotlib 默认使用的 font.family 是 sans-serif，即无衬线字体，在font.sans-serif中设置的全部为西文字体，这里的设置和css样式文件中设置差不多，只需要添加系统存在的字体名称即可（需要注意的是，matplotlib只支持ttf格式的字体），设置时需要将注释符号#去除。

**c. 自定义字体**

略



### 4.标题、x轴y轴描述信息

```python
plt.xlabel("时间")
plt.ylabel("温度")
plt.title("中午11点0分到12点之间的温度变化图示")
```

### 5.多条折线, 自定义图形风格

重复调用 matplotlib.pyplot.plot 方法, 绘制多条线

```python
# 生成北京的温度
y_beijing = [random.uniform(1, 3) for i in x]

# 画折线图
plt.plot(x, y_shanghai, label="上海")
# 使用plot可以多次画多个折线
plt.plot(x, y_beijing, color='r', linestyle='--', label="北京")

# 点状图: 'bo', 更多参数见plt.plot的定义
plt.plot(x, y_beijing, 'bo', color='r', label="北京")
```



#### 格式化字符

| 字符   | 描述         |
| :----- | :----------- |
| `'-'`  | 实线样式     |
| `'--'` | 短横线样式   |
| `'-.'` | 点划线样式   |
| `':'`  | 虚线样式     |
| `'.'`  | 点标记       |
| `','`  | 像素标记     |
| `'o'`  | 圆标记       |
| `'v'`  | 倒三角标记   |
| `'^'`  | 正三角标记   |
| `'<'`  | 左三角标记   |
| `'>'`  | 右三角标记   |
| `'1'`  | 下箭头标记   |
| `'2'`  | 上箭头标记   |
| `'3'`  | 左箭头标记   |
| `'4'`  | 右箭头标记   |
| `'s'`  | 正方形标记   |
| `'p'`  | 五边形标记   |
| `'*'`  | 星形标记     |
| `'h'`  | 六边形标记 1 |
| `'H'`  | 六边形标记 2 |
| `'+'`  | 加号标记     |
| `'x'`  | X 标记       |
| `'D'`  | 菱形标记     |
| `'d'`  | 窄菱形标记   |
| `'|'`  | 竖直线标记   |
| `'_'`  | 水平线标记   |



#### 颜色的缩写

| 字符  | 颜色   |
| :---- | :----- |
| `'b'` | 蓝色   |
| `'g'` | 绿色   |
| `'r'` | 红色   |
| `'c'` | 青色   |
| `'m'` | 品红色 |
| `'y'` | 黄色   |
| `'k'` | 黑色   |
| `'w'` | 白色   |



**点状图**

要显示圆来代表点，而不是线，则使用 'ob' 作为 plot() 函数中的格式字符串。 



### 6. 图例-plt.legend

```python
# 添加图形注释
plt.legend(loc="best")

# 注释显示的内容: 前面plt.plot传入的label

```

**可选 loc**

```python
# ...\Lib\site-packages\matplotlib\legend.py
class Legend(Artist):
    """
    Place a legend on the axes at location loc.

    """
    # location string  <-->  location code
    codes = {'best':         0,  # only implemented for axes legends
             'upper right':  1,
             'upper left':   2,
             'lower left':   3,
             'lower right':  4,
             'right':        5,
             'center left':  6,
             'center right': 7,
             'lower center': 8,
             'upper center': 9,
             'center':       10,
             }
    
    ...

```



### 7.汇总(1-6)

```python
import matplotlib.pyplot as plt
import random

# 准备画图区域
plt.figure(figsize=(20, 8), dpi=80)

# 准备x,y轴数据
x = range(60)
y_shanghai = [random.uniform(15, 18) for i in x]
y_beijing = [random.uniform(1, 3) for i in x]
# 构造中文列表的字符串
x_ch = ["11点{}分".format(i) for i in x]
y_ticks = range(40)

# 画折线图
plt.plot(x, y_shanghai, label="上海")
# 使用plot可以多次画多个折线
plt.plot(x, y_beijing, color='r', linestyle='--', label="北京")

# 指定需要显示的坐标刻度(传入一个列表)
plt.xticks(x[::5], x_ch[::5])
plt.yticks(y_ticks[::5])

# 增加标题、x轴y轴描述信息
plt.xlabel('时间')
plt.ylabel('温度')
plt.title('中午11点0分到12点之间的温度变化图示')

# 图例
plt.legend(loc="best")


plt.show()

```



### 8.多坐标系-plt.subplots

将多条线显示在同一个图的不同坐标系中, 创建一个带有多个坐标系的图: 

matplotlib.pyplot.subplots(nrows=1, ncols=1, **fig_kw)

```python
Parameters:    

nrows, ncols : int, optional, default: 1, Number of rows/columns of the subplot grid.
**fig_kw : All additional keyword arguments are passed to the figure() call.

Returns:
fig : 图对象
ax : 
    设置标题等方法不同：
    set_xticks
    set_yticks
    set_xlabel
    set_ylabel
```

整体实现

```python
# 画出温度变化图,展现在不同axes里面
# 创建一个figure
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8), dpi=80)

# 准备x, y坐标的数据
x = range(60)
# y的刻度范围
y_ticks = range(40)
y_shanghai = [random.uniform(15, 18) for i in x]
y_beijing = [random.uniform(1, 3) for i in x]

# 构造中文列表的字符串
x_ch = ["11点{}分".format(i) for i in x]

# 画折线图
axes[0].plot(x, y_shanghai, label="上海")
# 使用plot可以多次画多个折线
axes[1].plot(x, y_beijing, color='r', linestyle='--', label="北京")


# 美化x,y的刻度值
# 第一个参数必须是刻度数字类型，第二个是对应着第一个数字的中文描述
axes[0].set_xticks(x[::5], x_ch[::5])
axes[0].set_yticks(y_ticks[::5])

axes[1].set_xticks(x[::5], x_ch[::5])
axes[1].set_yticks(y_ticks[::5])

# 增加x,y描述信息和标题信息
axes[0].set_xlabel("时间")
axes[0].set_ylabel("温度")

axes[1].set_xlabel("时间")
axes[1].set_ylabel("温度")

axes[0].set_title("中午11点0分到12点之间的温度变化图示")
axes[1].set_title("中午11点0分到12点之间的温度变化图示")

axes[0].legend(loc="best")
axes[1].legend(loc="best")

plt.show()
```





## 绘制正弦波

```python
import numpy as np 
import matplotlib.pyplot as plt

# 也可以不实现 plt.figure(figsize=(xx, yy), dpi=zz)

# 计算正弦曲线上点的 x 和 y 坐标
x = np.arange(0, 3 * np.pi, 0.1) 
y = np.sin(x)
plt.title("sine wave form")  
# 使用 matplotlib 来绘制点
plt.plot(x, y) 
plt.show()
```



## plt.subplot()

subplot() 函数允许你在同一图中绘制不同的东西。 

![img](https://www.runoob.com/wp-content/uploads/2018/10/sub_plot.jpg)

```python
import numpy as np
import matplotlib.pyplot as plt

# 计算正弦和余弦曲线上的点的 x 和 y 坐标 
x = np.arange(0, 3 * np.pi, 0.1) 
y_sin = np.sin(x)
y_cos = np.cos(x)

# 建立 subplot 网格，高为 2，宽为 1
# 激活第一个 subplot, 绘制第一个图像
plt.subplot(2, 1, 1)
plt.plot(x, y_sin)
plt.title('Sine')

# 激活第二个 subplot，并绘制第二个图像
plt.subplot(2, 1, 2) 
plt.plot(x, y_cos) 
plt.title('Cosine')

# 展示图像
plt.show()
```



## K线图

```
matplotlib.finance.candlestick_ochl(ax, quotes, width=0.2, colorup='k', colordown='r')
```







# 柱状图-Bar

## matplotlib.pyplot.bar

```python
# Lib\site-packages\matplotlib\axes\_axes.py
class Axes(_AxesBase):
    ...
    
    @docstring.dedent_interpd
    def bar(self, x, height, width=0.8, bottom=None, *, align="center",
            **kwargs):
        r"""
        Make a bar plot.

        The bars are positioned at *x* with the given *align*\ment. Their
        dimensions are given by *width* and *height*. The vertical baseline
        is *bottom* (default 0).

        Each of *x*, *height*, *width*, and *bottom* may either be a scalar
        applying to all bars, or it may be a sequence of length N providing a
        separate value for each bar.

        Parameters
        ----------
        x : sequence of scalars
            The x coordinates of the bars. See also *align* for the
            alignment of the bars to the coordinates.

        height : scalar or sequence of scalars
            The height(s) of the bars.

        width : scalar or array-like, optional
            The width(s) of the bars (default: 0.8).

        bottom : scalar or array-like, optional
            The y coordinate(s) of the bars bases (default: 0).

        align : {'center', 'edge'}, optional, default: 'center'
            Alignment of the bars to the *x* coordinates:

            - 'center': Center the base on the *x* positions.
            - 'edge': Align the left edges of the bars with the *x* positions.

            To align the bars on the right edge pass a negative *width* and
            ``align='edge'``.

        Returns
        -------
        container : `.BarContainer`
            Container with all the bars and optionally errorbars.

        Other Parameters
        ----------------
        color : scalar or array-like, optional
            The colors of the bar faces.

        edgecolor : scalar or array-like, optional
            The colors of the bar edges.

        linewidth : scalar or array-like, optional
            Width of the bar edge(s). If 0, don't draw edges.

        tick_label : string or array-like, optional
            The tick labels of the bars.
            Default: None (Use default numeric labels.)

        xerr, yerr : scalar or array-like of shape(N,) or shape(2,N), optional
            If not *None*, add horizontal / vertical errorbars to the bar tips.
            The values are +/- sizes relative to the data:

            - scalar: symmetric +/- values for all bars
            - shape(N,): symmetric +/- values for each bar
            - shape(2,N): Separate - and + values for each bar. First row
                contains the lower errors, the second row contains the
                upper errors.
            - *None*: No errorbar. (Default)

            See :doc:`/gallery/statistics/errorbar_features`
            for an example on the usage of ``xerr`` and ``yerr``.

        ecolor : scalar or array-like, optional, default: 'black'
            The line color of the errorbars.

        capsize : scalar, optional
           The length of the error bar caps in points.
           Default: None, which will take the value from
           :rc:`errorbar.capsize`.

        error_kw : dict, optional
            Dictionary of kwargs to be passed to the `~.Axes.errorbar`
            method. Values of *ecolor* or *capsize* defined here take
            precedence over the independent kwargs.

        log : bool, optional, default: False
            If *True*, set the y-axis to be log scale.

        orientation : {'vertical',  'horizontal'}, optional
            *This is for internal use only.* Please use `barh` for
            horizontal bar plots. Default: 'vertical'.

        See also
        --------
        barh: Plot a horizontal bar plot.

        Notes
        -----
        The optional arguments *color*, *edgecolor*, *linewidth*,
        *xerr*, and *yerr* can be either scalars or sequences of
        length equal to the number of bars.  This enables you to use
        bar as the basis for stacked bar charts, or candlestick plots.
        Detail: *xerr* and *yerr* are passed directly to
        :meth:`errorbar`, so they can also have shape 2xN for
        independent specification of lower and upper errors.

        Other optional kwargs:

        %(Rectangle)s

        """
```



## 对比一项

**对比电影的票房收入**

数据

```
['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴', '降魔传','追捕','七十七天','密战','狂兽','其它']
[73853,57767,22354,15969,14839,8725,8716,8318,7916,6764,52222]
```

代码

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

plt.figure(figsize=(20, 8), dpi=80)

# prepare data
moves = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴', '降魔传','追捕','七十七天','密战','狂兽','其它']
x_axis = range(len(moves))
y_axis = [73853,57767,22354,15969,14839,8725,8716,8318,7916,6764,52222]
color = ['b','r','g','y','c','m','y','k','c','g','g']

plt.bar(x_axis, y_axis, width=0.4, color=color)

# 修改x轴的labels
plt.xticks(ticks=x_axis, labels=moves)

plt.show()
```



## 分类对比多项

 对比不同电影首日和首周的票房:

- 添加首日首周两部分的柱状图
- 调整 x轴中文坐标位置

数据

```python
movie_name = ['雷神3：诸神黄昏','正义联盟','寻梦环游记']

first_day = [10587.6,10062.5,1275.7]
first_weekend=[36224.9,34479.6,11830]
```

代码

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

# 三部电影的首日和首周票房对比
plt.figure(figsize=(20, 8), dpi=60)

movie_name = ['雷神3：诸神黄昏','正义联盟','寻梦环游记']

first_day = [10587.6, 10062.5, 1275.7]
first_weekend=[36224.9, 34479.6, 11830]

x = range(len(movie_name))

width = 0.2
plt.bar(x, first_day, width=width, label="首日票房")
# 首周柱状图显示的位置在首日的位置右边
plt.bar([i+width for i in x], first_weekend, width=width, label="首周票房")

# 显示X轴中文，固定在首日和首周的中间位置
plt.xticks([i+width/2 for i in x], movie_name)
plt.legend(loc='best')
plt.show()
```





# 直方图-Histogram

即:  **频数分布直方图**,  

- 组数：在统计数据时，我们把数据按照不同的范围分成几个组，分成的组的个数称为组数
- 组距：每一组两个端点的差

极差 = max - min

组数 = 极差/组距



## matplotlib.pyplot.hist

```python
# Lib\site-packages\matplotlib\axes\_axes.py
class Axes(_AxesBase):
    ...
	@_preprocess_data(replace_names=["x", 'weights'], label_namer="x")
    def hist(
        self,
        x,
        bins=None,
        range=None,
        density=None,
        weights=None,
        cumulative=False,
        bottom=None,
        histtype='bar',
        align='mid',
        orientation='vertical',
        rwidth=None,
        log=False,
        color=None,
        label=None,
        stacked=False,
        normed=None,
        **kwargs
    ):

       """
        Plot a histogram.

        Compute and draw the histogram of *x*. The return value is a
        tuple (*n*, *bins*, *patches*) or ([*n0*, *n1*, ...], *bins*,
        [*patches0*, *patches1*,...]) if the input contains multiple
        data.

        Multiple data can be provided via *x* as a list of datasets
        of potentially different length ([*x0*, *x1*, ...]), or as
        a 2-D ndarray in which each column is a dataset.  Note that
        the ndarray form is transposed relative to the list form.

        Masked arrays are not supported at present.
		
		部分参数:
            x : (n,) array or sequence of (n,) arrays
            bins : integer or sequence or ‘auto’, optional, 组距
            density : bool, optional, 以频率显示或者以頻数显示, 默认頻数, 值1为频率

        Returns
        -------
        n : array or list of arrays
            The values of the histogram bins. See *normed* or *density*
            and *weights* for a description of the possible semantics.
            If input *x* is an array, then this is an array of length
            *nbins*. If input is a sequence arrays
            ``[data1, data2,..]``, then this is a list of arrays with
            the values of the histograms for each of the arrays in the
            same order.

        bins : array
            The edges of the bins. Length nbins + 1 (nbins left edges and right
            edge of last bin).  Always a single array even when multiple data
            sets are passed in.

        patches : list or list of lists
            Silent list of individual patches used to create the histogram
            or list of such list if multiple input datasets.

```



## 电影时长分布直方图

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

# 展现不同电影的时长分布状态
plt.figure(figsize=(20, 8), dpi=100)

# 准备时长数据
time =[131,  98, 125, 131, 124, 139, 131, 117, 128, 108, 135, 138, 131, 102, 107, 114, 119, 128, 121, 142, 127, 130, 124, 101, 110, 116, 117, 110, 128, 128, 115,  99, 136, 126, 134,  95, 138, 117, 111,78, 132, 124, 113, 150, 110, 117,  86,  95, 144, 105, 126, 130,126, 130, 126, 116, 123, 106, 112, 138, 123,  86, 101,  99, 136,123, 117, 119, 105, 137, 123, 128, 125, 104, 109, 134, 125, 127,105, 120, 107, 129, 116, 108, 132, 103, 136, 118, 102, 120, 114,105, 115, 132, 145, 119, 121, 112, 139, 125, 138, 109, 132, 134,156, 106, 117, 127, 144, 139, 139, 119, 140,  83, 110, 102,123,107, 143, 115, 136, 118, 139, 123, 112, 118, 125, 109, 119, 133,112, 114, 122, 109, 106, 123, 116, 131, 127, 115, 118, 112, 135,115, 146, 137, 116, 103, 144,  83, 123, 111, 110, 111, 100, 154,136, 100, 118, 119, 133, 134, 106, 129, 126, 110, 111, 109, 141,120, 117, 106, 149, 122, 122, 110, 118, 127, 121, 114, 125, 126,114, 140, 103, 130, 141, 117, 106, 114, 121, 114, 133, 137,  92,121, 112, 146,  97, 137, 105,  98, 117, 112,  81,  97, 139, 113,134, 106, 144, 110, 137, 137, 111, 104, 117, 100, 111, 101, 110,105, 129, 137, 112, 120, 113, 133, 112,  83,  94, 146, 133, 101,131, 116, 111,  84, 137, 115, 122, 106, 144, 109, 123, 116, 111,111, 133, 150]
# 定义一个间隔大小
mid = 2

# 得出组数
bins = int((max(time) - min(time)) / mid)

# 画出直方图
plt.hist(
    time,      # y轴数值列表
    bins,      # 组数
    density=1  # density布尔值为True, 则纵坐标显示频率; 反之显示数量.
)

# 指定刻度的范围，以及步长
ticks = range(min(time), max(time))
ticks = list(ticks)[::mid]  # 步长为mid=2
plt.xticks(ticks=ticks)

plt.xlabel("电影时长大小")
plt.ylabel("电影的数据量")

plt.grid(True, linestyle='--', alpha=0.5)	# alpha: 透明度

plt.show()
```





## 正态分布图

```python
import numpy as np
import matplotlib.pyplot as plt

mu = 0 # mean
sigma = 0.1  # standard deviation
s = np.random.normal(mu, sigma, 1000)

# Verify the mean and the variance:
ver_mean = abs(mu - np.mean(s)) < 0.01
print(ver_mean)
ver_variance = abs(sigma - np.std(s, ddof=1)) < 0.01
print(ver_variance)

# 画直方图
count, bins, ignored = plt.hist(s, 30, density=True)
# 画折线图
plt.plot(
    bins,
    1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
    linewidth=2,
    color='r'
)
plt.show()
```





# 饼图-Pie

- 分类的占比情况（不超过9个分类）



## matplotlib.pyplot.pie

```python
# Lib\site-packages\matplotlib\axes\_axes.py
class Axes(_AxesBase):
    ...
    
	@_preprocess_data(replace_names=["x", "explode", "labels", "colors"],
                      label_namer=None)
    def pie(self, x, explode=None, labels=None, colors=None,
            autopct=None, pctdistance=0.6, shadow=False, labeldistance=1.1,
            startangle=None, radius=None, counterclock=True,
            wedgeprops=None, textprops=None, center=(0, 0),
            frame=False, rotatelabels=False):
        """
        Plot a pie chart.

        Make a pie chart of array *x*.  The fractional area of each wedge is
        given by ``x/sum(x)``.  If ``sum(x) < 1``, then the values of *x* give
        the fractional area directly and the array will not be normalized. The
        resulting pie will have an empty wedge of size ``1 - sum(x)``.

        The wedges are plotted counterclockwise, by default starting from the
        x-axis.
        
        部分参数:
            x : array-like. The wedge sizes.
            labels : list, optional, default: None
                A sequence of strings providing the labels for each wedge
            colors : array-like, optional, default: None
                A sequence of matplotlib color args through which the pie chart
                will cycle.  If *None*, will use the colors in the currently
                active cycle.
            autopct : None (default), string, or function, optional
                If not *None*, is a string or function used to label the wedges
                with their numeric value.  The label will be placed inside the
                wedge.  If it is a format string, the label will be ``fmt%pct``.
                If it is a function, it will be called.

        Notes
        -----
        The pie chart will probably look best if the figure and axes are
        square, or the Axes aspect is equal.
        This method sets the aspect ratio of the axis to "equal".
        The axes aspect ratio can be controlled with `Axes.set_aspect`.
        """
```





## 显示不同的电影的排片占比

数据

```python
movie_name = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴','降魔传','追捕','七十七天','密战','狂兽','其它']

place_count = [60605,54546,45819,28243,13270,9945,7679,6799,6101,4621,20105]
```

代码

```python
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

# 展现不同电影的时长分布状态
plt.figure(figsize=(20, 8), dpi=100)

# 准备数据
movies = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴','降魔传','追捕','七十七天','密战','狂兽','其它']
counts = [60605,54546,45819,28243,13270,9945,7679,6799,6101,4621,20105]
colors = [
    # colors data: site-packages\matplotlib\_color_data.py
    '#acc2d9',  # cloudy blue
    '#56ae57',  # dark pastel green
    '#b2996e',  # dust
    '#a8ff04',  # electric lime
    '#69d84f',  # fresh green
    '#894585',  # light eggplant
    '#70b23f',  # nasty green
    '#d4ffff',  # really light blue
]

x_axis = range(len(movies))
plt.pie(
    counts,                  # 坐标值列表
    labels=movies,           # 设置每个扇形区域的 label
    colors=colors,           # 设置每个扇形区域的颜色
    autopct='%.2f%%',        # 显示百分比(百分比会自动计算)
    explode=[0.1] + [0]*10   # 破裂效果
)

# 重要: 指定显示的pie是正圆
plt.axis('equal')

plt.legend(loc='upper right')
plt.title('排片占比示意图')

plt.show()

```

## plt.axis()

.....\Lib\site-packages\matplotlib\axes\_base.py

```python
class _AxesBase(martist.Artist):
    ...
    
    def axis(self, *v, **kwargs):
        """
        Convenience method to get or set some axis properties.

        Call signatures::

          xmin, xmax, ymin, ymax = axis()
          xmin, xmax, ymin, ymax = axis(list_arg)
          xmin, xmax, ymin, ymax = axis(string_arg)
          xmin, xmax, ymin, ymax = axis(**kwargs)

        Parameters
        ----------
        v : List[float] or one of the strings listed below.
            Optional positional-only argument

            If a list, set the axis data limits.  If a string:

            ======== ==========================================================
            Value    Description
            ======== ==========================================================
            'on'     Turn on axis lines and labels.
            'off'    Turn off axis lines and labels.
            'equal'  Set equal scaling (i.e., make circles circular) by
                     changing axis limits.
            'scaled' Set equal scaling (i.e., make circles circular) by
                     changing dimensions of the plot box.
            'tight'  Set limits just large enough to show all data.
            'auto'   Automatic scaling (fill plot box with data).
            'normal' Same as 'auto'; deprecated.
            'image'  'scaled' with axis limits equal to data limits.
            'square' Square plot; similar to 'scaled', but initially forcing
                     ``xmax-xmin = ymax-ymin``.
            ======== ==========================================================

        emit : bool, optional
            Passed to set_{x,y}lim functions, if observers are notified of axis
            limit change.

        xmin, ymin, xmax, ymax : float, optional
            The axis limits to be set.

        Returns
        -------
        xmin, xmax, ymin, ymax : float
            The axis limits.

        See also
        --------
        matplotlib.axes.Axes.set_xlim
        matplotlib.axes.Axes.set_ylim
        """
    ...
```









# 其它功能

更多画图功能

https://matplotlib.org/gallery/index.html



## 添加图的注释-annotate或text

```python
fig, ax = plt.subplots(nrows=1, ncols=1, dpi=80)

# 使用splines以及设置颜色，将上方和右方的坐标去除
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# 将刻度设置为空，去除刻度
plt.xticks([])
plt.yticks([])

# x,y数据
data = np.ones(100)
data[70:] = list(range(1, 31))
print(data)

# 使用annptate添加注释
plt.annotate(
    '这是一个拐点',
    xy=(70, 1), # 箭头指向位置
    arrowprops=dict(arrowstyle='->'),#自定义箭头样式 
    xytext=(50, 10))# 文本位置

plt.plot(data)

plt.xlabel('1')
plt.ylabel('2')

# 使用 text 添加注释
ax.text(
    30, 2,# 文本位置
    '这是一段文本')
```

## 动画matplotlib.animation

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

# 设置x,y数据，显示到图形当中
x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


def init():
    """
    初始设置
    """
    line.set_ydata([np.nan] * len(x))
    return line,


def animate(i):
    """
    更新坐标点函数
    """
    line.set_ydata(np.sin(x + i / 100))
    return line,


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=2, blit=True, save_count=50)

plt.show()
```

