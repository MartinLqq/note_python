# python编写 CLI 工具

在编写Command-line之前，  要先知道以下内容：

- python项目怎么打包？      setuptools
- setup.py官方文档怎么看？
- 编写CLI有哪些标准库、第三方库？最优选择哪个库？
  - 标准库中推荐的命令行解析模块： argparse
  - **但,  推荐使用第三方库:  click**
  - 还有其他模块可以完成同样的任务：docopt、getopt、optparse
  - argparse基于optparse，用法与其非常相似。 
- 选择的CLI库的官方文档怎么看？ 



文档：

- 分发 Python 模块：https://docs.python.org/zh-cn/3.6/distributing/index.html



python基础文档：

- Python常见问题：https://docs.python.org/zh-cn/3.6/faq/general.html#id3
- Python 常用指引: https://docs.python.org/zh-cn/3.6/howto/index.html



注意：

- 每个 CLI 工具的 setup.py 中都应有 entry_points 这个节点。





# 项目打包



**不包括Docker项目打包**



文档:

- Packaging Py thon Projects：https://packaging.python.org/tutorials/packaging-projects/

## 目录基本结构

```
my_project
    │  README.md
    │  setup.py
    │  __init__.py
    │
    ├─data
    │      data_file  # (text file)
    │
    ├─src
    │  │  __init__.py
    │  │
    │  └─example_pkg
    │      │  example.py
    │      │  package_data.dat
    │      └─__init__.py (defined function `main`)
    │
    └─tests
```



## setup.py

- `setup.py` is the build script for [setuptools](https://packaging.python.org/key_projects/#setuptools). 

- 在项目中的位置:  项目根目录 (包的同级目录)

- setup.py命令行:  

  - ```
    python setup.py -h
    ```

- **setup.py怎么写 ?**

  - Packaging and distributing projects: https://packaging.python.org/guides/distributing-packages-using-setuptools/
  - Github上的setup.py模板及参数说明:  https://github.com/pypa/sampleproject/blob/master/setup.py

```python
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='example-pkg',  # Required
    vaersion='0.0.1',  # Required
    author='Example Author',
    author_email='author@example.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',  # text/plain, text/x-rst
    url='https://github.com/pypa/sampleproject',
    keywords='example',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.5',  # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    install_requires=['requests'],  # https://packaging.python.org/discussions/install-requires-vs-requirements/#install-requires-vs-requirements-files
    extras_require={  # pip install example-pkg[dev]
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data = {
                   'example_pkg': ['package_data.dat'],
               },
    data_files=[('my_data', ['data/data_file'])],
    entry_points={  # provide a command called `example_pkg` which executes the function `main`
        'console_scripts': [  # console_scripts可以指定多个元素, 对应多个命令和入口
            'example_pkg=example_pkg:main',  # `命令=入口`
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)
```



## setup.cfg



## README.md / README.rst

- md:  markdown
- rst:   reStructuredText







## 安装'构建和分发工具'

1. 先创建好虚拟环境

2. ```bash
   # 下载或更新
   python3 -m pip install setuptools wheel twine
   python3 -m pip install --user --upgrade setuptools wheel
   ```

## 打包项目

```bash
python3 setup.py sdist bdist_wheel
# sdist: source distribution
# bdist_wheel  -->  dist/xxx.whl
```

生成目录:

```
build/
    ├─bdist.win-amd64
    └─lib
    	└─example_pkg
            example.py
            package_data.dat
            __init__.py

dist/
  example-pkg-0.0.1-py3-none-any.whl
  example-pkg-0.0.1.tar.gz

example_pkg.egg-info/
  dependency_links.txt
  PKG-INFO
  SOURCES.txt
  top_level.txt
```



## 本地安装包

```bash
pip install -e .
pip install -e .[dev]
python setup.py install
```

pip  install  -e  .[dev]:

- -e, --editable <path/url>   Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.
- .[xxx]中的xxx对应为 setup.py中的 extras_require 字典的key



## 发布

略





# argparse

- 标准库
- 命令行选项、参数和子命令解析器.
- 文档:  https://docs.python.org/zh-cn/3.6/library/argparse.html





## 基本使用流程

1. 创建一个解析器： parser = argparse.ArgumentParser()
2. 添加参数：parser.add_argument()
3. 解析参数: args = parser.parse_args()
4. 处理命令,  返回结果



## argparse开源项目

1. foremast:  https://github.com/foremast/foremast/blob/master



## ArgumentParser()

 [`ArgumentParser`](https://docs.python.org/zh-cn/3.6/library/argparse.html#argparse.ArgumentParser) 对象包含将命令行解析成 Python 数据类型所需的全部信息。

### 参数

Keyword Arguments:

```
prog - 程序（program）的名称（默认值：sys.argv[0]），无论程序从何处被调用
usage - 描述程序用途的字符串（默认值：从添加到解析器的参数生成）
description - 在参数帮助文档之前显示的文本（默认值：无）
epilog - 在参数帮助文档之后显示的文本（默认值：无）
parents - 一个 ArgumentParser 对象的列表，它们的参数也应包含在内
formatter_class - 用于自定义帮助文档输出格式的类
prefix_chars - 可选参数的前缀字符集合（默认值： ‘-‘）
fromfile_prefix_chars - 当需要从文件中读取其他参数时，用于标识文件名的前缀字符集合（默认值： None）
argument_default - 参数的全局默认值（默认值： None）
conflict_handler - 解决冲突选项的策略（通常是不必要的）
add_help - 为解析器添加一个 -h/--help 选项（默认值： True）
allow_abbrev - 如果缩写是无歧义的，则允许缩写长选项 （默认值：True）
```





## add_argument()

### 参数

- 位置参数:
  - 增加必传位置参数:  parser.add_argument('name', ...)
  - 增加可选:  parser.add_argument('-n', '--name' ...),  根据require参数的值,  可选/必传
  -  当 parse_args() 被调用，可选选项会以 `-` 前缀识别，剩下的参数则会被假定为必传位置参数
- 可选参数:
  - [name or flags](https://docs.python.org/zh-cn/3.6/library/argparse.html#name-or-flags) - 一个命名或者一个选项字符串的列表，例如 `foo` 或 `-f, --foo`。
  - [action](https://docs.python.org/zh-cn/3.6/library/argparse.html#action) - Union[str, Type[Action]],  当参数在命令行中出现时使用的动作基本类型。
  - [nargs](https://docs.python.org/zh-cn/3.6/library/argparse.html#nargs) - 命令行参数应当消耗的数目。
  - [const](https://docs.python.org/zh-cn/3.6/library/argparse.html#const) - 被一些 [action](https://docs.python.org/zh-cn/3.6/library/argparse.html#action) 和 [nargs](https://docs.python.org/zh-cn/3.6/library/argparse.html#nargs) 选择所需求的常数。
  - [default](https://docs.python.org/zh-cn/3.6/library/argparse.html#default) - 当参数未在命令行中出现时使用的值。
  - [type](https://docs.python.org/zh-cn/3.6/library/argparse.html#type) - 命令行参数应当被转换成的类型。
  - [choices](https://docs.python.org/zh-cn/3.6/library/argparse.html#choices) - 可用的参数的容器。
  - [required](https://docs.python.org/zh-cn/3.6/library/argparse.html#required) - bool, 此命令行选项是否可省略 （仅选项可用）。
  - [help](https://docs.python.org/zh-cn/3.6/library/argparse.html#help) - Optional[str], 一个此选项作用的简单描述。
  - [metavar](https://docs.python.org/zh-cn/3.6/library/argparse.html#metavar) - 在使用方法消息中使用的参数值示例。
  - [dest](https://docs.python.org/zh-cn/3.6/library/argparse.html#dest) - Optional[str], 被添加到 [`parse_args()`](https://docs.python.org/zh-cn/3.6/library/argparse.html#argparse.ArgumentParser.parse_args) 所返回对象上的属性名。
  - version



### nargs参数取值

1. N:  一个整数,  命令行中的N个参数会被聚集到一个列表中 
2. '?':   如果可能的话，会从命令行中消耗一个参数，并产生一个单一项。如果当前没有命令行参数，则会产生 [default](https://docs.python.org/zh-cn/3.6/library/argparse.html#default) 值。注意，对于选项，有另外的用例 - 选项字符串出现但没有跟随命令行参数，则会产生 [const](https://docs.python.org/zh-cn/3.6/library/argparse.html#const)值。 
3. '*'
4. '+'
5. argarse.REMAINDER

**举例**

1. nargs=一个整数

   ```python
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', nargs=2)
   >>> parser.add_argument('bar', nargs=1)
   >>> parser.parse_args('c --foo a b'.split())
   Namespace(bar=['c'], foo=['a', 'b'])
   ```

2. nargs='?'

   ```python
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
   >>> parser.add_argument('bar', nargs='?', default='d')
   >>> parser.parse_args(['XX', '--foo', 'YY'])
   Namespace(bar='XX', foo='YY')
   >>> parser.parse_args(['XX', '--foo'])
   Namespace(bar='XX', foo='c')
   >>> parser.parse_args([])
   Namespace(bar='d', foo='d')
   ```

    `nargs='?'` 的一个更普遍用法是允许可选的输入或输出文件: 

   ```python
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
   ...                     default=sys.stdin)
   >>> parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
   ...                     default=sys.stdout)
   >>> parser.parse_args(['input.txt', 'output.txt'])
   Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
             outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
   >>> parser.parse_args([])
   Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
             outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)
   ```

3. nargs='*'

    `'*'`。所有当前命令行参数被聚集到一个列表中。注意通过 `nargs='*'` 来实现多个位置参数通常没有意义，但是多个选项是可能的。 

   ```python
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', nargs='*')
   >>> parser.add_argument('--bar', nargs='*')
   >>> parser.add_argument('baz', nargs='*')
   >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
   Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])
   ```

4. nargs='+'

    和 `'*'` 类似，所有当前命令行参数被聚集到一个列表中。另外，当前没有至少一个命令行参数时会产生一个错误信息。例如: 

   ```python
   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('foo', nargs='+')
   >>> parser.parse_args(['a', 'b'])
   Namespace(foo=['a', 'b'])
   >>> parser.parse_args([])
   usage: PROG [-h] foo [foo ...]
   PROG: error: the following arguments are required: foo
   ```

5. nargs=argarse.REMAINDER

   所有剩余的参数，均转化为一个列表赋值给此项，通常用此方法来将剩余的参数传入另一个parser进行解析。

   ```python
   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('--foo')
   >>> parser.add_argument('command')
   >>> parser.add_argument('args', nargs=argparse.REMAINDER)
   >>> print(parser.parse_args('--foo B cmd --arg1 XX ZZ'.split()))
   Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')
   ```

6. 如果不提供 nargs 命名参数，则消耗参数的数目将被 action 决定。通常这意味着单一项目（非列表）消耗单一命令行参数。 



提供 `default=argparse.SUPPRESS` 导致命令行参数未出现时没有属性被添加:

```
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', default=argparse.SUPPRESS)
>>> parser.parse_args([])
Namespace()
>>> parser.parse_args(['--foo', '1'])
Namespace(foo='1')
```



### action参数取值

```
None:
	...
store: 
	存储参数的值，这是默认的动作。
	如增加了选项--name, 命令行指定后会赋值: args.name = 传入值
store_const: 
	必须配合add_argument()方法的const参数,
	如增加了选项--name, 命令行指定后会赋值: args.name = const参数值
store_true:  
	如增加了选项--name, 命令行指定后会赋值: args.name = True，
	默认是True
store_false：
	默认是False
append:
	如增加了选项和参数 --name 'John' --name 'Martin', 
	命令行指定后会赋值: args.name = ['John', 'Martin']
append_const：
	重要， 见后面例子
count:
	如增加了选项 --name --name( 或短选项-nn ), 命令行指定后会赋值: args.name = 2.
	注意增加了选项--name时, 默认结果是None
help:
	如增加了选项 --name, 命令行指定后会打印帮助信息
version:
	必须配合add_argument()方法的version参数, 命令行指定后会打印version值
parsers:
	
	
	
	
```



append_const：

- 存储一个列表，并将 const 命名参数指定的值追加到列表中。（注意 const 命名参数默认为 None。）append_const  动作一般在多个参数需要在同一列表中存储常数时会有用。
- 例如:

```php
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--str', dest='types', action='append_const', const=str)
>>> parser.add_argument('--int', dest='types', action='append_const', const=int)
>>> parser.parse_args('--str --int'.split())
Namespace(types=[<class 'str'>, <class 'int'>])
```



### type参数取值

 add_argument() 的 `type` 关键词参数允许任何的类型检查和类型转换。一般的内建类型和函数可以直接被 `type` 参数使用

```python
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('foo', type=int)
>>> parser.add_argument('bar', type=open)  # open函数
>>> parser.parse_args('2 temp.txt'.split())
Namespace(bar=<_io.TextIOWrapper name='temp.txt' encoding='UTF-8'>, foo=2)
```



#### FileType - 命令行传文件

1. type=open:

   - parser.add_argument('bar', type=open)  # open函数

2.  type=FileType(mode='r', bufsize=-1, encoding=None, errors=None):

   - ```python
     # 参数均与内置open()函数一致
     - mode
     - bufsize
     - encoding
     - errors
     ```



#### type可接收任意callable类型

- type可接收任意callable类型
- 返回转换后的值

\>>>

```python
>>> def perfect_square(string):
...     value = int(string)
...     sqrt = math.sqrt(value)
...     if sqrt != int(sqrt):
...         msg = "%r is not a perfect square" % string
...         raise argparse.ArgumentTypeError(msg)
...     return value
...
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('foo', type=perfect_square)
>>> parser.parse_args(['9'])
Namespace(foo=9)
>>> parser.parse_args(['7'])
usage: PROG [-h] foo
PROG: error: argument foo: '7' is not a perfect square
```



## parse_args()

- args - List of strings to parse. The default is taken from `sys.argv`
- namespace - An object to take the attributes. The default is a new empty `Namespace` object.



### 选项与值的语法

parser.parse_args() 的 args 参数需要指定一个列表,  列表可以是:

1. ['--foo', 'FOO']

2. ['--foo=FOO']

   ```python
   >>> parser.parse_args(['--foo=FOO'])
   Namespace(foo='FOO', x=None)
   ```

3. 对于短选项:  ['-xX']、['-xyzZ']

   ```python
   >>> parser.parse_args(['-xX'])
   Namespace(foo=None, x='X')
   
   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x', action='store_true')
   >>> parser.add_argument('-y', action='store_true')
   >>> parser.add_argument('-z')
   >>> parser.parse_args(['-xyzZ'])
   Namespace(x=True, y=True, z='Z')
   ```



### 包含 `-` 的参数

https://docs.python.org/zh-cn/3.6/library/argparse.html#arguments-containing





### 参数缩写（前缀匹配）

```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-bacon')
>>> parser.add_argument('-badger')
>>> parser.parse_args('-bac MMM'.split())
Namespace(bacon='MMM', badger=None)
>>> parser.parse_args('-bad WOOD'.split())
Namespace(bacon=None, badger='WOOD')
>>> parser.parse_args('-ba BA'.split())
usage: PROG [-h] [-bacon BACON] [-badger BADGER]
PROG: error: ambiguous option: -ba could match -badger, -bacon
```





### 命名空间对象

- args = parser.parse_args(),  args 是一个 argparse.Namespace() 对象,  
- 如果仅需要一个字典,  使用 **vars(args)**
- parser.parse_args()方法有一个namespace参数,  可以指向一个自定义类,  参数会解析为这个类的对象的属性:

```python
>>> class C:
...     pass
...
>>> c = C()
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo')
>>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
>>> c.foo
'BAR'
```



## 子命令

### 基本使用流程

1. 创建命令解析器:   parser = argparse.ArgumentParser()

2. 添加主命令参数:   parser.add_argument()

3. 将主命令绑定特定的函数:  parser.set_defaults(func=parser.print_help)

4. 添加子命令

   - subparsers = parser.add_subparsers()
   - subparser= subparsers.add_parser()
   - 子命令还可以再添加子命令...

5. 添加一个子命令参数:    subparser.add_argument()

6. 将子命令分别绑定特定的函数:  subparser.set_defaults(func=my_func)

7. 解析所有参数:

   a. args = parser.parse_known_args()

   b. args = parser.parse_args()

8. 执行命令对应的函数:    args.func(args)



```python
"""Mygit Init."""
import argparse
import collections

# from .add_subparsers import add_clone, add_init, add_add

from . import add_subparsers
from .tools import print_version


def main():
    """These are common Git commands used in various situations."""
    # 创建命令解析器
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # 添加主命令参数
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help=print_version.__doc__
    )
    # 将主命令绑定特定的函数
    parser.set_defaults(func=parser.print_help)

    # 添加子命令
    subparsers = parser.add_subparsers()
    # funcs = [add_clone, add_init, add_add]
    # for func in funcs:
    #     func(subparsers)
    for func_name in add_subparsers.__all__:
        getattr(add_subparsers, func_name)(subparsers)

    # 解析参数
    cli_args = collections.namedtuple('cli_args', ['parsed', 'extra'])
    parsed, extra = parser.parse_known_args()
    args = cli_args(parsed, extra)
    if args.parsed.version:
        args.parsed.func = print_version

    # 执行命令对应的函数
    try:
        args.parsed.func(args)
    except (AttributeError, TypeError):
        # AttributeError: 'cli_args' object has no attribute 'write'
        args.parsed.func()


if __name__ == '__main__':
    main()

```



#### add_subparsers的参数

````python
subparsers = parser.add_subparsers()
````

- title - title for the sub-parser group in help output; by default “subcommands” if description is provided, otherwise uses title for positional arguments
- description - description for the sub-parser group in help output, by default `None`
- prog - usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument
- parser_class - class which will be used to create sub-parser instances, by default the class of the current parser (e.g. ArgumentParser)
- [action](https://docs.python.org/zh-cn/3.6/library/argparse.html#action) - the basic type of action to be taken when this argument is encountered at the command line
- [dest](https://docs.python.org/zh-cn/3.6/library/argparse.html#dest) - name of the attribute under which sub-command name will be stored; by default `None` and no value is stored
- [help](https://docs.python.org/zh-cn/3.6/library/argparse.html#help) - help for sub-parser group in help output, by default `None`
- [metavar](https://docs.python.org/zh-cn/3.6/library/argparse.html#metavar) - string presenting available sub-commands in help; by default it is `None` and presents sub-commands in form {cmd1, cmd2, ..}

```python
>>> # create the top-level parser
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo', action='store_true', help='foo help')
>>> subparsers = parser.add_subparsers(help='sub-command help')
>>>
>>> # create the parser for the "a" command
>>> parser_a = subparsers.add_parser('a', help='a help')
>>> parser_a.add_argument('bar', type=int, help='bar help')
>>>
>>> # create the parser for the "b" command
>>> parser_b = subparsers.add_parser('b', help='b help')
>>> parser_b.add_argument('--baz', choices='XYZ', help='baz help')
>>>
>>> # parse some argument lists
>>> parser.parse_args(['a', '12'])
Namespace(bar=12, foo=False)
>>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
Namespace(baz='Z', foo=True)
```



#### 开源例子

(1)  **项目：**quartetsampling   **作者：**FePhyFoFum   | [项目源码](https://github.com/FePhyFoFum/quartetsampling) | [文件源码](https://github.com/FePhyFoFum/quartetsampling/tree/master/pysrc/merge_output.py) 

```python
def generate_argparser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=LICENSE)
    parser.add_argument('-d', '--nodedata', required=True, nargs=1,
                        help=("file containing paths of one or more"
                              "RESULT.node.score.csv files"))
    parser.add_argument('-t', '--tree', required=True, type=open,
                        nargs=1,
                        help="tree file in Newick format")
    parser.add_argument('-o', '--out', required=True,
                        nargs=1,
                        help="new output files prefix")
    parser.add_argument("-v", "--verbose", action="store_true")
    # These args are hidden to pass through to the treedata object
    parser.add_argument("-c", "--clade", nargs=1, help=argparse.SUPPRESS)
    parser.add_argument("-s", "--startk", type=int, default=0,
                        help=argparse.SUPPRESS)
    parser.add_argument("-p", "--stopk", type=int, help=argparse.SUPPRESS)
    return parser
```

(2) **项目：**foremast   **作者：**gogoair   | [项目源码](https://github.com/gogoair/foremast) | [文件源码](https://github.com/gogoair/foremast/tree/master/src/foremast/securitygroup/__main__.py)

```python
def main():
    """Entry point for creating an application specific security group"""
    logging.basicConfig(format=LOGGING_FORMAT)
    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    add_debug(parser)
    add_app(parser)
    add_env(parser)
    add_properties(parser)
    add_region(parser)
    args = parser.parse_args()

    logging.getLogger(__package__.split('.')[0]).setLevel(args.debug)

    log.debug('Parsed arguments: %s', args)

    spinnakerapps = SpinnakerSecurityGroup(app=args.app, env=args.env, region=args.region, prop_path=args.properties)
    spinnakerapps.create_security_group()
```

(3) 更多开源项目: http://codingdict.com/sources/py/argparse/1904.html





### 平行运行多个子命令





## 参数组

add_argument_group()

```python
>>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
>>> group1 = parser.add_argument_group('group1', 'group1 description')
>>> group1.add_argument('foo', help='foo help')
>>> group2 = parser.add_argument_group('group2', 'group2 description')
>>> group2.add_argument('--bar', help='bar help')
>>> parser.print_help()
usage: PROG [--bar BAR] foo

group1:
  group1 description

  foo    foo help

group2:
  group2 description

  --bar BAR  bar help
```



```python
import argparse
import json
from functools import partial


def jsonable(param, parser, string):
    try:
        ret = json.loads(string.replace('\'', '"'))
        if not isinstance(ret, dict):
            raise ValueError
        return ret
    except ValueError:
        print(string)
        parser.exit('%s must be a jsonable dict string' % param)


parser = argparse.ArgumentParser(prog='MyProg')
grp1 = parser.add_argument_group('grp1', 'grp1 description')
grp2 = parser.add_argument_group('grp2')

grp1.add_argument(
    '-u', '--url',
    action='store',
    required=True,
    help='The start url.'
)
grp1.add_argument(
    '-H', '--headers',
    action='store',
    type=partial(jsonable, 'headers', parser)
)

grp2.add_argument(
    '-d', '--deep',
    action='store',
    type=int,
)
print(parser.parse_args())

```





## 互斥组

add_mutually_exclusive_group()

互斥组中只有一个参数在命令行中可用

```python
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> group = parser.add_mutually_exclusive_group()
>>> group.add_argument('--foo', action='store_true')
>>> group.add_argument('--bar', action='store_false')
>>> parser.parse_args(['--foo'])
Namespace(bar=True, foo=True)
>>> parser.parse_args(['--bar'])
Namespace(bar=False, foo=False)
>>> parser.parse_args(['--foo', '--bar'])
usage: PROG [-h] [--foo | --bar]
PROG: error: argument --bar: not allowed with argument --foo
```

[`add_mutually_exclusive_group()`](https://docs.python.org/zh-cn/3.6/library/argparse.html#argparse.ArgumentParser.add_mutually_exclusive_group) 方法也接受一个 *required* 参数，表示在互斥组中至少有一个参数是需要的:

```
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> group = parser.add_mutually_exclusive_group(required=True)
>>> group.add_argument('--foo', action='store_true')
>>> group.add_argument('--bar', action='store_false')
>>> parser.parse_args([])
usage: PROG [-h] (--foo | --bar)
PROG: error: one of the arguments --foo --bar is required
```

注意，目前互斥参数组不支持 [`add_argument_group()`](https://docs.python.org/zh-cn/3.6/library/argparse.html#argparse.ArgumentParser.add_argument_group) 的 *title* 和 *description* 参数。



## Parser defaults

 `ArgumentParser.set_defaults`(***kwargs*) 

 `ArgumentParser.get_default`(*dest*) 



## 打印帮助

```python
ArgumentParser.print_usage(file=None)
ArgumentParser.print_help(file=None)
ArgumentParser.format_usage()
ArgumentParser.format_help()
```





## Partial parsing

 ArgumentParser.parse_known_args(*args=None*, *namespace=None*) 

返回的参数中包含多余参数

```python
>>> parser = argparse.ArgumentParser()
>>> parser.add_argument('--foo', action='store_true')
>>> parser.add_argument('bar')
>>> parser.parse_known_args(['--foo', '--badger', 'BAR', 'spam'])
(Namespace(bar='BAR', foo=True), ['--badger', 'spam'])
```



## [自定义文件解析](https://docs.python.org/zh-cn/3.6/library/argparse.html#customizing-file-parsing)

 ArgumentParser.convert_arg_line_to_args(*arg_line*) 

```python
class MyArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        return arg_line.split()
    
    
with open('txt', 'rt') as file:
    arg_line = file.readline()
args = parser.convert_arg_line_to_args(arg_line)
print(parser.parse_args(args))
```



## 退出方法

- ArgumentParser.**exit**(*status=0*, *message=None*)

  This method terminates the program, exiting with the specified *status* and, if given, it prints a *message* before that.

- ArgumentParser.**error**(*message*)

  This method prints a usage message including the *message* to the standard error and terminates the program with a status code of 2.

