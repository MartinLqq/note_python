# click

- **C**ommand **L**ine **I**nterface **C**reation **K**it
- Click in three points:
  - 任意嵌套命令   arbitrary nesting of commands
  - automatic help page generation
  - supports lazy loading of subcommands at runtime



文档：

- Github： https://github.com/pallets/click
- 英文文档:     https://click.palletsprojects.com/en/7.x/
- 中文文档：  https://click-docs-zh-cn.readthedocs.io/zh/latest/



# 基本概念

Click 是通过装饰器声明命令的。在内部，高级用例有一个非装饰器接口，但不鼓励高级用法。

一个函数通过装饰器成为一个 Click 命令行工具[`click.command()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.command)。

# 嵌套命令

命令可以附加到其他 [`Group`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Group) 类型的命令。这允许任意嵌套脚本。下面例子中的脚本实现了两个管理数据库的命令：

```python
@click.group()
def cli():
    pass
 
@click.command()
def initdb():
    click.echo('Initialized the database')
 
@click.command()
def dropdb():
    click.echo('Dropped the database')
 
cli.add_command(initdb)
cli.add_command(dropdb)
```

正如你所看到的那样, [`group()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.group) 装饰器就像 [`command()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.command)装饰器一样工作, 但创建一个 [`Group`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Group) 对象，可以通过 [`Group.add_command()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Group.add_command) 赋予多个可以附加的子命令。

对于简单的脚本，也可以使用 [`Group.command()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Group.command) 装饰器自动附加和创建命令。上面的脚本可以写成这样：

```python
@click.group()
def cli():
    pass
 
@cli.command()
def initdb():
    click.echo('Initialized the database')
 
@cli.command() 
def dropdb():
    click.echo('Dropped the database')
```



# Setuptools 集成

yourscript.py

```python
import click
 
@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')
```

setup.py

> 神奇的是 `entry_points` 参数. 下面`console_scripts`, 每行标识一个控制台脚本。第一部分是在等号 (`=`) 前面的应该生成的脚本名称。第二部分是在冒号后面(`:`)的导入路径。 

```python
from setuptools import setup
 
setup(
    name='yourscript',
    version='0.1',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourscript:cli
    ''',
)
```

**安装**

- **此方法安装的好处:   如果更新了代码,  不需要先删除已安装的包再安装一次,   代码更新会直接更新到已安装的包中!**

```bash
# pip install --editable .
pip install --e .

# 查看-e 选项的作用:
# pip install --help
-e, --editable <path/url>   Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.
```

使用

```
yourscript --help
```



**包中的脚本**

如果您的脚本正在增多，并且您希望切换到包含在Python包中的脚本，那么所需的更改很少。我们假设你的目录结构变成这样:

```
yourpackage/
    __init__.py
    main.py
    utils.py
    scripts/
        __init__.py
        yourscript.py
```

在这种情况下，在 `setup.py` 文件中，使用 `pacckages` 代替 `py_modules` ，同时自动包会找到 setuptools的支持。除此之外，还建议它含其他包数据。

如下这些是对 `setup.py` 文件内容的修改:

```python
from setuptools import setup, find_packages
 
setup(
    name='yourpackage',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourpackage.scripts.yourscript:cli
    ''',
)
```





# 一、Parameter

- **parameter 和 argument 概念区分:**  
  - parameter:  形参
  - argument:  实参
- Click 支持两种类型的脚本参数:  选项和参数 (  option 和 argument  )。

- 正如其名称所示，选项是可选的。虽然参数在合理的范围内是可选的，但是它们在选择的方式上会受到更多的限制。 

## 参数(argument)与选项

参数 ( argument ) 功能略少于选项。以下功能仅适用于选项:

- 选项可自动提示缺少输入
- 选项可作为标志（布尔值或其他）
- 选项值可以从环境变量中拉出来，但参数不能
- 选项能完整记录在帮助页面中，但参数不能（这显而易见，因为参数可能过于具体而不能自动记录）
  另一方面，与选项不同，参数可以接受任意数量的参数。选项可以严格地只接受固定数量的参数（默认为1）。



## Parameter 初始化参数

```python
Parameter:

    param_decls=None,
    type=None,
    required=False,
    default=None,
    callback=None,
    nargs=None,
    metavar=None,
    expose_value=True,
    is_eager=False,
    envvar=None,
    autocompletion=None

```







## Parameter类型

```
str / click.STRING
int / click.INT
float / click.FLOAT
bool / click.BOOL
click.UUID
click.File
click.Path
click.Choice
click.IntRange
click.FloatRange
click.DateTime

click.ParamType:  自定义类型时要继承的父类
```





## Parameter名称

- 参数Parameter（包括选项和参数）都接受一些参数声明的位置参数。
- 每个带有单个短划线的字符串都被添加为短参数
- 每个字符串都以一个双破折号开始。
- 如果添加一个没有任何破折号的字符串，它将成为内部参数名称，也被用作变量名称。



- 如果一个参数没有给出一个没有破折号的名字, 那么通过采用最长的参数并将所有的破折号转换为下划线来自动生成一个名字。

- For an option with `('-f', '--foo-bar')`, the parameter name is foo_bar.
- For an option with `('-x',)`, the parameter is x.
- For an option with `('-f', '--filename', 'dest')`, the parameter name is dest.
- For an option with `('--CamelCaseOption',)`, the parameter is camelcaseoption.
- For an arguments with `(`foogle`)`, the parameter name is foogle. To provide a different human readable name for use in help text, see the section about [Truncating Help Texts](https://click.palletsprojects.com/en/7.x/documentation/#doc-meta-variables).



## 自定义类型

- 要实现一个自定义类型，你需要继承这个[`click.ParamType`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.ParamType)类类型可以调用有或没有上下文和参数对象，这就是为什么他们需要能够处理这个问题。 

- 一个子类需要实现 [`ParamType.convert()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.ParamType.convert) 方法，并且可以选择提供 [`ParamType.name`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.ParamType.name) 属性,  可用于文档的目的。 

如:  实现一个整数类 型，除了普通整数之外，还接受十六进制和八进制数字，并将它们转换为常规整数 

```python
import click

class BasedIntParamType(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except TypeError:
            self.fail(
                "expected string for int() conversion, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

BASED_INT = BasedIntParamType()
```



# 二、Option

- 通过 [`option()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.option) 装饰器可以给命令增加选项。通过配置参数来控制不同的选项。
- Click 中的选项不同于 [位置参数](https://click-docs-zh-cn.readthedocs.io/zh/latest/arguments.html#arguments)。 



## Option(Parameter) 初始化参数

- Option 继承自 Parameter

```
装饰器  @click.option(*param_decls, **attrs)

*param_decls
**attrs:
	show_default	# 是否在help信息中显示default参数指定的内容
	prompt			# 输入框, =True/str
	confirmation_prompt  # 确认输入框
	hide_input		# 是否隐藏输入框文字 (用于密码输入)
	is_flag
	flag_value
	multiple		# 多个选项, 如 git commit -m foo -m bar 会记录两行 commit 信息
	count			# 使用重复的选项来计数
	allow_from_autoenv
	help
	
	type
	required
	default
	callback
	nargs
	metavar
	expose_value
	is_eager		# eager values are processed before non eager ones
	envvar
```





## 基本的 值选项

- 默认情况下，参数的名称为第一个长选项，如果没有长选项则为第一个短选项。 

## 多个值的选项

- 通过 `nargs` 参数来配置。多个值将被放入一个元组（tuple）中。 

```python
@click.command()
@click.option('--pos', nargs=2, type=float)
def findme(pos):
    click.echo('%s / %s' % pos)
```



### 使用元组代替多个值的选项

使用 *nargs* 来设置一个每个值都是数字的选项，得到的元组（tuple）中都是一样的数字类型。这可能不是你想要的。通常情况下，你希望元组中包含不同类型的值。你可以直接使用下列的特殊元组达成目的： 

```python
@click.command()
@click.option('--item', type=(unicode, int))
def putitem(item):
    click.echo('name=%s id=%d' % item)
```



## 多个选项

和 `nargs` 类似，有时候可能会需要一个参数传递多次，同时记录每次的值而不是只记录最后一个值。比如，`git commit -m foo -m bar` 会记录两行 commit 信息：`foo` 和 `bar`。这个功能可以通过 `multiple` 参数实现：

例如:

```python
@click.command()
@click.option('--message', '-m', multiple=True)
def commit(message):
    click.echo(message)
```

在命令行中运行:

```bash
$ commit -m foo -m bar
('foo', 'bar')
$ commit --message bar -m foo
('foo', 'bar')
```



## 计数

使用重复的选项来计数

```python
@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo('Verbosity: %s' % verbose)
```

在命令行中运行:

```
$ log -vvv
Verbosity: 3
```



## 布尔值标记

- 布尔值标记用于开启或关闭选项。
- 可以通过以 `/` 分割的两个标记来实现开启或关闭选项。（如果 `/` 在一个选项名中，Click 会自动识别其为布尔值标记，隐式默认 `is_flag=True`）。
- Click 希望你能提供一个开启和关闭标记然后设置默认值。

例如:

```python
import sys
 
@click.command()
@click.option('--shout/--no-shout', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

在命令行中运行:

```bash
$ info --shout
LINUX2!!!!111
$ info --no-shout
linux2
```

如果你实在不想要一个关闭标记，你只需要定义开启标记，然后手动设置它为标记。

```python
import sys
 
@click.command()
@click.option('--shout', is_flag=True)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

在命令行中运行:

```bash
$ info --shout
LINUX2!!!!111
```

提示：如果 `/` 已经包含在你的选项名中（比如说如果你使用 Windows 风格的参数 `/` 是字符串的前缀），你可以使用 `;` 来代替 `/`。

```python
@click.command()
@click.option('/debug;/no-debug')
def log(debug):
    click.echo('debug=%s' % debug)
 
if __name__ == '__main__':
    log()
```

在 6.0 版更改.

如果你想定义一个别名作为第二个选项名，你需要开头空格消除格式化字符串时的歧义：

例如:

```python
import sys
 
@click.command()
@click.option('--shout/--no-shout', ' /-S', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

```bash
$ info --help
Usage: info [OPTIONS]
 
Options:
  --shout / -S, --no-shout
  --help                    Show this message and exit.
```





## 功能开关

另一种布尔值标记，同时也是功能开关。通过对多个选项设置同一个参数名，同时设置一个标记来实现。提示通过提供 `flag_value` 参数，Click 会自动隐式设置 `is_flag=True`。

设置一个默认值为 *True* 的默认标记。

```python
import sys
 
@click.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info(transformation):
    click.echo(getattr(sys.platform, transformation)())
```

在命令行中运行:

```bash
$ info --upper
LINUX2
$ info --lower
linux2
$ info
LINUX2
```





## 选择选项

```python
@click.command()
@click.option('--hash-type', type=click.Choice(['md5', 'sha1']))
def digest(hash_type):
    click.echo(hash_type)
```





## 提示

有时候，你想通过命令行输入没有提供的参数。通过定义一个 prompt 参数可以实现这个功能。

例如:

```python
@click.command()
@click.option('--name', prompt=True)
def hello(name):
    click.echo('Hello %s!' % name)
```

运行如下:

```bash
$ hello --name=John
Hello John!
$ hello
Name: John
Hello John!
```

如果你不喜欢默认的提示信息，你可以自己定义：

```python
@click.command()
@click.option('--name', prompt='Your name please')
def hello(name):
    click.echo('Hello %s!' % name)
```

运行如下:

```bash
$ hello
Your name please: John
Hello John!
```



## 密码提示

Click 也支持隐藏输入信息和确认，这在输入密码时非常有用：

```python
@click.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def encrypt(password):
    click.echo('Encrypting password to %s' % password.encode('rot13'))
```

运行如下:

```bash
$ encrypt
Password: 
Repeat for confirmation: 
Encrypting password to frperg
```

### @click.password_option()

因为这种情况非常普遍，因此可以直接用 **password_option()** 装饰器取代：

```python
@click.command()
@click.password_option()
def encrypt(password):
    click.echo('Encrypting password to %s' % password.encode('rot13'))
```



## 提示时获取动态的默认值

上下文中的 `auto_envvar_prefix` 和 `default_map` 选项允许程序从环境变量或者配置文件中读取选项的值。不过这会覆盖提示机制，你将不能够自主输入选项的值。

如果你想要用户自己设置默认值，同时如果命令行没有获取该选项的值仍然使用提示进行输入，你可以提供一个可供调用的默认值。比如说从环境变量中获取一个默认值：

```python
@click.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('USER', ''))
def hello(username):
    print("Hello,", username)
```

To describe what the default value will be, set it in `show_default`.

```python
@click.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('USER', ''),
              show_default='current user')
def hello(username):
    print("Hello,", username)


$ hello --help
Usage: hello [OPTIONS]

Options:
  --username TEXT  [default: (current user)]
  --help           Show this message and exit.
```



## 回调选项和优先选项

有时候，你想要一个参数去完整地改变程序运行流程。比如，你想要一个 `—version` 参数去打印出程序的版本然后退出。

提示：`—version` 参数功能真正地实现是依靠 Click 中的 [`click.version_option()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.version_option)。下面的代码只是做一个简单的展示。

在下面你例子中，你需要明白两个概念：优先参数和回调。优先参数会比其他参数优先处理，回调是参数被处理后将调用回调函数。在优先需要一个参数时优先运行是很必须要的。比如，如果 `—version` 运行前需要 `—foo` 参数，你需要让它优于 `—version` 运行。详细信息请查看 [回调评估顺序](https://click-docs-zh-cn.readthedocs.io/zh/latest/advanced.html#callback-evaluation-order)。

回调是有当前上下文 [`Context`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Context) 和值两个参数的函数。上下文提供退出程序和访问其他已经生成的参数的有用功能。

下面是一个 `—version` 的简单例子:

```python
def print_version(ctx: click.Context, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()
 
@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello():
    click.echo('Hello World!')
```

- *expose_value* 参数可以避免没有用的 `version` 参数传入回调函数中。如果没有设置它，一个布尔值将传入 *hello* 脚本中。
- *resilient_parsing* 用于在 Click 想在不影响整个程序运行的前提下解析命令行。

如下所示:

```
$ hello
Hello World!
$ hello --version
Version 1.0
```



## Yes 参数

对于一些危险的操作，询问用户是否继续是一个明智的选择。通过添加一个布尔值 `—yes` 标记就可以实现，用户如果不提供它，就会得到提示。

```python
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()
 
@click.command()
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')
```

在命令行中运行:

```bash
$ dropdb
Are you sure you want to drop the db? [y/N]: n
Aborted!
$ dropdb --yes
Dropped all tables!
```

### @click.confirmation_option()

因为这样的组合很常见，所以你可以用 [`confirmation_option()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.confirmation_option) 装饰器来实现：

```python
@click.command()
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')
```





## 从环境变量中获取值

Click 有一个非常有用的特性，除了接收常规的参数外它可以从环境变量中接收参数。这个功能可以让工具更容易自动化。比如，你可能想要通过 `—config` 参数获取配置文件，同时又想支持通过提供 `TOOL_CONFIG=hello.cfg` 键值对来获取配置文件。

Click 通过两种方式实现这种需求。一种是去自动创建选项所需的环境变量。开启这个功能需要在脚本运行时使用 `auto_envvar_prefix` 参数。每个命令和参数将被添加为以下划线分割的大写变量。如果你有一个叫做 `foo` 的子命令，它有一个叫 `bar` 的选项，且有一个叫 `MY_TOOL` 的前缀，那么变量名就叫 `MY_TOOL_FOO_BAR`。

用例:

```python
@click.command()
@click.option('--username')
def greet(username):
    click.echo('Hello %s!' % username)
 
if __name__ == '__main__':
    greet(auto_envvar_prefix='GREETER')
```

在命令行中运行:

```
$ export GREETER_USERNAME=john
$ greet
Hello john!
```

另一种是通过在选项中定义环境变量的名字来手工从特定的环境变量中获取值。

用例:

```
@click.command()
@click.option('--username', envvar='USERNAME')
def greet(username):
    click.echo('Hello %s!' % username)
 
if __name__ == '__main__':
    greet()
```

在命令行中运行:

```
$ export USERNAME=john
$ greet
Hello john!
```

在这个例子中，也可以使用列表，列表中的第一个值将被选用。



## 从环境变量中获取多个值

由于选项可以接收多个值，从环境变量中获取多个值（字符串）稍微复杂一些。Click 通过定义 type同时 `multiple` 和 `nargs` 的值需要为 `1` 以外的值，Click 会运行 [`ParamType.split_envvar_value()`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.ParamType.split_envvar_value)方法来进行分隔。

默认情况下所有的 type 都将使用空格来分割。但是 [`File`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.File) 和 [`Path`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.Path) type 是例外，它们两个都遵守操作系统的路径分割规则。在 Linux 和 OS X 的 Unix系统上，通过 (`:`) 分割，在 Windows 系统上，通过 (`;`) 分割。

用例:

```
@click.command()
@click.option('paths', '--path', envvar='PATHS', multiple=True,
              type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)
 
if __name__ == '__main__':
    perform()
```

在命令行中运行:

```
$ export PATHS=./foo/bar:./test
$ perform
./foo/bar
./test
```



## 其他前缀参数

Click 能够使用除了 `-` 以外进行分割的前缀参数。如果你想处理有斜杠 `/` 或其他类似的参数，这个特性将非常有用。注意一般情况下强烈不推荐使用，因为 Click 想要开发者尽可能地保持 POSIX 语法。但是在一些特定情况下，这个特性是很有用的：

```
@click.command()
@click.option('+w/-w')
def chmod(w):
    click.echo('writable=%s' % w)
 
if __name__ == '__main__':
    chmod()
```

在命令行中运行:

```
$ chmod +w
writable=True
$ chmod -w
writable=False
```

注意如果你想使用 `/` 作为前缀字符，如果你想要使用布尔值标记，你需要使用 `;` 分隔符替换 `/`:

```
@click.command()
@click.option('/debug;/no-debug')
def log(debug):
    click.echo('debug=%s' % debug)
 
if __name__ == '__main__':
    log()
```



## 范围选项

使用 [`IntRange`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.IntRange) type 可以获得一个特殊的方法，它和 [`INT`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.INT) type 有点像，它的值被限定在一个特定的范围内（包含两端的值）。它有两种模式：

- 默认模式（非强制模式），如果值不在区间范围内将会引发一个错误。
- 强制模式，如果值不在区间范围内，将会强制选取一个区间临近值。也就是说如果区间是 `0-5`，值为 `10` 则选取 `5`，值为 `-1` 则选取 `0`。
  例如:

```
@click.command()
@click.option('--count', type=click.IntRange(0, 20, clamp=True))
@click.option('--digit', type=click.IntRange(0, 10))
def repeat(count, digit):
    click.echo(str(digit) * count)
 
if __name__ == '__main__':
    repeat()
```

在命令行中运行:

```
$ repeat --count=1000 --digit=5
55555555555555555555
$ repeat --count=1000 --digit=12
Usage: repeat [OPTIONS]
 
Error: Invalid value for "--digit": 12 is not in the valid range of 0 to 10.
```

如果区间的一端为 `None`，这意味着这一端将不限制。



## 使用回调函数进行验证

在 2.0 版更改.

如果你想自定义验证逻辑，你可以在回调参数中做这些事。回调方法中既可以改变值又可以在验证失败时抛出错误。

在 Click 1.0 中，你需要抛出 [`UsageError`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.UsageError) 错误，但是从 Click 2.0 开始，你也可以抛出 [`BadParameter`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.BadParameter) 错误，这个错误增加了一些优点，它会自动格式化包含参数名的错误信息。

例如:

```
def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')
 
@click.command()
@click.option('--rolls', callback=validate_rolls, default='1d6')
def roll(rolls):
    click.echo('Rolling a %d-sided dice %d time(s)' % rolls)
 
if __name__ == '__main__':
    roll()
```

在命令行中运行:

```
$ roll --rolls=42
Usage: roll [OPTIONS]
 
Error: Invalid value for "--rolls": rolls need to be in format NdM
 
$ roll --rolls=2d12
Rolling a 12-sided dice 2 time(s)
```


 





# 三、Argument

## 基本参数

最基本的 option 是一个值的简单字符串参数。如果没有提供option，则使用默认值的类型。如果没有提供默认值，则类型被假定为 [`STRING`](https://click-docs-zh-cn.readthedocs.io/zh/latest/api.html#click.STRING).

例如:

```
@click.command()
@click.argument('filename')
def touch(filename):
    click.echo(filename)
```

它看起来像:

```
$ touch foo.txt
foo.txt
```





## 可变参数

## 文件参数

## 文件路径参数

## 文件安全打开

## 环境变量

## Option-Like 参数















