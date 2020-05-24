# clint

# 基本介绍

一个简单的命令行开发工具

# 资源

- github:  https://github.com/kennethreitz-archive/clint

# 使用方法

### 打印时带缩进

```python
>>> from clint.textui import puts, indent

>>> puts('not indented text')
>>> with indent(4):
>>>     puts('indented text')
not indented text
    indented text
```

### 缩进 + 指定前缀

```python
>>> puts('not indented text')
>>> with indent(4, quote=' >'):
>>>     puts('quoted text')
>>>     puts('pretty cool, eh?')

not indented text
 >  quoted text
 >  pretty cool, eh?
```

### 打印时带颜色

```python
>>> from clint.textui import colored, puts

>>> puts(colored.red('red text'))
red text

# It's red in Windows, OSX, and Linux alike.
```

### 获取多行输入内容

I want to get data piped to stdin.

```python
>>> clint.piped_in()
# if no data was piped in, piped_in returns None
```

### 解析命令行传入的参数

```python
>>> from clint import arguments
>>> args = arguments.Args()
>>> args.get(0)

# if no argument was passed, get returns None
```

### 存储一个配置文件

```python
>>> from clint import resources

>>> resources.init('Company', 'AppName')
>>> resources.user.write('config.ini', file_contents)

# OSX: '/Users/appuser/Library/Application Support/AppName/config.ini'
# Windows: 'C:\\Users\\appuser\\AppData\\Local\\Company\\AppName\\config.ini'
# Linux: '/home/appuser/.config/appname/config.ini'
```



I want to force color output even if stdout is not a TTY:

> $ export CLINT_FORCE_COLOR=1



### 获取用户输入并交验

```python
>>> from clint.textui import prompt, validators
>>> path = prompt.query('Installation Path', default='/usr/local/bin/', validators=[validators.PathValidator()])
```



### 输入确认

```python
from clint.textui import prompt

confirm = prompt.yn('是否确认?')
assert isinstance(confirm, bool)
```



### 多选一

```python
from clint.textui import prompt

print(prompt.options('请选择: ', options=['a', 'b', 'c']))
```



# 代码结构

```
clint
│  arguments.py		# 定义了 Args 类, 提供命令行参数接口
│  eng.py
│  pipes.py
│  resources.py
│  utils.py
│  __init__.py
│
├─packages
│  │  appdirs.py	# 即第三方模块 appdirs
│  │  ordereddict.py
│  │  __init__.py
│  │
│  ├─colorama
│     │  ansi.py
│     │  ansitowin32.py
│     │  initialise.py
│     │  win32.py
│     │  winterm.py
│     ├─ __init__.py
│
├─textui
   │  colored.py
   │  cols.py
   │  core.py
   │  formatters.py
   │  progress.py
   │  prompt.py
   │  validators.py
   ├─ __init__.py
```



# 细节





# 扩展内容 (如: 类似模块, ...)

## click

## argparse

