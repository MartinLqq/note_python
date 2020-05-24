# Pycharm使用技巧

## Shortcuts

### help

```
搜索action:		Ctrl + Shift + A
快速预览Docstring:	Ctrl + Q (在函数/类的开头处，使用三个引号包含的函数文档即DocString)
在当前页面展示类或者函数的源代码:	Ctrl + shift + I
```

### 文本操作

```
自动规范化代码: 		Ctrl + Alt + L
替换: 				Ctrl + R
复制光标所在行/所选内容:	Ctrl + D
删除光标所在行/所选内容:	Ctrl + X
注释光标所在行:		  Ctrl + /
选中光标前/后所有内容:	Ctrl + Shift + Home/End
选中光标所在行的前/后内容:	Shift + Home/End
选中整个单词:			Ctrl + Shift + ←/→
同时选择与当前选中内容(或光标所在位置单词) 一致的所有文本:
	Ctrl + Shift + Alt + J

以单词为一个单位, 向右增加光标选中的内容:	Ctrl + W  (Ctrl+Shift+W, 减少)
大小写转换(测试效果):	Ctrl + Shift + U

搜索文本/文件:
	Shift + Shift
	Ctrl + Shift + F
	Ctrl + Shift
搜索时过滤:
	在使用 Find in Path 时可以过滤搜索内容,
	1. 勾选 File mask
	2. 输入 !xxx, 表示过滤指定字符串内容, 支持正则表达式
	如 !test* 可以test文件过滤掉
	
替换:	
	Ctrl + Shift + R
	Ctrl + R
从历史记录中选择文本复制:		Ctrl + Shift + V

光标选中方法/函数/类的()内, 查看参数信息:	Ctrl + P

缩进:			Tab
取消缩进:	   Shift + Tab

单击放置多个光标:		Ctrl + 鼠标左键
移动放置多个光标:		Alt + 鼠标左键

上下移动光标所在行内容:	Alt + Shift + ↑/↓
```

### 文件级操作

```
文件内容比较:			Ctrl + D,  先选中一个文件, 再Ctrl+D, 选择另一个文件
查找用到当前选中内容的文件:
	Alt + F7
	Dtrl + Alt + F7
复制光标所在文件的路径:	Ctrl + Shift + C
复制文件:			F5
安全删除文件:		   Alt + Del
关闭当前标签:			Ctrl + F4
```

### 快速定位

#### 常用定位

```
跳到光标上一个位置: 		Alt + 左方向键, 代码跳转时非常有用
跳到光标下一个位置: 		Alt + 右方向键, 代码跳转时非常有用

跳到光标所在行首:		Home
跳到光标所在行末:		End
跳到当前文档最首:		Ctrl + Home
跳到当前文档最末:		Ctrl + End
向上跳一页:			Pgup
向下跳一页:			Pgdn
```

#### 快速定位到错误行

```
快速定位到错误行 (pycharm 波浪线提示)
     F2
     Shift+F2 
```

#### 快速查看最近的修改

```
快速查看最近的修改:		Alt + Shift + C
```

#### 使用书签，快速定位

在看框架的源代码时，最常使用的是 `Ctrl` + `鼠标左键` 一层一层地往里深入，但是当源代码比较多，可能一整个事件过程涉及十几文件，函数调用错综复杂，对于一个庞大的项目来说，有用的可能就几个关键函数，每次要找到这几个函数，都要重头从源函数再一层一层的找下去，比较麻烦.

可以设置 Pycharm书签, 快速定位

```
创建书签
	Ctrl + F11	可用 数字/字母 标记书签, 如果设置为数字, 可以 Ctrl+数字 直接跳到书签所在行
	F11			直接创建不带数字/字母的书签
获取书签列表		Shift + F11
删除书签		  F11
```

#### 精准定位

```
精准定位到文件:	Ctrl + Shift + N
精准定位到类:		Ctrl + N
精准定位到符号(Symbol)：
	类的所有成员（函数、变量等）都可以称之为符号
	Ctrl + Alt + Shift + N
精准定位到当前文件的结构：
	文件结构包括类、函数、变量
	Ctrl + F12
精准定位到某行:	Ctrl + G

快速定位 TODO/FIXME 注释:	  Alt + 6
```



### 样式

```
快速切换Schema:
	Ctrl + ` ( ~ 所在键)
	可设置: Color Scheme, Code Style Scheme, Keymap,,,
```

### 程序运行

```
首次运行代码:			Alt + Shift + F10
首次Debug模式运行:	Alt + Shift + F9
运行代码:			Shift + F10
Debug模式运行:		Shift + F9

附着到某个进程:		Ctrl + Alt + F5, 可以查看该进程的输出
```



## Useful Tools

### 设置项

```
查看快捷键设置:   File --> Settings --> Keymap
设置背景图片及透明度:	
	File --> Settings --> Appearance&Behavior --> Appearance --> Background Image

```

### 调试

```
Run to Cursor (Alt + F9)以Debug模式运行时,  可以对所打的断点进行条件设定:
    在断点上单击鼠标右键,  在 Condition 中输入条件, Debug时若条件返回True, 断点才会起作用,
    (进入 More, 可查看更多设置项)

    应用场景举例:
        1. 控制在循环中进行到哪一步, 才让断点起作用
        2. 在变量值满足某一条件时, 才让断点起作用
        3. 为指定远程IP打断点: 如 request.remote_addr=="10.166.66.66"

临时让所有断点不可用:			More Breakpoints按钮
Debug时打开调试计算窗口:		Alt + F8,	Evaluate Expression按钮
Debug时直接跳到光标所在的位置:	Alt + F9,	Run to Cursor按钮
跳回当前Debug所在文件的所在行:	Alt + F10,	Show Excutition Point按钮

Debug时调出python shell:	Show Python Prompt按钮
	在 python shell 中, 能获取程序中所有变量, 可以对变量重新赋值(会改变原值)

```

### 恢复误删文件

pycharm Local History

```
1. 在项目目录/文件上右键 --> Local History --> Show History
2. 选择修改记录, 右键 --> Revert(恢复)
```

### 设置和使用代码模板

```
设置代码模板
    1. File --> Settings --> Editor --> Live Templates -->
    2. 点击右侧 + 号, 填写输入框: Abbreviation, Description, Template text, 
    3. 点击下方 Define, 选择模板应用于哪个语言(如python)
    4. Apply --> OK
	
查看代码模板列表
	Ctrl + J
使用代码模板
	A. Ctrl+J调出代码模板列表, 选择和使用模板
	B. 或输入之前设置的 Abbreviation 值, 选择模板.
```



### 一键分析代码性能

在 Python 中有许多模块可以帮助你分析并找出你的项目中哪里出现了性能问题。

比如，常用的模块有 cProfile，在某些框架中，也内置了中间件帮助你进行性能分析，比如 Django ，WSGI。

做为Python 的第一 IDE， PyCharm 本身就支持了这项功能。

假设现在要分析如下这段代码的性能损耗情况，找出哪个函数耗时最多

```
import time
def fun1():
	time.sleep(1)
def fun2():    
	time.sleep(1)
def fun3():    
	time.sleep(2)
def fun4():    
	time.sleep(1)
def fun5():    
	time.sleep(1)    

fun4()
fun1()
fun2()
fun3()
fun5()
```

点击 Run -> Profile '程序' (或在代码窗口单击鼠标右键来找到) ，即可进行性能分析。

![img](https://mmbiz.qpic.cn/mmbiz_png/UFM3uMlAXxNe5MPfmmNeCMibRg3o9PGqm8MlYBFBjiaMBIvXiaTUeMVoFGRjX0IjyP5rWIhI3WHKbusjPLA8ql2fg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

运行完毕后，会自动跳出一个性能统计界面。

![img](https://mmbiz.qpic.cn/mmbiz_png/UFM3uMlAXxNe5MPfmmNeCMibRg3o9PGqmx60pPyTiaevCH8wp3upRSRaZ0DFWjOT5b8JWTCC7icJPoOIA4JPUnPLg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

性能统计界面由Name、Call Count、Time(ms)、Own Time(ms) ，4列组成一个表格，见下图。

1. 表头Name显示被调用的模块或者函数；Call Count显示被调用的次数；Time(ms)显示运行时间和时间百分比，时间单位为毫秒（ms）。
2. 点击表头上的小三角可以升序或降序排列表格。
3. 在Name这一个列中双击某一行可以跳转到对应的代码。
4. 以fun4这一行举例：fun4被调用了一次，运行时间为1000ms，占整个运行时间的16.7%

点击 Call Graph（调用关系图）界面直观展示了各函数直接的调用关系、运行时间和时间百分比，见下图。

![img](https://mmbiz.qpic.cn/mmbiz_png/UFM3uMlAXxNe5MPfmmNeCMibRg3o9PGqmn7rSRiaTBsIQSxrf8VZ9FEsrSX77oPZe5dzSembJdscVHawsEjVhsnQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

左上角的4个按钮表示放大、缩小、真实大小、合适大小；

1. 箭头表示调用关系，由调用者指向被调用者；
2. 矩形的左上角显示模块或者函数的名称，右上角显示被调用的次数；
3. 矩形中间显示运行时间和时间百分比；
4. 矩形的颜色表示运行时间或者时间百分比大小的趋势：红色 > 黄绿色 > 绿色，由图可以看出fun3的矩形为黄绿色，fun1为绿色，所有fun3运行时间比fun1长。
5. 从图中可以看出Test.py直接调用了fun3、fun1、fun2和fun5函数；fun5函数直接调用了fun4函数；fun1、fun2、fun3、fun4和fun5都直接调用了print以及sleep函数；整个测试代码运行的总时间为6006ms，其中fun3的运行时间为1999ms，所占的时间百分比为33.3%，也就是 1999ms / 6006ms = 33.3%。







# Ubuntu Server使用Pycharm

> 可参考 [Linux公社](https://www.linuxidc.com/Linux/2017-09/147112.htm)
>
> [Xmanager passive功能不能使用的问题](https://www.linuxidc.com/Linux/2012-07/64852.htm)



1-windows下载 `Xmanager`, `Xshell`

打开 `Xmanager - Passive`  (重要):  下载好Xmanager后,  `Xmanager - Passive` 就在 `tools` 目录下

2-Windows打开 Xshell,  连接Ubuntu服务器

3-Ubuntu服务器下载桌面程序

```bash
sudo apt-get remove unity
sudo apt-get remove ubuntu-desktop --auto-remove
sudo apt-get remove ghome * --auto-remove

sudo apt-get install ubuntu-desktop -y
sudo apt-get install xrdp -y
sudo apt-get install vnc4server tightvncserver -y

echo "xfce4-session" > ~/.xsession

sudo service xrdp restart
```

4-Ubuntu服务器设置环境变量 `DISPLAY`,  启动 `pycharm`

```bash
export DISPLAY=192.168.199.121:0.0
sh /home/lqq/pycharm-community-2019.1.1/bin/pycharm.sh
```



了解:  [xrdp 与 vnc](https://www.linuxidc.com/Linux/2017-09/147112.htm)



附: 尝试过无效的命令

```
vncserver
export DISPLAY=localhost:1
xhost +
export DISPLAY=192.168.199.121:0.0
xclock
sh /home/lqq/pycharm-community-2019.1.1/bin/pycharm.sh
```


