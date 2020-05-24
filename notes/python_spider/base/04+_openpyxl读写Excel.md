# Python使用openpyxl读写excel文件

by @[sunhaiyu](https://www.cnblogs.com/sun-haiyu/p/7096423.html)

2017.6.29

这是一个第三方库，可以处理`xlsx`格式的Excel文件。`pip install openpyxl`安装。如果使用Aanconda，应该自带了。

## 1 读取Excel文件

需要导入相关函数。

```python
from openpyxl import load_workbook

# 默认可读写，若有需要可以指定write_only和read_only为True
wb = load_workbook('mainbuilding33.xlsx')
```

默认打开的文件为可读写，若有需要可以指定参数`read_only`为`True`。

### 获取工作表--Sheet

```python
# 获得所有sheet的名称
wb.sheetnames
wb.get_sheet_names()

# 根据sheet名字获得sheet
a_sheet = wb.get_sheet_by_name('Sheet1')
a_sheet = wb['Sheet1']

# 获得当前正在显示的sheet, 也可以用wb.get_active_sheet()
active_sheet = wb.active 

# 获得sheet名
a_sheet.title
```

### 获取单元格

```python
# 获取某个单元格的值，观察excel发现也是先字母再数字的顺序，即先列再行
b4 = sheet['B4']
# 分别返回
print(f'({b4.column}, {b4.row}) is {b4.value}')  # 返回的数字就是int型

# 除了用下标的方式获得，还可以用cell函数, 换成数字，这个表示B4
b4_too = sheet.cell(row=4, column=2)
print(b4_too.value)
```

`b4.column`返回`B`, `b4.row`返回4, value则是那个单元格的值。

另外cell还有一个属性`coordinate`, 像b4这个单元格返回的是坐标`B4`。

### 获得最大行和最大列

```python
# 获得最大列和最大行
print(sheet.max_row)
print(sheet.max_column)
```

### 获取行和列

- `sheet.rows`为生成器, 里面是每一行的数据，每一行又由一个tuple包裹。
- `sheet.columns`类似，不过里面是每个tuple是每一列的单元格。

```python
# 因为按行，所以返回A1, B1, C1这样的顺序
for row in sheet.rows:
    for cell in row:
        print(cell.value)

# A1, A2, A3这样的顺序
for column in sheet.columns:
    for cell in column:
        print(cell.value)
```

上面的代码就可以获得所有单元格的数据。如果要获得某行的数据呢？

给其一个索引就行了，**因为sheet.rows是生成器类型，不能使用索引，转换成list之后再使用索引**，

`list(sheet.rows)[2]`这样就获取到第三行的tuple对象。

```python
for cell in list(sheet.rows)[2]:
    print(cell.value)
```

如何获得任意区间的单元格？

可以使用`range`函数，下面的写法，获得了以A1为左上角，B3为右下角矩形区域的所有单元格。**注意range从1开始的，因为在openpyxl中为了和Excel中的表达方式一致，并不和编程语言的习惯以0表示第一个值。**

```python
for i in range(1, 4):
    for j in range(1, 3):
        print(sheet.cell(row=i, column=j))
        
# out
<Cell mainbuilding33.A1>
<Cell mainbuilding33.B1>
<Cell mainbuilding33.A2>
<Cell mainbuilding33.B2>
<Cell mainbuilding33.A3>
<Cell mainbuilding33.B3>
```

还可以像使用切片那样使用。`sheet['A1':'B3']`返回一个tuple，该元组内部还是元组，由每行的单元格构成一个元组。

```python
for row_cell in sheet['A1':'B3']:
    for cell in row_cell:
        print(cell)
        

for cell in sheet['A1':'B3']:
    print(cell)

# out
(<Cell mainbuilding33.A1>, <Cell mainbuilding33.B1>)
(<Cell mainbuilding33.A2>, <Cell mainbuilding33.B2>)
(<Cell mainbuilding33.A3>, <Cell mainbuilding33.B3>)
```

### 根据字母获得列号，根据列号返回字母

需要导入， 这两个函数存在于`openpyxl.utils`

```python
from openpyxl.utils import get_column_letter, column_index_from_string

# 根据列的数字返回字母
print(get_column_letter(2))  # B
# 根据字母返回列的数字
print(column_index_from_string('D'))  # 4
```



## 2 将数据写入Excel

### 工作表相关

需要导入`WorkBook`

```python
from openpyxl import Workbook

wb = Workbook()
```

这样就新建了一个新的工作表（只是还没被保存）。

若要指定**只写模式**，可以指定参数`write_only=True`。一般默认的可写可读模式就可以了。

```python
print(wb.get_sheet_names())  # 提供一个默认名叫Sheet的表，office2016下新建提供默认Sheet1
# 直接赋值就可以改工作表的名称
sheet.title = 'Sheet1'
# 新建一个工作表，可以指定索引，适当安排其在工作簿中的位置
wb.create_sheet('Data', index=1)  # 被安排到第二个工作表，index=0就是第一个位置

# 删除某个工作表
wb.remove(sheet)
del wb[sheet]
```

### 写入单元格

还可以使用公式哦

```python
# 直接给单元格赋值就行
sheet['A1'] = 'good'
# B9处写入平均值
sheet['B9'] = '=AVERAGE(B2:B8)'
```

**但是如果是读取的时候需要加上data_only=True这样读到B9返回的就是数字，如果不加这个参数，返回的将是公式本身'=AVERAGE(B2:B8)'**

#### append函数

可以一次添加多行数据，从第一行空白行开始（下面都是空白行）写入。

```python
# 添加一行
row = [1 ,2, 3, 4, 5]
sheet.append(row)

# 添加多行
rows = [
    ['Number', 'data1', 'data2'],
    [2, 40, 30],
    [3, 40, 25],
    [4, 50, 30],
    [5, 30, 10],
    [6, 25, 5],
    [7, 50, 10],
]
```

由于`append`函数只能**按行写入**。如果我们想按列写入呢。append能实现需求么？如果把上面的列表嵌套看作矩阵。只要将矩阵转置就可以了。使用`zip()`函数可以实现，不过内部的列表变成了元组就是了。都是可迭代对象，不影响。

```python
list(zip(*rows))

# out
[('Number', 2, 3, 4, 5, 6, 7),
 ('data1', 40, 40, 50, 30, 25, 50),
 ('data2', 30, 25, 30, 10, 5, 10)]
```

解释下上面的`list(zip(*rows))`

首先`*rows`将列表打散，相当于填入了若干个参数，

`zip`从某个列表中提取第1个值组合成一个tuple，再从每个列表中提取第2个值组合成一个tuple，一直到**最短列表**的最后一个值提取完毕后结束，更长列表的之后的值被舍弃，换句话，**最后的元组个数是由原来每个参数（可迭代对象）的最短长度决定的。**比如现在随便删掉一个值，最短列表长度为2，data2那一列（竖着看）的值全部被舍弃。

```python
for i in list(zip(*rows)):
    sheet.append(list(i))
wb.save('example.xlsx')
```

### 保存文件

所有的操作结束后，一定记得保存文件。指定路径和文件名，后缀名为`xlsx`。

```python
wb.save(r'D:\example.xlsx')
```



## 3 设置单元格风格--Style

先导入需要的类`from openpyxl.styles import Font, colors, Alignment`

分别可指定字体相关，颜色，和对齐方式。

### 字体

```python
bold_itatic_24_font = Font(name='等线', size=24, italic=True, color=colors.RED, bold=True)

sheet['A1'].font = bold_itatic_24_font
```

上面的代码指定了等线24号加粗斜体，字体颜色红色。直接使用cell的`font`属性，将Font对象赋值给它。

### 对齐方式

也是直接使用cell的属性`aligment`，这里指定垂直居中和水平居中。除了center，还可以使用`right、left`等等参数。

```python
# 设置B1中的数据垂直居中和水平居中
sheet['B1'].alignment = Alignment(horizontal='center', vertical='center')
```

### 设置行高和列宽

有时候数据太长显示不完，就需要拉长拉高单元格。

```python
# 第2行行高
sheet.row_dimensions[2].height = 40
# C列列宽
sheet.column_dimensions['C'].width = 30
```

### 合并和拆分单元格

所谓合并单元格，即以合并区域的左上角的那个单元格为基准，覆盖其他单元格使之称为一个大的单元格。

相反，拆分单元格后将这个大单元格的值返回到原来的左上角位置。

```python
# 合并单元格， 往左上角写入数据即可
sheet.merge_cells('B1:G1') # 合并一行中的几个单元格
sheet.merge_cells('A1:C3') # 合并一个矩形区域中的单元格
```

**合并后只可以往左上角写入数据，也就是区间中:左边的坐标。**

如果这些要合并的单元格都有数据，只会保留左上角的数据，其他则丢弃。换句话说**若合并前不是在左上角写入数据，合并后单元格中不会有数据。**

以下是拆分单元格的代码。拆分后，值回到A1位置。

```python
sheet.unmerge_cells('A1:C3')
```







# 在Scrapy中的pipelines.py中保存数据成`xlsx`格式

```python
from openpyxl import Workbook

class TuniuPipeline(object): 

	def open_spider(self, spider):
        self.wb = Workbook()        # 实例化一个文件
        self.ws = self.wb.active	# 实例化一个工作簿
        self.ws.append(['music_name', 'auth_name', 'publis_time', 'class'])  # 设置表头


    def process_item(self, item, spider):  
        data = [item['music_name'], item['auth_name'], item['publis_time'], item['class']]  
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        
        return item
    
    def close_spider(self, spider):
        self.wb.save('music_info.xlsx')  # 保存xlsx文件
```



