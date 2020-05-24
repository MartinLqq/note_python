# 测试代码的结构

-  功能代码 与 测试代码分离
-  源码放在`src`下，而测试则放在`tests`下。 
- 不把`mypkg`直接放在根目录下，是为了避免直接从当前路径导入 

```shell
project
├── setup.cfg
├── setup.py
├── src
│   └── mypkg
│       ├── __init__.py
│       └── something.py
└── tests
    ├── conftest.py
    ├── test_init.py
    └── test_something.py
```

- setup.py与setup.cfg

在`setup.py`的`tests_require`中，需要配置[pytest](https://pytest.org/)。 另外，也建议在`setup_requires`里配置[pytest-runner](https://pypi.python.org/pypi/pytest-runner)。

```python
from setuptools import setup

setup(
    ...
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
```

即使不配置[pytest](https://pytest.org/)，也可直接通过运行`pytest`命令来测试。 而做出以上配置后，可以通过`python setup.py pytest`命令来测试，并且不用提前安装`pytest`。

如果需要通过`python setup.py test`的形式执行测试，则需要添加`[aliases]`到`setup.cfg`。

```ini
[aliases]
test=pytest

[tool:pytest]
addopts = --verbose
python_files = tests/*
```

在`setup.cfg`中的`[tool:pytest]`块，就是对[pytest](https://pytest.org/)的配置。 也可在`pytest.ini`或`tox.ini`中，添加`[pytest]`块进行相同配置，效果一样。 不过，配在`setup.cfg`，可以在项目根目录少一个文件，孤更喜欢一些。

`addopts`是`pytest`的命令行参数，`--verbose`会让打印输出更细致。`python_files`指定了测试代码的位置。 有了这两个基本的配置，执行测试时就可以不用输入任何参数了。 后续如果有什么新的参数，也都可以配置到这里。



# pytest 测试框架



**建立于基础之上, 请花时间研究源码 !**



晏启东:  https://note.qidong.name



## 运行测试

```
1. pytest [...]
2. python -m pytest [...]
3. 在python代码中运行测试: 
	pytest.main()
	pytest.main(['-x', 'mytestdir'])
	
	# content of myinvoke.py
    import pytest
    class MyPlugin(object):
    	def pytest_sessionfinish(self):
    		print("*** test run reporting finishing")
    pytest.main(["-qq"], plugins=[MyPlugin()])

1/2 区别: 后者会将当前路径加入 sys.path
```

帮助

```shell
# show where pytest was imported from
	pytest --version
# show available builtin function arguments
	pytest --fixtures
# show help on command line and config file options
	pytest -h | --help
```

## 测试的对象

```python
By file:		pytest a/b/c.py
By dir:			pytest a/b
By node ids:	pytest test_mod.py::test_func
            	pytest test_mod.py::TestClass::test_method
By marker:		pytest -m unit
```

## 打印堆栈

主要命令:

```python
pytest --showlocals		# show local variables in tracebacks
pytest -l				# show local variables (shortcut)

pytest --full-trace
```



## 调试测试

1. `assert 0` 主动抛出异常,  查看 print 结果

   ```python
   def test_mytest():
       print("test")
       assert 0
   ```

2. `pdb.set_trace()` 设置断点

   ```python
   import pdb
   
   from pytest_mock import MockFixture
   
   def test_mytest(mocker: MockFixture):
       aa = 1
       pdb.set_trace()
       b = 2
   ```

   执行测试:

   ```python
   pytest --pdb
   pytest -x --pdb		# drop to PDB on first failure, then end test session
   pytest --pdb --maxfail=3	# drop to PDB for first three failures
   
   # 查看 pdb 命令帮助
   """
   (Pdb) help
   
   Documented commands (type help <topic>):
   ========================================
   EOF    c          d        h         list      q        rv       undisplay
   a      cl         debug    help      ll        quit     s        unt
   alias  clear      disable  ignore    longlist  r        source   until
   args   commands   display  interact  n         restart  step     up
   b      condition  down     j         next      return   tbreak   w
   break  cont       enable   jump      p         retval   u        whatis
   bt     continue   exit     l         pp        run      unalias  where
   
   Miscellaneous help topics:
   ==========================
   exec  pdb
   
   (Pdb) help a
   a(rgs)
           Print the argument list of the current function.
           
   (Pdb) mocker
   <pytest_mock.plugin.MockFixture object at 0x000002F02B0E1940>
   """
   ```



## 搜集测试持续时间

To get a list of the slowest 10 test durations:

```shell
pytest --durations=10
```

By default, pytest will not show test durations that are too small (<0.01s) unless -vv is passed on the command-line.



## 测试指定Exception

### 预期抛出某个异常 - raises方法

```python
# content of test_sysexit.py
import pytest

def f():
	raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()

# pytest -q test_sysexit.py
```

### 预期异常内容 - match参数

Similar to the `TestCase.assertRaisesRegexp` method from `unittest`

```python
import pytest

def myfunc():
	raise ValueError("Exception 123 raised")
    
def test_match():
    with pytest.raises(ValueError, match=r'.* 123 .*'):
    	myfunc()
```



测试指定 Warning

```python
import warnings
import pytest

def test_warning():
	with pytest.warns(UserWarning):
		warnings.warn("my warning", UserWarning)
```



## 使用class进行测试分组

```python
# content of test_class.py

class TestClass(object):
    
    def test_one(self):
        x = "this"
        assert 'h' in x
        
    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
        
# pytest -q test_class.py
```



## conftest.py

1. Initial test
2. Sharing fixture functions



### conftest.py 作用范围

一个工程下可以建多个 `conftest.py` 的文件，一般在工程根目录下设置的 `conftest.py` 起到全局作用。在不同子目录下也可以放 `conftest.py` 的文件，作用范围只能在该层级以及以下目录生效。

1. `conftest.py` 在不同的层级间的作用域不一样

2. `conftest.py` 不能跨模块调用





## Fixtures

### 作用

fixture区别于unnitest的传统单元测试（setup/teardown）有显著改进：

1. 有独立的命名，并通过声明它们从测试函数、模块、类或整个项目中的使用来激活。

2. 按模块化的方式实现，每个fixture都可以互相调用。

3. fixture的范围从简单的单元测试到复杂的功能测试，可以对fixture配置参数，或者跨函数function，类class，模块module或整个测试session范围。



注:  

​	根据需求,  fixtures 可以有返回值,  也可以没有返回值



### 作用域

scope参数 控制fixture的作用范围:  `session` > `module` > `class` > `function`

```python
@fixture(scope="function"):	
	# 每个 函数或方法都会调用 (默认). (每个方法, 各自用一个fixture)
@fixture(scope="class"):	
	# 每个 类调用 一次，一个类中可以有多个方法. (一个类中的多个方法, 共用同一个fixture)
@fixture(scope="module"):	
    # 每个 .py文件调用一次，该文件内有多个function和class. (一个py文件, 共用同一个fixture)
@fixture(scope="session"):	
    # 多个文件调用一次，可以跨.py文件调用，每个.py文件就是module
```

### 3 种用法

1. 函数或类里面方法直接传 fixture 的函数参数名称:  传给 `函数`,  传给 `方法`

2. 使用装饰器 `@pytest.mark.usefixtures()` : 装饰 `函数`,  装饰 `类`

3. 叠加 `usefixtures`:  使用@pytest.mark.usefixture()进行叠加,  注意叠加顺序，先执行的放底层，后执行的放上层

#### **比较: usefixtures | fixture**

1. 如果fixture有返回值，那么**usefixture无法获取到返回值**，这个是装饰器usefixture与用例直接传fixture参数的区别。

2. 当fixture需要用到return出来的参数时，只能将参数名称直接当参数传入，**不需要用到return出来的参数时**，两种方式都可以

#### 自动使用 fixture

```python
# autouse=True

@pytest.fixture(scope='module', autouse=True)
def test1():
    print('\n开始执行module')
```

在每个 test_* 方法/函数执行时,  自动执行一次 scope='function' 的 fixture.



### 内置&插件 Fixtures

```shell
# shows builtin and custom fixtures
pytest --fixtures
pytest --fixture test_a.py

cache
    Return a cache object that can persist state between testing sessions.
    cache.get(key, default)
    cache.set(key, value)
    Keys must be a ``/`` separated value, where the first part is usually the
    name of your plugin or application to avoid clashes with other cache users.
    Values can be any object handled by the json stdlib module.
capsys
    Enable capturing of writes to sys.stdout/sys.stderr and make
    captured output available via ``capsys.readouterr()`` method calls
    which return a ``(out, err)`` tuple.
    
    def test_myoutput(capsys):
        # or use "capfd" for fd-level
        print("hello")
        sys.stderr.write("world\n")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"
        assert captured.err == "world\n"
        print("next")
        captured = capsys.readouterr()
        assert captured.out == "next\n"
    
capfd
    Enable capturing of writes to file descriptors 1 and 2 and make
    captured output available via ``capfd.readouterr()`` method calls
    which return a ``(out, err)`` tuple.
monkeypatch
    The returned ``monkeypatch`` fixture provides these
    helper methods to modify objects, dictionaries or os.environ::

        monkeypatch.setattr(obj, name, value, raising=True)
        monkeypatch.delattr(obj, name, raising=True)
        monkeypatch.setitem(mapping, name, value)
        monkeypatch.delitem(obj, name, raising=True)
        monkeypatch.setenv(name, value, prepend=False)  # 临时设置环境变量
        monkeypatch.delenv(name, value, raising=True)  # 临时删除环境变量
        monkeypatch.syspath_prepend(path)
        monkeypatch.chdir(path)

tmpdir_factory
tmpdir			print(tmpdir)查看类型
tmp_path		print(tmp_path)查看类型

------------------ fixtures defined from pytest_mock.plugin -------------------
mocker
	<pytest_mock.plugin.MockFixture>
    return an object that has the same interface to the `mock` module, but
    takes care of automatically undoing all patches after each test method.
mock
    Same as "mocker", but kept only for backward compatibility.
```



`tmp_path`

```Python
def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("CONTENT")
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 
```



`caplog`

```python
def test_foo(caplog):
    caplog.set_level(logging.INFO)
    pass

def test_bar(caplog):
    with caplog.at_level(logging.INFO):
    	pass
    
def test_bar(caplog):
    with caplog.at_level(logging.CRITICAL, logger='root.baz'):
    	pass
    
def test_baz(caplog):
    func_under_test()
    for record in caplog.records:
        assert record.levelname != 'CRITICAL'
        assert 'wally' not in caplog.text
        
def test_foo(caplog):
    logging.getLogger().info('boo %s', 'arg')
    assert caplog.record_tuples == [
    	('root', logging.INFO, 'boo arg'),
    ]
    
def test_something_with_clearing_records(caplog):
    some_method_that_creates_log_records()
    caplog.clear()
    your_test_method()
    assert ['Foo'] == [rec.message for rec in caplog.records]
```







### fixtures 工厂模式

```python
@pytest.fixture
def make_customer_record():
    def _make_customer_record(name):
        return {
        "name": name,
        "orders": []
        }
	return _make_customer_record

def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

If the data created by the factory requires managing, the fixture can take care of that:

```python
@pytest.fixture
def make_customer_record():
	created_records = []
    def _make_customer_record(name):
        record = models.Customer(name=name, orders=[])
        created_records.append(record)
        return record
    yield _make_customer_record
    for record in created_records:
        record.destroy()
        
def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```



### fixtures 参数化

```python
import pytest


@pytest.fixture(scope="module", params=["111", "222"])
def fix(request):
    param = request.param
    print("SETUP modarg %s" % param)
    yield param
    print("TEARDOWN modarg %s" % param)


def test_fixture_params(fix):
    print(fix)
    assert 0
```

## mocker

mocker - **pytest_mock的fixture**

关于 `mocker` 的用法先看官方的 `unittest.mock` 教程

- [26.5. `unittest.mock` — mock object library](https://docs.python.org/3.5/library/unittest.mock.html)
- [26.6. `unittest.mock` — getting started](https://docs.python.org/3.5/library/unittest.mock-examples.html)



### mock property属性

1. property get
2. property setter
3. property deleter

```python
from pytest_mock import MockFixture

class Sugar:

    def __init__(self, dream=None):
        self.__dream = dream

    @property
    def dream(self):
        return self.__dream

    @dream.setter
    def dream(self, target):
        self.__dream = target

    @dream.deleter
    def dream(self):
        self.__dream = None

def test_prop_get(mocker: MockFixture):
    mock_sugar = mocker.patch.object(
        Sugar, 'dream',
        new_callable=mocker.PropertyMock,
        return_value='test_property_get'
    )
    sugar = Sugar()
    dream = sugar.dream
    assert dream == 'test_property_get'
    assert mock_sugar.called

def test_prop_setter(mocker: MockFixture):
    pass

def test_prop_delter(mocker: MockFixture):
    pass

```



### mock 多进程

> mock 进程池:  `multiprocessing.pool.Pool`

```python
from multiprocessing.pool import Pool
from multiprocessing import TimeoutError as PTimeoutError

mock_async = mocker.patch.object(Pool, 'apply_async')
mock_async.return_value.get.return_value = get_ret
# mock get超时异常
# mock_async.return_value.get.side_effect = PTimeoutError
mocker.patch.object(Pool, 'close')
mocker.patch.object(Pool, 'join')
```





### mock with 上下文

#### > python获取当前模块对象

```python
# __import__ lets you use a variable, but... it gets more
# complicated if the module is in a package.
__import__(__name__)

# So just go to sys modules... and hope that the module wasn't
# hidden/removed (perhaps for security), that __name__ wasn't
# changed, and definitely hope that no other module with the
# same name is now available.
class X(object):
    pass

import sys
mod = sys.modules[__name__]
mod = sys.modules[X.__class__.__module__]
```

#### > Test

```python
import sys

from pytest_mock import MockFixture


class A:
    def __enter__(self):
        # do sth, then return self
        print("In __enter__()")
        return self

    def __exit__(self, type, value, trace):
        # do sth
        print("In __exit__()")
        pass
    def func(self):
        print("in func")
        return 'func return 111'


def test_with(mocker: MockFixture):
    mock_enter = mocker.patch.object(A, '__enter__')
    mock_exit = mocker.patch.object(A, '__exit__')
    mock_enter.return_value.func.return_value = 'test11'
    with A() as a:
        result = a.func()
    assert mock_enter.called
    assert mock_exit.called
    assert result == 'test11'

```







### mock 不改变原功能

如果只是想用[MagicMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)包装一个东西，而又不想改变其功能，可以用`spy`。

```python
def test_spy_listdir(mocker):
    mock_listdir = mocker.spy(os, 'listdir')
    os.listdir()
    assert mock_listdir.called
```

与上例中的`patch.object`不同的是，上例的`os.listdir()`不会真的执行，而本例中则会真的执行。



### side_effect

- side_effect 除了可以是一个异常, 还可以是一个列表.

**问题:**

如果一个被测函数内部,  有多处调用了一个相同的外部接口,  在进行 `mock` 时, 若使用 `mock_obj.return_value = xxx`, 则会导致所有地方的返回值都一样 (很多时候不满足需求),  如何 `mock` 出不同的返回值 ??

**解决:**

使用 `side_effect`,  甚至组合 `mark.parametrize()`

**举例:**

```python
# your_module.py

def your_func():
    # first place
    other_module.func()
    ...
    # second place
    if xxx:
    	other_module.func()
        return
    ...
    # third place
    other_module.func()


# test_your_module.py
from pytest import mark
from your_module import your_func
import other_module

@mark.unit
def test_your_func(mocker):
    mock_func = mocker.patch.object(other_module, "func")
    mock_func.side_effect = [
        "ret_01",
        "ret_02",
        "ret_03"
    ]
    your_func()
    assert mock_func.call_count == 2
    # side_effect列表中的值, 
    # 会依次作为业务代码中 几处 调用的 `other_module.func()` 的return_value
    
    # 代码能走到哪里(return为止), side_effect列表中的元素就需要几个, 少了不行, 多了可以

"""
注意: 
	若`if xxx`成立, 只会使用`side_effect list`前2个元素;
	若`if xxx`不进, 也只会使用`side_effect list`前2个元素, 作为
	第1,3次 `other_module.func()` 的return_value.
"""
```

### parametrize + side_effect

```python
# test_your_module.py
from pytest import mark
from your_module import your_func
import other_module

@mark.unit
@mark.parametrize(
    "side_eff", [
        ("g1_ret1", "g1_ret2", "will not be used"),
        ("g2_ret1", "g2_ret2"),  # 对应当前被测函数, 写两个元素即可, 因为只会用到2个
        ("g3_ret1", "g3_ret2"),
        ...
    ]
)
def test_your_func(mocker, side_eff):
    mock_func = mocker.patch.object(other_module, "func")
    mock_func.side_effect = side_eff
    your_func()
```





## markers

内置markers

- `skip` - always skip a test function
- `skipif` - skip a test function if a certain condition is met
- `xfail` - produce an “expected failure” outcome if a certain condition is met
- `parametrize` to perform multiple calls to the same test function.



### @pytest.mark.parametrize

- `@pytest.fixture(params=[])` allows one to parametrize fixture functions.

- `@pytest.mark.parametrize()` allows one to define multiple sets of arguments and fixtures at the test function or class.

  ```python
  # 1. use one `@`
  @pytest.mark.parametrize(
      "param1, param2", [
          ("1+2", 3),
          ("1+2", 4),
      ]
  )
  def test_parametrize(param1, param2):
      assert eval(param1) == param2
      
  # 2. use many `@`
  @pytest.mark.parametrize("param2", [3, 4])
  @pytest.mark.parametrize("param1", ["1+2", "1+2"])
  def test_parametrize(param1, param2):
      assert eval(param1) == param2
  ```



## monkeypatch

### monkeypatch.setattr

patch the function before calling into a function which uses it

```python
# content of test_module.py

import os.path
def getssh(): # pseudo application code
	return os.path.join(os.path.expanduser("~admin"), '.ssh')

def test_mytest(monkeypatch):
    def mockreturn(path):
    	return '/abc'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    x = getssh()
    assert x == '/abc/.ssh'
```

### monkeypatch.delattr

example: preventing “requests” from remote operations

```python
# content of conftest.py
import pytest

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
	monkeypatch.delattr("requests.sessions.Session.request")
   
# This autouse fixture will be executed for each test function and it will delete the method request.session.Session.request so that any attempts within tests to create http requests will fail.
```



### monkeypatch.setenv

临时设置环境变量



### 注意

1. 不推荐 mock 掉python内置函数

```python
Be advised that it is not recommended to patch builtin functions such as open, compile, etc., because it might break pytest’s internals.

If that’s unavoidable, passing 
--tb=native
--assert=plain
--capture=no
might help although there’s no guarantee.
```

2. 一些标准库和第三方库也不推荐mock掉

**monkeypatch.context()**

```python
Mind that patching stdlib functions and some third-party libraries used by pytest might break pytest itself,

therefore in those cases it is recommended to use monkeypatch.context() to limit the patching to the block you want tested:
    
    import functools
    def test_partial(monkeypatch):
    	with monkeypatch.context() as m:
            m.setattr(functools, "partial", 3)
            assert functools.partial == 3
```



## 插件

### pytest插件有多少?

-  还可通过classifier——[Framework :: Pytest](https://pypi.org/search/?q=&o=&c=Framework+::+Pytest)——进行条件搜索。 



Finding out which plugins are active

```shell
pytest --trace-config
```

Deactivating / unregistering a plugin by name

```shell
pytest -p no:NAME

[pytest]
addopts = -p no:NAME
```

### pytest-pylint

### pytest-yapf / pytest-yapf3

From yanqidong: https://note.qidong.name/2019/01/yapf-and-isort/

在`setup.py`的`tests_require`中，或者`requirements.txt`中，添加[pytest-isort](https://github.com/moccu/pytest-isort)和~~[pytest-yapf](https://github.com/django-stars/pytest-yapf)~~（推荐使用[pytest-yapf3](https://github.com/yanqd0/pytest-yapf3)），并且安装它们。 然后，配置`setup.cfg`。

```ini
[tool:pytest]
addopts = --verbose
          --isort
          --yapf
          ...
isort_ignore = setup.py

[isort]
...

[yapf]
...
```

这里，主要是添加`--isort`和`--yapf`到已有的[pytest](https://docs.pytest.org/)配置中。 [pytest-isort](https://github.com/moccu/pytest-isort)还支持`isort_ignore`，忽略不需要检查的文件； [pytest-yapf](https://github.com/django-stars/pytest-yapf)还不支持这个功能。

配置完成后，一切尽在`pytest`。



由于[pytest-yapf](https://github.com/django-stars/pytest-yapf)完成度不高，也不再维护，因此qidong大佬fork出来重写了一份。 `3`的意思，除了区分外，也是只支持Python 3的意思。 除原先的基本功能外，增加了以下改进：

- Basic support to validate yapf.
- Fix the diff line count error and improve the performance.
- Display `YAPF-check` as the error session name.
- Display `YAPF` in `pytest --verbose`.
- Add yapf as a marker to enable `pytest -m yapf`.
- Support `yapf-ignore` to ignore specified files.
- Skip running if a file is not changed.
- **100%** test coverage.



### pytest-pep8

https://pypi.org/project/pytest-pep8/

```shell
pip install pytest-pep8
pytest --pep8
```

pytest-pep8 Configure

```
# content of setup.cfg (or pytest.ini)cfg
[pytest]
pep8ignore =
    *.py E201
    doc/conf.py ALL
pep8maxlinelength = 99
```

### pytest-flake8

https://pypi.org/project/pytest-flakes/

```shell
pip install pytest-flakes
pytest --flake8
```

pytest-flake8 Configure

```
# content of setup.cfg
[pytest]
flakes-ignore =
    *.py UnusedImport
    doc/conf.py ALL
```

### pytest-fakes

```shell
pytest --flakes test_flakes.py
```





### pytest-docstyle

### pytest-cov

https://pytest-cov.readthedocs.io/en/latest/

[pytest-cov](https://pypi.org/pypi/pytest-cov)是自动检测测试覆盖率的一个插件。

```shell
----------------- coverage: platform linux2, python 2.6.4-final-0 ------------------
Name                 Stmts   Miss  Cover
----------------------------------------
myproj/__init__          2      0   100%
myproj/myproj          257     13    94%
myproj/feature4286      94      7    92%
----------------------------------------
TOTAL                  353     20    94%
```

使用时，需要在测试命令后加`--cov`参数，例如：

```sh
pytest --cov=myproj tests/
```

其中，`myproj`需要替换成被测试模块名。

测试覆盖率，可以说是成功、失败以外，最重要的测试数据。 100%测试覆盖率，只是完成Python项目单元测试的一个基本要求。 因此，这个插件几乎是必选的。

```shell
pytest -m unit
coverage report
coverage report -m  # 同时查看哪些行未被覆盖
```



### pytest-mock

mock更多内容详见 [docs.python.org](docs.python.org) 的 `unittest.mock`

```python
mock可替代对象:
    1. modules
    2. functions
        1> builtins func
        2> user defined func
        3> decorator
    3. class
    4. methods
    5. attributes
    6. property
    7. property setter
    8. objects in multiprocessing, multi threads

Mock/MagicMock参数:
    return_value
    side_effect
    wraps

pytest-mock中的 mocker:
    @pytest.mark.unit
    def test_a(mocker: MockFixture):
        pass
```



### pytest-datadir

https://pypi.org/project/pytest-datadir/

```python
"""
pytest-datadir will look up for a directory with the name of your module or the global 'data' folder:

.
├── data/
│   └── hello.txt
├── test_hello/
│   └── spam.txt
└── test_hello.py

"""

def test_read_global(shared_datadir):
    contents = (shared_datadir / 'hello.txt').read_text()
    assert contents == 'Hello World!\n'

def test_read_module(datadir):
    contents = (datadir / 'spam.txt').read_text()
    assert contents == 'eggs\n'
```



### pytest-datafiles

See many examples on:  https://pypi.org/project/pytest-datafiles/



### pytest-django

https://pytest-django.readthedocs.io/en/latest/



### pytest-timeout

https://pypi.org/project/pytest-timeout/



###  pytest-runner

https://pypi.org/project/pytest-runner/

### pytest-httpserver

**用 `pytest-httpserver` 来测试 `requests`**

From yanqidong: https://note.qidong.name/2019/01/pytest-httpserver/

在Python程序中，用[requests](http://docs.python-requests.org/)发起网络请求，是常见的操作。 但如何测试，是一个麻烦的问题。 如果是单元测试，可以用[pytest-mock](https://github.com/pytest-dev/pytest-mock)；但如果是集成测试，用Stub的思路，则可以考虑[pytest-httpserver](https://github.com/csernazs/pytest-httpserver)。

- 基本原理

利用pytest的fixture机制，为测试函数提供一个`httpserver`。 这是一个基于[werkzeug](http://werkzeug.pocoo.org/)启动（`make_server`）的真实服务，启动在当前环境中，`host:port`自动生成，默认不可见。

```python
from werkzeug.serving import make_server
```

对这个Server的特定Request，设置特定的Response，以达到测试的目的。

- 简单示例

```python
import requests
from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import RequestHandler


def test_root(httpserver: HTTPServer):
    handler = httpserver.expect_request('/')
    assert isinstance(handler, RequestHandler)
    handler.respond_with_data('', status=200)

    response = requests.get(httpserver.url_for('/'))
    assert response.status_code == 200
```

`httpserver`需要设置两方面内容，输入（Request）和输出（Response）。 先通过`expect_request`指定输入，再通过`respond_with_data`指定输出。 最后，通过`url_for`来获取随机生成Server的完整URL。

这里，仅对`/`的Request响应，返回`status=200`的Response。

如果在使用一些不方便使用fixtures的场景，可以通过`with`来使用相同功能。

```python
def test_root():
    with HTTPServer() as httpserver:
        handler = httpserver.expect_request('/')
        assert isinstance(handler, RequestHandler)
        handler.respond_with_data('', status=200)

        response = requests.get(httpserver.url_for('/'))
        assert response.status_code == 200
```

- 更多代码示例

```python
def test_status(httpserver: HTTPServer):
    uri = '/status'
    handler = httpserver.expect_request(uri)
    handler.respond_with_data('', status=302)

    response = requests.get(httpserver.url_for(uri))
    assert response.status_code == 302

def test_method(httpserver: HTTPServer):
    uri = '/method'
    handler = httpserver.expect_request(uri=uri, method='GET')
    handler.respond_with_data('', status=200)

    response = requests.get(httpserver.url_for(uri))
    assert response.status_code == 200
    response = requests.post(httpserver.url_for(uri))
    assert response.status_code == 500

def test_respond_with_data(httpserver: HTTPServer):
    uri = '/data'
    handler = httpserver.expect_request(
        uri=uri,
        method='POST',
    )
    handler.respond_with_data('good')

    response = requests.post(httpserver.url_for(uri))
    assert response.status_code == 200
    assert response.content == b'good'

def test_respond_with_json(httpserver: HTTPServer):
    uri = '/data'
    expect = {'a': 1, 'b': 2}
    handler = httpserver.expect_request(
        uri=uri,
        method='POST',
    )
    handler.respond_with_json(expect)
    handler.respond_with_data

    response = requests.post(httpserver.url_for(uri))
    assert response.status_code == 200
    assert expect == response.json()
```

以上的几个测试函数，展示了一些常用的手段：

- 不同`uri`
- 指定[HTTP response status codes](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)
- 指定[HTTP request methods](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods)
- 指定返回的内容（Content）
- 指定返回内容为 `JSON`
- 未指定Response的，统一返回状态码500





### 插件配合  setup.py /  setup.cfg

From yanqidong: https://note.qidong.name/2018/04/pytest-plugins/

`setup.py`文件示例片段如下：

```python
setup(
    ...
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pep8',
        'pytest-flakes',
    ],
    ...
)
```

这里主要是指明这些插件的安装需要。 在执行`./setup.py test`时，这些包会自动安装。

`setup.cfg`文件示例片段如下：

```ini
[tool:pytest]
addopts = --verbose
          --cov myproj
          --pep8
          --flakes
python_files = tests/*
pep8ignore = setup.py ALL
flakes-ignore = tests/* ALL
                **/__init__.py UnusedImport
```

其中，`myproj`需要替换成被测试模块名。 `addopts`的配置是关键，指定了会参与执行的插件。 `pep8ignore`是指定不需要执行[pytest-pep8](https://pypi.org/pypi/pytest-pep8)的文件列表，这里以`setup.py`举例（实战中`setup.py`通常不需要忽略）。

`flakes-ignore`是指定不需要执行[pytest-flakes](https://pypi.org/pypi/pytest-flakes)的文件列表。 通常测试代码都都不需要执行，因为[pytest](https://github.com/pytest-dev/pytest)的测试代码（尤其是fixtures）不一定符合[pyflakes](https://pypi.org/pypi/pyflakes)的标准。 而`__init__.py`文件有时会包含不在当前文件使用的`import`语句，所以需要指定不检查`UnusedImport`。

无论`pep8ignore`还是`flakes-ignore`，都可以精确指定不检查的错误类型，像`UnusedImport`。 具体的错误类型，可以参考测试的错误提示。



## 自定义插件

cookiecutter-pytest-plugin:   https://github.com/pytest-dev/cookiecutter-pytest-plugin

[用cookiecutter来创建新项目](https://note.qidong.name/2018/10/cookiecutter/)



https://docs.pytest.org/en/latest/writing_plugins.html#setuptools-entry-points



插件类别:

- `builtin plugins`: loaded from pytest’s internal _pytest directory.
- `external plugins`: modules discovered through setuptools entry points,  `pip-installable plugins`
- `conftest.py plugins`: modules auto-discovered in test directories

插件查找顺序:

1. 内置插件
2. `setuptools entry points` 指明的插件
3. 命令行指定插件
4. 所有 `conftest.py` 中定义的插件





# setup/teardown

 为了兼容[unittest](https://docs.python.org/3/library/unittest.html)而保留，并非[pytest](https://pytest.org/)推荐的写法 ,  有4种层级 (作用域).

 [pytest](https://pytest.org/)独创的 `fixture` 写法可以完美实现这类场景 .

```python
# 1. module
def setup_module(module):
    pass

def teardown_module(module):
    pass

# 2. function
def setup_function(function):
    pass

def teardown_function(function):
    pass

class TestSomething:
    
    # 3. class
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
	
    # 4. method
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

# 在pytest的3.0版本以后，参数module、function、method 可以去掉。
```





# 命令行添加默认选项

有2种方式给 `pytest` 命令执行时添加默认选项

1. 写入配置文件

```python
# content of `pytest.ini` or `tox.ini`
# `setup.cfg` files should use `[tool:pytest]` section instead
[pytest]
addopts = -ra -q
    --pylint
    --yapf3
    --pep8
    ...
```

2. 写入环境变量 `PYTEST_ADDOPTS`

```shell
export PYTEST_ADDOPTS="-v"
```



