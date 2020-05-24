# 【Pandas】

- **以Numpy为基础，借力Numpy模块在计算方面性能高的优势**
- **基于matplotlib，能够简便的画图**
- **独特的数据结构**

- 适用的数据类型：
  - 与 SQL 或 Excel 表类似的，含异构列的表格数据;
  - 有序和无序（非固定频率）的时间序列数据;
  - 带行列标签的矩阵数据，包括同构或异构型数据;
  - 任意其它形式的观测、统计数据集, 数据转入 Pandas 数据结构时不必事先标记

- Pandas 的主要数据结构是 [Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)（一维数据）与 [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)（二维数据），这两种数据结构足以处理金融、统计、社会科学、工程等领域里的大多数典型用例。

- 部分优势 ：
  - 处理浮点与非浮点数据里的**缺失数据**，表示为 `NaN`；
  - 大小可变：**插入或删除** DataFrame 等多维对象的列；
  - 自动、显式**数据对齐**：显式地将对象与一组标签对齐，也可以忽略标签，在 Series、DataFrame 计算时自动与数据对齐；
  - 强大、灵活的**分组**（group by）功能：**拆分-应用-组合**数据集，聚合、转换数据；
  - 把 Python 和 NumPy 数据结构里不规则、不同索引的数据**轻松**地转换为 DataFrame 对象；
  - 基于智能标签，对大型数据集进行**切片**、**花式索引**、**子集分解**等操作；
  - 直观地**合并（merge）**、**连接（join）**数据集；
  - 灵活地**重塑（reshape）**、**透视（pivot）**数据集；
  - **轴**支持结构化标签：一个刻度支持多个标签；
  - 成熟的 IO 工具：读取**文本文件**（CSV 等支持分隔符的文件）、Excel 文件、数据库等来源的数据，利用超快的 **HDF5** 格式保存 / 加载数据；
  - **时间序列**：支持日期范围生成、频率转换、移动窗口统计、移动窗口线性回归、日期位移等时间序列功能。

- Pandas的重要性

对于数据的处理，如果没有pandas，那么可能python就在数据挖掘/机器学习领域领域落后于R

**那么在说大数据可能我们可能会听过Hadoop和Spark，它们的有时是基于集群的云端处理数据，如果数据只有几GB，甚至1~2TB，那么pandas也是处理数据的最好选择**





# 文档

- Pandas中文快速入门：https://www.pypandas.cn/docs/getting_started/
- 0.25.3:  https://pandas.pydata.org/pandas-docs/stable/index.html
- 数据集资源:  Machine Learning Repository    https://archive.ics.uci.edu/ml/datasets.php
- Pandas常用知识点总结:  https://blog.csdn.net/wangpei1949/article/details/80472000

B站视频:   https://www.bilibili.com/video/av6785636?from=search&seid=15880205862713615709





# 数据结构

## 三大数据结构

Pandas有三大数据结构，Series、DataFrame以及Panel。

- **Series(一维数据)**
- **DataFrame(二维数据)**
- Panel(三维结构数据/面板数据)

> 对于Panel，会很少使用，通常会使用使用MultiIndex这种结构解决三维数据表示问题 



## Series

> series结构只有行索引,  一维结构.

通过已有数据创建

- 指定内容，默认索引

```python
pd.Series(np.arange(10))
```

- 指定索引

```python
pd.Series([6.7,5.6,3,10,2], index=)
```

通过字典数据创建

```python
pd.Series({'red':100, ''blue':200, 'green': 500, 'yellow':1000})
```

series获取属性和值

- index
- values



## DataFrame

```python
# 随机生成500个股票两年的交易日涨幅数据
stock = np.random.normal(0, 1, (500, 504))
# 使用Pandas中的数据结构
stock_df = pd.DataFrame(stock)
print(stock_df)
```

DataFrame对象既有行索引，又有列索引

- 行索引，表明不同行，横向索引，叫index，0轴，axis=0
- 列索引，表名不同列，纵向索引，叫columns，1轴，axis=1



### 自定义行列索引

1. 自定义行索引

```python
# 构造行索引序列
index = ['股票' + str(i) for i in range(stock.shape[0])]
# 自定义行索引
stock_df = pd.DataFrame(stock, index=index)
```

2. 自定义列索引

股票的日期是一个时间的序列，我们要实现从前往后的时间还要考虑每月的总天数等，不方便。

使用 **pd.date_range()：用于生成一组连续的时间序列**

```python
pd.date_range(
	start=None,  # 开始时间
	end=None,  # 结束时间
	periods=None,  # 时间天数
	freq='B',  # 递进单位，默认1天,'B'默认略过周末
	...
)
```

实现自定义列索引

```python
# 生成一个时间的序列，略过周末非交易日
columns = pd.date_range(
    start='2017-01-01',
    periods=stock.shape[1],
    freq='B'    # 先只考虑略过周末，不考虑节日
)
# index代表行索引，columns代表列索引
data = pd.DataFrame(stock, index=index, columns=columns)
```



### 修改行列索引

- 修改行列索引值

```python
# 只能通过整体修改，不能单个赋值
data.index = [i for i in range(500)]

# 错误方式(无法修改)
data.index[499] = "0000001.SH"
```

- 重设索引 - df.reset_index()

```python
# df.reset_index()把原来的索引删除, 或把原来的索引设置为一列值(行索引自动为'index'), 以从0开始的整数作为新索引.
data.reset_index(drop=True)  # drop=True -- 删除
```

- 以某列值设置为新的索引 - df.set_index()

```python
df = pd.DataFrame({'month':[1,4,7,10], 'year':[1, 1, 2, 2], 'sale':[55, 40, 84, 31]})
# 设置新的索引值，但是返回一个新的dataframe
df = df.set_index(['month'])
# 设置多重索引 MultiIndex的结构
df.set_index(['year', df.index])

# 打印df的索引
df.index   # MultiIndex
```

> 注：通过刚才的设置，DataFrame就变成了一个具有 MutiIndex 的DataFrame。



### DatatFrame的属性

- shape
- dtypes
- ndim
- **index**
- **columns**
- **values**
- **T**

还有一些方便整体查询的属性

- head(5)
- tail(5)









# 基本数据操作

```python
data = pd.read_csv(r".\stock_day.csv")
```

![stock_data_picture](C:\Users\Administrator\Desktop\Learning-Notes\notes\data_analysis\images\stock_data_picture.jpg)



## 索引取值

Numpy使用索引选取序列和切片选择，pandas也支持类似的操作.  

pandas的 DataFrame 的获取有三种形式:

1. **直接按名称取值，甚至组合列名、行名使用。 ( 先列后行 )**
   - A. 直接传 行列名/行列名列表:    `data['open'][['2018-02-27']]`  (先列后行)
   - B. df.loc[ ]:    `df.loc['2018-02-27':'2018-02-22', 'open']`  (先行后列)

2. **按下标取值**
   - `data.iloc[0:100, 0:2]`  (先行后列)
   - **注**:  在numpy中,  直接支持同时传两个切片,  在pandas中需要用 df.iloc 才支持

3. **下标和名称组合做引**
   - `data[['open', 'high']][0:10]`   (先列后行)
   - `data.ix[0:10, ['open', 'close']]`   (先行后列)  (不推荐)



- **1、直接按名称取值，甚至组合列名、行名使用。 ( 先列后行 )**

  ```python
  # 注意: 先列后行
  --------------------------------------------
  >>> data['open'][['2018-02-27']]    # Return: Series
  2018-02-27    23.53
  Name: open, dtype: float64
  --------------------------------------------
  >>> data['open'][['2018-02-28', '2018-02-27', '2018-02-26']]    # Return: Series
  2018-02-28      NaN     # `行索引`不存在时返回 NaN
  2018-02-27    23.53
  2018-02-26    22.80
  Name: open, dtype: float64
  --------------------------------------------
  >>> data['open']['2018-02-27']    # Return: 标量值
  23.53
  --------------------------------------------
  >>> data['open'][0]    # Series支持整数值索引, 但DataFrame行/列通过行名/列名索引
  23.53
  --------------------------------------------
  >>> data['open']
  2018-02-27    23.53
  ...
  2015-03-02    12.25
  Name: open, Length: 643, dtype: float64
  --------------------------------------------
  # 支持
  >>> data[['open', 'close']]    # Return: DataFrame
  >>> data[['open', 'close']]['open']
  >>> data[0:10]    # 注意是切片行, 不是切片列!  不支持data[0]
  
  # 不支持
  >>> data[['open', 'close']][0]  # 报错原因: DataFrame索引是`先列后行`, 行通过行名索引.
  >>> data[0]
  ```

- **2、按下标取值:  df.iloc**

- https://www.pypandas.cn/docs/getting_started/10min.html#选择

  ```python
  # 使用 iloc 可以通过索引的下标去获取
  # 注意:  第一个切片为行切片,  第二个切片为列切片  (传索引: 先行后列)
  data.iloc[0:100, 0:2].head()
  ```

- **3、组合索引:   df.ix**

  ```python
  # 使用 ix 进行下标和名称组合做引
  data.ix[0:10, ['open', 'close']]
  # 不推荐使用df.ix,  因为效果相当于
  data[['close', 'open', 'high']][0:3]
  ```



**不支持的操作**

```python
# 不支持
data[['2018-02-27']]['open']
# 不支持
data[:1, :2]    # 支持data[]
```



**获取Dataframe对象的列内容, 还可以通过属性调用的方式:**

```python
data['open'] 相当于 data.open
```



## 修改内容

```python
# 直接修改原来的值
data['close'] = 1
# 或者
data.close = 1
```



## 排序

- df.sort_values():   默认是从小到大,  可以对单个键或多个键进行排序

  ```python
  # 按照涨跌幅大小进行排序 , 使用ascending指定按照大小排序
  data = data.sort_values(by='p_change', ascending=False)
  
  # 按照过个键进行排序
  data = data.sort_values(by=['open', 'high'])
  ```

- df.sort_index():  对索引进行排序

  ```python
  # 对索引进行排序
  data.sort_index()
  ```

## 去重

```
df.drop_duplicates()
```



# 统计分析

## 1、基本统计分析

综合分析

- describe:  综合统计,  计算平均值、标准差、最大值、最小值、分位数

单个函数分析

- max:  最大值计算
- min:  最小值计算
- mean:  平均值计算
- std:  标准差计算
-  var:  方差计算
- idxmin:  最小值的索引
- idxmax:  最小值的索引

对于单个函数去进行统计的时候，坐标轴还是按照这些默认“index” (axis=0, default), “columns” (axis=1)指定

```python
# 单独计算
data['close'].max()

# 对所有的列进行计算
data.max(0)
# 对所有的行进行计算
data.max(1)

# 求出最大值的位置
data.idxmax(axis=0)

# 求出最小值的位置
data.idxmin(axis=0)
```



## 2、累计统计分析

- cumsum	计算前1/2/3/…/n个数的和
- cummax	计算前1/2/3/…/n个数的最大值
- cummin	计算前1/2/3/…/n个数的最小值
- cumprod	计算前1/2/3/…/n个数的积

以上这些函数可以对 series 和 dataframe 操作

```python
# 排序之后，进行累计求和
data = data.sort_index()

#计算累计函数
stock_rise = data['p_change']

stock_rise.cumsum()
```



**如何让这个连续求和的结果更好的显示呢？**

如果要使用plot函数，需要导入matplotlib

```python
import matplotlib.pyplot as plt
# plot方法集成了前面直方图、条形图、饼图、折线图
stock_rise.cumsum().plot()
plt.show()
```





# 逻辑与算术运算

## 1、逻辑运算符<、>

```python
# 进行逻辑判断
# 用true false进行标记，逻辑判断的结果可以作为筛选的依据
data[data['p_change'] > 2]
```

## 2、使用|、&完成复合的逻辑

```python
# 完成一个符合逻辑判断， p_change > 2, open > 15
data[(data['p_change'] > 2) & (data['open'] > 15)]
```

### df.query(query_str)

pandas提供了一个非常方便的函数供逻辑判断

query_str:  逻辑判断的字符串

```python
data.query("p_change > 2 & open > 15")   # 复合逻辑
data.query("p_change > turnover")        # 跨列比较
```



## 3、isin()

```python
# 可以指定值进行一个判断，从而进行筛选操作
data[data['turnover'].isin([4.19])]
data.head(10)
```

## 4、数学运算 add(), sub()

**如果想要得到每天的涨跌大小？**

```python
# 进行数学运算 加上具体的一个数字
data['open'].add(1)

# 求出每天 close- open价格差
# 筛选两列数据
close = data['close']
open1 = data['open']
# 默认按照索引对齐
data['m_price_change'] = close.sub(open1)
```

## 5、使用apply() 传入自定义运算函数

```python
# 进行apply函数运算
data[['open', 'close']].apply(lambda x: x.max() - x.min(), axis=0)
data[['open', 'close']].apply(lambda x: x.max() - x.min(), axis=1)
```





# IO操作

pandas的API支持众多的文件格式，如CSV、SQL、XLS、JSON、HDF5。

最常用的是 HDF5 和 CSV 文件



## 汇总

| Format Type | Data Description                                             | Reader                                                       | Writer                                                       |
| :---------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| text        | [CSV](https://en.wikipedia.org/wiki/Comma-separated_values)  | [read_csv](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-csv-table) | [to_csv](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-store-in-csv) |
| text        | [JSON](https://www.json.org/)                                | [read_json](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-json-reader) | [to_json](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-json-writer) |
| text        | [HTML](https://en.wikipedia.org/wiki/HTML)                   | [read_html](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-html) | [to_html](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-html) |
| text        | Local clipboard                                              | [read_clipboard](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-clipboard) | [to_clipboard](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-clipboard) |
| binary      | [MS Excel](https://en.wikipedia.org/wiki/Microsoft_Excel)    | [read_excel](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-excel-reader) | [to_excel](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-excel-writer) |
| binary      | [OpenDocument](http://www.opendocumentformat.org/)           | [read_excel](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-ods) |                                                              |
| binary      | [HDF5 Format](https://support.hdfgroup.org/HDF5/whatishdf5.html) | [read_hdf](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5) | [to_hdf](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5) |
| binary      | [Feather Format](https://github.com/wesm/feather)            | [read_feather](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-feather) | [to_feather](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-feather) |
| binary      | [Parquet Format](https://parquet.apache.org/)                | [read_parquet](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-parquet) | [to_parquet](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-parquet) |
| binary      | [Msgpack](https://msgpack.org/index.html)                    | [read_msgpack](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-msgpack) | [to_msgpack](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-msgpack) |
| binary      | [Stata](https://en.wikipedia.org/wiki/Stata)                 | [read_stata](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-stata-reader) | [to_stata](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-stata-writer) |
| binary      | [SAS](https://en.wikipedia.org/wiki/SAS_(software))          | [read_sas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sas-reader) |                                                              |
| binary      | [Python Pickle Format](https://docs.python.org/3/library/pickle.html) | [read_pickle](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-pickle) | [to_pickle](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-pickle) |
| SQL         | [SQL](https://en.wikipedia.org/wiki/SQL)                     | [read_sql](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql) | [to_sql](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql) |
| SQL         | [Google Big Query](https://en.wikipedia.org/wiki/BigQuery)   | [read_gbq](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-bigquery) | [to_gbq](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-bigquery) |

## read_csv与to_csv

- pandas.read_csv(filepath_or_buffer, sep =',' , delimiter = None)
  - filepath_or_buffer:文件路径
  - usecols:指定读取的列名，列表形式
- DataFrame.to_csv(path_or_buf=None, sep=', ’, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None)
  - path_or_buf :string or file handle, default None
  - sep :character, default ‘,’
  - columns :sequence, optional
  - mode:'w'：重写, 'a' 追加
  - index:是否写进行索引
  - header :boolean or list of string, default True,  是否写进列索引值

```python
# 读
data = pd.read_csv("./data/stock_day.csv", usecols=['open', 'close'])
# 写
data[:10].to_csv("./data/test.csv", columns=['open'], index=False, mode='a', header=False)   # header=False:  不写列名
```



## read_hdf与to_hdf

- pandas.read_hdf(path_or_buf，key =None，** kwargs)

  从h5文件当中读取数据

  - path_or_buffer:文件路径
  - key: 读取的键
  - mode: 打开文件的模式:  ['r', 'r+', 'a']
  - return: Theselected object

```python
close = pd.read_hdf("./data/test_day_close.h5")
a = close[['000001.SZ', '000002.SZ']]
a.to_hdf("./data/test.h5", key="x")
b = pd.read_hdf("./data/test.h5", key="x")

# 如果提示找不到tables模块: ImportError: HDFStore requires PyTables...
!conda install -n [env_name] pytables
```



**优先选择使用hdf文件存储**

速度快,  空间小,  跨平台

- hdf存储支持压缩，**使用的方式是blosc，是速度最快**的也是pandas默认支持的
- 使用压缩可以**提高磁盘利用率，节省空间**
- **hdf跨平台**，可以轻松迁移到hadoop 上面



h5可以方便存储三维数据,   一个h5文件可以放多个key,  来存储三维结构.





# 缺失值处理

## Pandas缺失值类型

1. NaN
2. 不是缺失值nan，有默认标记的,  如 '?' .

```python
movie = pd.read_csv("./data/IMDB-Movie-Data.csv")
```

## pd.isnull 判断是否有NaN

```python
pd.isnull(movie)    # 返回DataFrame
pd.notnull(movie)   # 返回DataFrame
```

## df.dropna 删除缺失值

```python
# 使用dropna的前提是，缺失值的类型必须是np.nan
movie.dropna(axis='rows')

按行删除缺失值, 因为列是需要的数据
```

## df.fillna 填充缺失值

```python
# 替换存在缺失值的样本
# 替换？, 填充平均值，中位数
movie['Revenue (Millions)'].fillna(movie['Revenue (Millions)'].mean(), inplace=True)
# inplace=True ---> 直接修改原DataFrame
movie['Metascore'].fillna(movie['Metascore'].mean(), inplace=True)
```

## df.replace 替换数据

不是缺失值nan，有默认标记的,  如 "?" 号,   先替换 "?" 为np.nan,  再进行缺失值的处理.

```python
wis = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data")
# df.replace(to_replace=, value=)
# 把一些其它值标记的缺失值，替换成np.nan
wis = wis.replace(to_replace='?', value=np.nan)
wis.dropna()

# 替换DataFrame中指定字符串
df.replace({"2003-05-10": "2008-08-08"}, regex=True, inplace=True)
```





# 数据离散化

## 什么是数据的离散化 ?

**连续属性的离散化就是将连续属性的值域上，将值域划分为若干个离散的区间，最后用不同的符号或整数** **值代表落在每个子区间中的属性值。**

离散化有很多种方法，这使用一种最简单的方式去操作

- 原始人的身高数据：165，174，160，180，159，163，192，184
- 假设按照身高分几个区间段：150~165, 165~180,180~195

这样我们将数据分到了三个区间段，我可以对应的标记为矮、中、高三个类别，最终要处理成一个"哑变量"矩阵



**股票的涨跌幅离散化**

验证涨跌幅变化是否符合正态分布

```python
data = pd.read_csv("./data/stock_day.csv")
p_change= data['p_change']
p_change.hist(bins=80)
plt.show()
```



## 将数据进行分组

**将股票涨跌幅数据进行分组**

```
(1.106, 1.57]      67    # 区间、个数
(7.198, 10.03]     65
(3.662, 5.11]      65
(0.332, 0.73]      65
(-0.001, 0.332]    65
(2.802, 3.662]     64
(1.57, 2.1]        64
(5.11, 7.198]      63
(0.73, 1.106]      63
(2.1, 2.802]       62
Name: p_change, dtype: int64
```

- pd.qcut：对数据进行分组
  - 将数据分组 一般会value_counts搭配使用，统计每组的个数
- series.value_counts()：统计分组次数

```python
# 自行分组
qcut = pd.qcut(np.abs(p_change), 10)
qcut.value_counts()
```

## 自定义区间分组

- pd.cut(data, bins)

```python
# 自己指定分组区间
bins = [-100, -7, -5, -3, 0, 3, 5, 7, 100]
p_counts = pd.cut(p_change, bins)
p_counts.value_counts()
"""
(0, 3]        215
(-3, 0]       188
(3, 5]         57
(-5, -3]       51
(7, 100]       35
(5, 7]         35
(-100, -7]     34
(-7, -5]       28
Name: p_change, dtype: int64
"""
```

## 哑变量矩阵

**股票涨跌幅分组数据变成 哑变量矩阵**

```python
dummaries = pd.get_dummies(p_counts, prefix="rise")
```

|            | rise_(-100, -7] | rise_(-7, -5] | rise_(-5, -3] | rise_(-3, 0] | rise_(0, 3] | rise_(3, 5] | rise_(5, 7] | rise_(7, 100] |
| ---------: | --------------: | ------------: | ------------: | -----------: | ----------: | ----------: | ----------: | :------------ |
| 2018-02-27 |               0 |             0 |             0 |            0 |           1 |           0 |           0 | 0             |
| 2018-02-26 |               0 |             0 |             0 |            0 |           0 |           1 |           0 | 0             |
| 2018-02-23 |               0 |             0 |             0 |            0 |           1 |           0 |           0 | 0             |
| 2018-02-22 |               0 |             0 |             0 |            0 |           1 |           0 |           0 | 0             |
|        ... |             ... |           ... |           ... |          ... |         ... |         ... |         ... | ...           |



# 合并

## pd.concat()

```python
def concat(objs, axis=0, join='outer', join_axes=None, ignore_index=False,
           keys=None, levels=None, names=None, verify_integrity=False,
           sort=None, copy=True):
    ...
```

 例如将上面处理好的哑变量与原数据合并 

```python
pd.concat([data, dummaries], axis=1)
```



## pd.merge()

```python
def merge(left, right, how='inner', on=None, left_on=None, right_on=None,
          left_index=False, right_index=False, sort=False,
          suffixes=('_x', '_y'), copy=True, indicator=False,
          validate=None):
          ...

"""
可以指定按照两组数据的共同键值对合并或者左右各自
left: A DataFrame object
right: Another DataFrame object
on: Columns (names) to join on. Must be found in both the left and right DataFrame objects.
left_on=None, right_on=None：指定左右键
"""
```

| Merge method | SQL Join Name      | Description                               |
| ------------ | ------------------ | ----------------------------------------- |
| `left`       | `LEFT OUTER JOIN`  | Use keys from left frame only             |
| `right`      | `RIGHT OUTER JOIN` | Use keys from right frame only            |
| `outer`      | `FULL OUTER JOIN`  | Use union of keys from both frames        |
| `inner`      | `INNER JOIN`       | Use intersection of keys from both frames |



例1

```python
left = pd.DataFrame({'ky1': ['K0', 'K0', 'K1', 'K2'],
                        'ky2': ['K0', 'K1', 'K0', 'K1'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']})
"""
	A	B	ky1	ky2
0	A0	B0	K0	K0
1	A1	B1	K0	K1
2	A2	B2	K1	K0
3	A3	B3	K2	K1
"""
right = pd.DataFrame({'ky1': ['K0', 'K1', 'K1', 'K2'],
                        'ky2': ['K0', 'K0', 'K0', 'K0'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']})
"""
	C	D	ky1	ky2
0	C0	D0	K0	K0
1	C1	D1	K1	K0
2	C2	D2	K1	K0
3	C3	D3	K2	K0
"""
# 默认内连接
result = pd.merge(left, right, on=['ky1', 'ky2'])
"""
    A	B	ky1	ky2	C	D
0	A0	B0	K0	K0	C0	D0
1	A2	B2	K1	K0	C1	D1
2	A2	B2	K1	K0	C2	D2
"""


# 左连接
result = pd.merge(left, right, how='left', on=['ky1', 'ky2'])
"""
    A	B	ky1	ky2	C	D
0	A0	B0	K0	K0	C0	D0
1	A1	B1	K0	K1	NaN	NaN
2	A2	B2	K1	K0	C1	D1
3	A2	B2	K1	K0	C2	D2
4	A3	B3	K2	K1	NaN	NaN
"""


# 右连接
result = pd.merge(left, right, how='right', on=['ky1', 'ky2'])
"""
	A	B	ky1	ky2	C	D
0	A0	B0	K0	K0	C0	D0
1	A2	B2	K1	K0	C1	D1
2	A2	B2	K1	K0	C2	D2
3	NaN	NaN	K2	K0	C3	D3
"""


# 外链接
result = pd.merge(left, right, how='outer', on=['ky1', 'ky2'])
"""
    A	B	ky1	ky2	C	D
0	A0	B0	K0	K0	C0	D0
1	A1	B1	K0	K1	NaN	NaN
2	A2	B2	K1	K0	C1	D1
3	A2	B2	K1	K0	C2	D2
4	A3	B3	K2	K1	NaN	NaN
5	NaN	NaN	K2	K0	C3	D3
"""
```





# 交叉表与透视表

# 分组与聚合





























