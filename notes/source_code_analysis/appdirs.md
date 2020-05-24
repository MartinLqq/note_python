# appdirs

## 资源

- github:  https://github.com/ActiveState/appdirs

## 基本介绍

提供一些方法,  用于快速获取或生成本地的一些路径,  如 app 数据存储路径、缓存路径、配置文件路径......

## 使用方法

### 问题

- 你的应用app 如果要存储用户数据,  应该使用哪个路径?

What directory should your app use for storing user data? If running on macOS, you should use:

```
~/Library/Application Support/<AppName>
```

If on Windows (at least English Win XP) that should be:

```
C:\Documents and Settings\<User>\Application Data\Local Settings\<AppAuthor>\<AppName>
```

or possibly:

```
C:\Documents and Settings\<User>\Application Data\<AppAuthor>\<AppName>
```

for [roaming profiles](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-vista/cc766489(v=ws.10)) but that is another story.

```
Win 7  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
Win 7  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>
```

On Linux (and other Unices) the dir, according to the [XDG spec](https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html), is:

```
~/.local/share/<AppName>
```



### 使用 appdirs 解决问题

This kind of thing is what the `appdirs` module is for. `appdirs` will help you choose an appropriate:

- user data dir (`user_data_dir`)
- user config dir (`user_config_dir`)
- user cache dir (`user_cache_dir`)
- site data dir (`site_data_dir`)
- site config dir (`site_config_dir`)
- user log dir (`user_log_dir`)

and also:

- is a single module so other Python packages can include their own private copy
- is slightly opinionated on the directory names used. Look for "OPINION" in documentation and code for when an opinion is being applied.

### 一些输出例子

On macOS:

```python
>>> from appdirs import *
>>> appname = "SuperApp"
>>> appauthor = "Acme"

>>> user_data_dir(appname, appauthor)
'/Users/trentm/Library/Application Support/SuperApp'

>>> site_data_dir(appname, appauthor)
'/Library/Application Support/SuperApp'

>>> user_cache_dir(appname, appauthor)
'/Users/trentm/Library/Caches/SuperApp'

>>> user_log_dir(appname, appauthor)
'/Users/trentm/Library/Logs/SuperApp'
```

On Windows 7:

```python
>>> from appdirs import *
>>> appname = "SuperApp"
>>> appauthor = "Acme"

>>> user_data_dir(appname, appauthor)
'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp'
>>> user_data_dir(appname, appauthor, roaming=True)
'C:\\Users\\trentm\\AppData\\Roaming\\Acme\\SuperApp'

>>> user_cache_dir(appname, appauthor)
'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp\\Cache'

>>> user_log_dir(appname, appauthor)
'C:\\Users\\trentm\\AppData\\Local\\Acme\\SuperApp\\Logs'
```

On Linux:

```python
>>> from appdirs import *
>>> appname = "SuperApp"
>>> appauthor = "Acme"

>>> user_data_dir(appname, appauthor)
'/home/trentm/.local/share/SuperApp

>>> site_data_dir(appname, appauthor)
'/usr/local/share/SuperApp'
>>> site_data_dir(appname, appauthor, multipath=True)
'/usr/local/share/SuperApp:/usr/share/SuperApp'

>>> user_cache_dir(appname, appauthor)
'/home/trentm/.cache/SuperApp'

>>> user_log_dir(appname, appauthor)
'/home/trentm/.cache/SuperApp/log'

>>> user_config_dir(appname)
'/home/trentm/.config/SuperApp'

>>> site_config_dir(appname)
'/etc/xdg/SuperApp'

>>> os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'
>>> site_config_dir(appname, multipath=True)
'/etc/SuperApp:/usr/local/etc/SuperApp'
```

### AppDirs 类

```python
>>> from appdirs import AppDirs
>>> dirs = AppDirs("SuperApp", "Acme")
>>> dirs.user_data_dir
'/Users/trentm/Library/Application Support/SuperApp'
>>> dirs.site_data_dir
'/Library/Application Support/SuperApp'
>>> dirs.user_cache_dir
'/Users/trentm/Library/Caches/SuperApp'
>>> dirs.user_log_dir
'/Users/trentm/Library/Logs/SuperApp'
```



If you have multiple versions of your app in use that you want to be able to run side-by-side, then you may want version-isolation for these dirs:

```
>>> from appdirs import AppDirs
>>> dirs = AppDirs("SuperApp", "Acme", version="1.0")
>>> dirs.user_data_dir
'/Users/trentm/Library/Application Support/SuperApp/1.0'
>>> dirs.site_data_dir
'/Library/Application Support/SuperApp/1.0'
>>> dirs.user_cache_dir
'/Users/trentm/Library/Caches/SuperApp/1.0'
>>> dirs.user_log_dir
'/Users/trentm/Library/Logs/SuperApp/1.0'
```



## 一些 import

### ctypes

ctypes  是 Python 的外部函数库。它提供了与 C 兼容的数据类型，并允许调用 DLL 或共享库中的函数。可使用该模块以纯 Python 形式对这些库进行封装。  

- https://docs.python.org/zh-cn/3.7/library/ctypes.html
- https://blog.csdn.net/mfq1219/article/details/81945448

### winreg

python 通过 winreg API 访问 Windows 注册表

- https://docs.python.org/zh-cn/3/library/winreg.html

```python
    if PY3:
      import winreg as _winreg
    else:
      import _winreg
```

### pywin32 

pywin32 是 Microsoft Windows 的 Python 扩展,   提供了对大部分Win32 API的访问、创建和使用COM对象的能力以及Pythonwin 环境

pywin32 是 Windows平台Python编程必会模块

- github pywin32:  https://github.com/mhammond/pywin32
- https://www.cnblogs.com/achillis/p/10462585.html

#### win32com

#### win32api



## 代码结构

仅有一个 appdirs.py,  包含 7 个函数, 1 个 AppDirs 类.

### py版本兼容, 系统兼容

- 代码开头和一些函数内部做了一些 py版本兼容、平台兼容、导包兼容

```python
PY3 = sys.version_info[0] == 3

if PY3:
    unicode = str  # python3的unicode字符串方法

if sys.platform.startswith('java'):  # java平台
    import platform
    os_name = platform.java_ver()[3][0]
    if os_name.startswith('Windows'): # "Windows XP", "Windows 7", etc.
        system = 'win32'
    elif os_name.startswith('Mac'): # "Mac OS X", etc.
        system = 'darwin'
    else: # "Linux", "SunOS", "FreeBSD", etc.
        # Setting this to "linux2" is not ideal, but only Windows or Mac
        # are actually checked for and the rest of the module expects
        # *sys.platform* style strings.
        system = 'linux2'
else:   # 一般走这个分支, 如 windows 上 sys.platform == 'win32'
    system = sys.platform
```



### 函数

```python
user_data_dir(appname=None, appauthor=None, version=None, roaming=False)
site_data_dir(appname=None, appauthor=None, version=None, multipath=False)
user_config_dir(appname=None, appauthor=None, version=None, roaming=False)
site_config_dir(appname=None, appauthor=None, version=None, multipath=False)
user_cache_dir(appname=None, appauthor=None, version=None, opinion=True)
user_state_dir(appname=None, appauthor=None, version=None, roaming=False)
user_log_dir(appname=None, appauthor=None, version=None, opinion=True)

# 私有函数
_get_win_folder_from_registry(csidl_name)
_get_win_folder_with_pywin32(csidl_name)
_get_win_folder_with_ctypes(csidl_name)
_get_win_folder_with_jna(csidl_name)
```



### 类

```python
AppDirs()
# 提供多个 property 属性,  间接访问上面的各个函数
```



### user_data_dir() 例子

```python
from appdirs import user_data_dir

print(user_data_dir())  # C:\Users\Administrator\AppData\Local
user_data_dir = user_data_dir(
    appname='MyPython', appauthor='Lqq', version='1.0', roaming=True
)
print(user_data_dir)    # C:\Users\Administrator\AppData\Roaming\Lqq\MyPython\1.0
```