# Anaconda

[Anaconda官网](https://www.anaconda.com/)

Anaconda是一个方便的python包管理和环境管理软件，可以创建多个互不干扰的环境，分别运行不同版本的软件包，以达到兼容的目的。

## Miniconda

https://docs.conda.io/en/latest/miniconda.html

Miniconda 是一个 Anaconda 的轻量级替代，默认只包含了 python 和 conda，但是可以通过 pip 和 conda 来安装所需要的包。

Miniconda 安装包可以到 https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/ 下载。



# 安装

**获取安装包**

[清华大学TUNA镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/):   https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

windows: `.exe`文件

linux: `.sh` 脚本

MacOS: `.pkg`包

**windows上安装Anaconda**

执行`.exe`安装成功后，可以从windows开始菜单中查看到Anaconda下面包含以下内容：

- Anaconda Navigator：图形界面。 
- Anaconda Prompt：命令行界面。 打开时默认进入`base`环境。
- Jupyter Noterbook：基于Web的交互式计算环境，用于展示数据分析的过程，并且生成容易阅读的文档。 
- Spyder：Python集成开发环境，布局类似于Matlab。



**Linux上安装Anaconda**

```shell
sudo chmod +x xxx.sh
sudo ./xxx.sh
```



# 配置pypi下载源

```shell
# 添加conda默认源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
# 配置在包后面显示来源
conda config --set show_channel_urls yes

# 更新conda
conda upgrade --all

# view your configuration's current state
conda config --show channels
# view config file locations
conda config --show-sources
```



pypi清华源:  https://pypi.tuna.tsinghua.edu.cn/simple/

> 直接访问会获取所有包列表,  可以根据包名获取包目录:
>
> ```
> https://pypi.tuna.tsinghua.edu.cn/simple/包名
> ```



# 环境管理

当创建一个新环境时，anaconda将在 `envs` 中创建一个新的文件夹，这个文件夹包括了你安装在这个环境中的所有包.

```shell
# 查看conda环境配置
conda info

# 查看当前有多少环境
# 系统默认创建了名叫base的默认环境
conda env list	# 或 conda info --envs

# 查看当前python环境
conda info --e

# 创建新环境
conda create --name [env_name]	# 或 conda create -n [env_name]

# 创建新环境时指定包内容
conda create -n [env_name] python=3.5
# 指定多个包
conda create -n [env_name] python=3.5 numpy pandas

# 更新包信息
conda update --all

# windows上切换环境
activate [env_name]
# linux和mac上切换环境
source activate [env_name]

# windows上退出环境
deactivate
# linux和mac上退出环境 
source deactivate [env_name]
```



其他常用命令

```shell
# 创建一个新环境想克隆一部分旧的环境
conda create -n [env_name] --clone [oldname]

# 删除环境
conda remove -n [env_name] --all

# 导出环境配置
conda env export > environment.yml

# 导入环境配置  
conda env create -f environment.yml

```





# 包管理

 `conda` 是包及其依赖项和环境的管理工具。 `conda` 结合了 `pip` 和 `virtualenv` 的功能。 

```shell
# 当前环境下的操作
conda list	# 列举所有包
conda list -n [pkg_name]	# 列举特定包
conda install [pkg_name]	# 安装某包
conda install -n [env_name] [pkg_name]	# 为指定环境安装包
conda search [pkg_name]		# 搜索包, 精确查找: conda search --full-name [pkg_name]
conda update [pkg_name]		# 更新包
conda update -n [env_name] [pkg_name]	# 为指定环境更新包
conda remove [pkg_name]		# 删除包
conda remove -n [env_name] [pkg_name]	# 为指定环境删除包

# conda、anaconda、python本身也是包
conda update conda
conda update anaconda
conda update python
```

也可以通过pip命令安装包：

```bash
pip install lxml
pip install "xxx/xxx/xxx.whl"
```







**pip 与 conda 比较**

- 依赖项检查

```
1. 依赖项检查
	pip： 不一定会展示所需其他依赖包。安装包时或许会直接忽略依赖项而安装，仅在结果中提示错误。
	conda：列出所需其他依赖包。安装包时自动安装其依赖项。可以便捷地在包的不同版本中自由切换。
2. 环境管理
	pip：维护多个环境难度较大。
	conda：比较方便地在不同环境之间进行切换，环境管理较为简单。
3. 对系统自带Python的影响
	pip：在系统自带Python中包的**更新/回退版本/卸载将影响其他程序。
	conda：不会影响系统自带Python。
4. 适用语言
	pip：仅适用于Python。
	conda：适用于Python, R, Ruby, Lua, Scala, Java, JavaScript, C/C++, FORTRAN。
```





# Jupyter Notebook

文档:

- 官方文档:  https://jupyter-notebook.readthedocs.io/en/stable/notebook.html

- Jupyter Notebook介绍、安装及使用教程：  https://www.jianshu.com/p/91365f343585/

简介

- Jupyter Notebook，原名IPython Notbook，是IPython的加强网页版，一个开源Web应用程序
- 是一款程序员和科学工作者的**编程/文档/笔记/展示**软件
- **.ipynb**文件格式是用于计算型叙述的**JSON文档格式**的正式规范

使用Anaconda安装

```shell
# 切换到目标环境
    # windows上切换环境
    activate [env_name]
    # linux和mac上切换环境
    source activate [env_name]
# 安装
conda install jupyter notebook
```

使用pip安装

```
# 1.切换环境
# 2.安装
pip3 install --upgrade pip
pip3 install jupyter
```

启动命令

```shell
jupyter notebook

# 本地notebook的默认URL为：http://localhost:8888
# 默认工作路径：当前用户目录
```



## 关联conda环境和包: nb_conda

① 安装

```shell
conda install nb_conda
```

执行上述命令能够将你conda创建的环境与Jupyter Notebook相关联，便于你在Jupyter Notebook的使用中，在不同的环境下创建笔记本进行工作。

② 使用

管理conda环境和包:

- 可以在Conda类目下对conda环境和包进行一系列操作。

  ![img](https:////upload-images.jianshu.io/upload_images/5101171-80f141edb2bac9d5?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

切换内核:

- 可以在笔记本内的“Kernel”类目里的“Change kernel”切换内核。

  ![img](https:////upload-images.jianshu.io/upload_images/5101171-2cb5c4ec387ca814?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

③ 卸载nb_conda包

```
canda remove nb_conda
```



## 更改工作空间

在其配置文件ipython_notebook_config.py中，有如下一句

> The directory to use for notebooks and kernels.
> c.NotebookApp.notebook_dir = u''


该句就是用来指定其工作空间的，例如，默认的工作空间是：用户名文件夹，例如，现在想要将工作空间变为D:\Jupyter，那么，需要做如下更改(要记得删掉注释#)

> The directory to use for notebooks and kernels.
> c.NotebookApp.notebook_dir = u'D:\Jupyter'1
> 注意：路径最后一级后面不要加符号“\”



**如何找到该配置文件？**

在cmd中输入 `jupyter notebook --generate-config`
如果该配置文件已经存在，那么，会出现如下信息,从中可以见到配置文件存在的位置，注意，此时，输入N，不要overwrite

![image_1b4e641ot340t3g1asfdv81972m.png-16.9kB](http://static.zybuluo.com/lutingting/cdan3d424oinr691ppo8qe2h/image_1b4e641ot340t3g1asfdv81972m.png)

如果该配置文件不存在，那么，将会初始化产生一个配置文件
在cmd中输入：`ipython profile create `
可以找到关于jupyter的配置文件的位置



## 使用shell命令

```
!跟shell命令
如:
!ls
```



## 加载本地Python文件

- 使用场景:   想在Jupyter Notebook中加载本地的Python文件并执行文件代码。

- 方法:   在cell中执行以下命令：

```
%load Python文件的绝对路径

%load URL 可以加载指定网站的源代码
```

- 输入命令后，可以按`CTRL 回车`来执行命令。第一次执行，是将本地的Python文件内容加载到单元格内。此时，Jupyter Notebook会自动将“%load”命令注释掉（即在前边加井号“#”），以便在执行已加载的文件代码时不重复执行该命令；第二次执行，则是执行已加载文件的代码。



## 直接运行本地Python文件

- 使用场景:   不想在Jupyter Notebook的单元格中加载本地Python文件，想要直接运行。

- 方法:   执行命令：

```
%run Python文件的绝对路径
或
!python3 Python文件的绝对路径
或
!python Python文件的绝对路径
```

- “!python3”和“!python”属于 `!shell命令` 语法的使用，即在Jupyter Notebook中执行shell命令的语法。

- 输入命令后，可以按 `CTRL 回车` 来执行命令，执行过程中将不显示本地Python文件的内容，直接显示运行结果。



## 获取当前位置

```
%pwd  (windows, linux)
或
!pwd  (linux)
```



## 新建终端

```
页面按钮: New --> Terminal

在windows的Jupyter Notebook上开启的终端, 可以输入 ls, pwd等linux命令
```



## 隐藏笔记本输入单元格

使用场景

在Jupyter Notebook的笔记本中无论是编写文档还是编程，都有输入（In []）和输出（Out []）。当我们编写的代码或文档使用的单元格较多时，有时我们只想关注输出的内容而暂时不看输入的内容，这时就需要隐藏输入单元格而只显示输出单元格。

方法一

代码

```python
from IPython.display import display
from IPython.display import HTML
import IPython.core.display as di # Example: di.display_html('<h3>%s:</h3>' % str, raw=True)

# 这行代码的作用是：当文档作为HTML格式输出时，将会默认隐藏输入单元格。
di.display_html('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)

# 这行代码将会添加“Toggle code”按钮来切换“隐藏/显示”输入单元格。
di.display_html('''<button onclick="jQuery('.input_area').toggle(); jQuery('.prompt').toggle();">Toggle code</button>''', raw=True)
```

在笔记本第一个单元格中输入以上代码，然后执行，即可在该文档中使用“隐藏/显示”输入单元格功能。

- 缺陷：此方法不能很好的适用于Markdown单元格。



## 使用Matplotlib绘图

在Jupyter Notebook中，如果使用Matplotlib绘图，有时是弹不出图像框的，此时，可以在开头加入

```
%matplotlib inline
```

## 在jupyter中设置link

在jupyter中设置link，需要设置两部分：
**1. 要跳到的位置(the destination)** , 需要在要跳转到的位置添加下面语句:

```
<a id='the_destination'></a>
这里的id取值任意赋值，下面在添加链接时要用
```

**2. 需要添加链接的文字**，即点击该处可以跳转到the destination，在需要添加链接的文字后面加入：

```
[需要添加连接的文字](#the_destination)
```







