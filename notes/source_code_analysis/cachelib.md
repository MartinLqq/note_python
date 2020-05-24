# cachelib

# 基本介绍

 A collection of cache libraries in the same API interface. Extracted from werkzeug. 

通过相同的接口调用各种不同的 缓存库

1. 基于文件的缓存:  FileSystemCache
2. 基于 memcached 的缓存:  MemcachedCache
3. 基于 redis 的缓存:  RedisCache
4. SimpleCache
5. UWSGICache

# 资源

# 使用方法

## 使用本地文件进行缓存

```python
from appdirs import user_cache_dir
from cachelib import FileSystemCache, NullCache

CACHE_DIR = user_cache_dir(appname='MyTest', appauthor='Lqq', version='1.0')
print(CACHE_DIR)
CACHE_ENTRY_MAX = 128
CACHE_EMPTY_VAL = "NULL"

if os.getenv('MY_DISABLE_CACHE'):
    cache = NullCache()  # works like an always empty cache
else:
    cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)

def get_by_cache_first(key):
    val = cache.get(key)
    if val:
        return val
    # 没有缓存, 或缓存已失效 --> 再次去获取真实数据
    data = fetch_data()
    cache.set(key, val)
    return data

def fetch_data():
    pass
        
def _clear_cache():
    global cache
    if not cache:
        cache = FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, 0)
    return cache.clear()  # 清理缓存, 并返回是否成功: True/False

def main():
    data = get_by_cache_first()
```

## 使用 memecache

### 服务端 memecached 下载, 安装, 使用

memecached 下载, 安装, 使用 请先学习菜鸟教程,  下面仅列出部分使用命令

- memcache 菜鸟教程:  https://www.runoob.com/memcached/window-install-memcached.html

- ```bash
  # 1.下载 memcached
  # 如: 64位系统 1.4.4版本,  http://static.runoob.com/download/memcached-win64-1.4.4-14.zip
  
  cd G:\工具安装\memcached
  
  # 查看帮助
  .\memcached.exe -h
  
  # 2. 安装 memcached, 需要管理员权限
  .\memcached.exe -d install
  
  # 3. 启动
  .\memcached.exe -d start -p 11211 -l 127.0.0.1
  
  # 停止
  .\memcached.exe -d stop
  ```

### 客户端 memecache 使用

1. 通过 telnet 命令行使用 memcached

   ```bash
   # 连接
   telnet 127.0.0.1 11211
   # 命令参考
   # Memcached调试参数&常用命令:  https://blog.csdn.net/codetomylaw/article/details/43015295
   
   # 一些命令
       # 存储命令   set/add/replace/append/prepend/cas
           set无论如何都进行存储
           add只有数据不存在时进行添加
           repalce只有数据存在时进行替换
           append往后追加：append <key> datablock <status>
           prepend往前追加：prepend <key> datablock <status>
           cas按版本号更改
   
       # 读取命令   get=bget?/gets
       # 删除命令   delete
       # 计数命令   incr/decr
       # 统计命令   stats/settings/items/sizes/slabs
   ```

2. 通过 python api 使用 memcached

> ????  测试过通过 cachelib 使用 memcache库,  一直取不到数据.  
>
> 但是,  直接使用 memcache 库没问题.

```python
import memcache

cache = memcache.Client(['127.0.0.1:11211'], debug=True)
data = cache.get_multi(['a', 'b'])
if data:
    print(data)
else:
    print('No data')
    cache.set_multi({'a': 'A', 'b': 'B'})
```



# 一些 import

## file.py

### errno

This module makes available standard errno system symbols.  

定义了许多的符号错误码,  比如 ``ENOENT`` ("没有该目录入口") 以及 ``EPERM`` ("权限被拒绝"). 它还提供了一个映射到对应平台数字错误代码的字典

- 查看每个错误代码的含义:  https://www.cnblogs.com/madsnotes/articles/5688008.html

```python
import errno

try:
    fp = open("no.txt")
except IOError as error:
    if error.errno == errno.ENOENT:
        print("no such file")
    elif error.errno == errno.EPERM:
        print("permission denied")
    else:
        print(error.strerror, ': ', error.filename)
```



### tempfile

处理临时文件和目录

详见 tempfile 源码分析

### hashlib

hashlib 提供了常见的摘要算法，如 MD5，SHA1 等等。

- https://www.cnblogs.com/jum-bolg/p/11094156.html
- https://www.cnblogs.com/sui776265233/p/9224754.html



## memcached.py

### memcache / python3-memcached

- 推荐使用 `memcache`,  即 `python3-memcached`

Memcached is a high performance multithreaded event-based key/value cache store intended to be used in a distributed system.

**安装**

- 参考:  https://blog.csdn.net/qq_42346414/article/details/98306818

```
pip install python3-memcached
```



### pylibmc

 `pylibmc` is a client in Python for [memcached](http://memcached.org/). It is a wrapper around [TangentOrg](http://tangent.org/)’s [libmemcached](http://libmemcached.org/libMemcached.html)library. 

- 文档:  http://sendapatch.se/projects/pylibmc/
- github:  https://github.com/lericson/pylibmc

**划重点**

```
如果你在Windows上进行开发，请注意，不要使用pylibmc这个库，不然会出现很多报错，如缺少C++、缺少libmemcached等等……
```



### libmc

 Fast and light-weight memcached client for C++ / #python / #golang 

- github:  https://github.com/douban/libmc

# 代码结构

## _compat.py

有关 python 版本的兼容处理

```python
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
    iteritems = lambda d, *args, **kwargs: d.iteritems(*args, **kwargs)

    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.encode(charset, errors)

else:
    text_type = str
    string_types = (str, )
    integer_types = (int, )
    iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))

    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.decode(charset, errors)
```



## BaseCache

Baseclass for the cache systems

```python
__init__(self, default_timeout=300)
get(key)
delete(key)
get_many(*keys)  # return [self.get(k) for k in keys]
get_dict(*keys)  # dict(zip(keys, self.get_many(*keys)))
set(key, value, timeout=None)  # -> bool
add(key, value, timeout=None)  # 与 set 不同, add不覆盖已存在的 key. -> bool
set_many(mapping, timeout=None)  # mapping: 映射类型, -> bool
delete_many(*keys)
has(key)
clear()
inc(key, delta=1)
        value = (self.get(key) or 0) + delta
        return value if self.set(key, value) else None
dec(key, delta=1)
        value = (self.get(key) or 0) - delta
        return value if self.set(key, value) else None
```



## NullCache

- 可用于单元测试
- 可设置环境变量, 用于确定是否使用缓存,  如果不使用,  就初始化 NullCache

```python
class NullCache(BaseCache):
    """A cache that doesn't cache.  This can be useful for unit testing.
    :param default_timeout: a dummy parameter that is ignored but exists
                            for API compatibility with other caches.
    """
    def has(self, key):
        return False
```



## FileSystemCache

- 使用本地文件系统作为缓存后端

主要关注 set 的逻辑实现

有两处应该是 bug:

1. set 方法, 下面已指明
2. get 方法, 下面已指明

```python
class FileSystemCache(BaseCache):
	def __init__(
        self,
        cache_dir,  		 # 缓存文件保存路径
        threshold=500,        # 阈值：缓存在开始删除某些项之前存储的最大项数。阈值为0表示没有阈值。
        default_timeout=300,  # 如果 set 方法没有指定 timeout, 将使用 default_timeout
        mode=0o600			 # 缓存文件的文件模式
    ):
    	# ...

    @property
    def _file_count(self):
        return self.get(self._fs_count_file) or 0

    def _update_count(self, delta=None, value=None):
        # If we have no threshold, don't count files
        if self._threshold == 0:
            return

        if delta:
            new_count = self._file_count + delta
        else:
            new_count = value or 0
        self.set(self._fs_count_file, new_count, mgmt_element=True)

    def _normalize_timeout(self, timeout):
        timeout = BaseCache._normalize_timeout(self, timeout)
        if timeout != 0:
            timeout = time() + timeout
        return int(timeout)

    def _list_dir(self):
        # 获取用户所有缓存数据对应的文件名列表
        mgmt_files = [self._get_filename(name).split('/')[-1]
                      for name in (self._fs_count_file,)]
        return [os.path.join(self._path, fn) for fn in os.listdir(self._path)
                if not fn.endswith(self._fs_transaction_suffix)
                and fn not in mgmt_files]

    def _prune(self):
        # 如果缓存数据个数超过 threshold 值, 则进行清理,  仅清理 非Management elements
        if self._threshold == 0 or not self._file_count > self._threshold:
            return

        entries = self._list_dir()
        now = time()
        for idx, fname in enumerate(entries):
            try:
                remove = False
                with open(fname, 'rb') as f:
                    expires = pickle.load(f)
                remove = (expires != 0 and expires <= now) or idx % 3 == 0

                if remove:
                    os.remove(fname)
            except (IOError, OSError):
                pass
        self._update_count(value=len(self._list_dir()))

    def clear(self):
        for fname in self._list_dir():
            try:
                os.remove(fname)
            except (IOError, OSError):
                self._update_count(value=len(self._list_dir()))
                return False
        self._update_count(value=0)
        return True

    def _get_filename(self, key):
        if isinstance(key, text_type):
            key = key.encode('utf-8')  # XXX unicode review
        hash = md5(key).hexdigest()
        return os.path.join(self._path, hash)

    def get(self, key):
        filename = self._get_filename(key)
        try:
            with open(filename, 'rb') as f:
                pickle_time = pickle.load(f)
                if pickle_time == 0 or pickle_time >= time():
                    return pickle.load(f)
                # 这里有一个 bug
                # ======== My modify start ===========
                # 源码这里的 os.remove(filename) 试图删除处于打开状态的 filename, 必有PermissionError,
                # 应该放到 with 语句执行完后
                # else:
                    # os.remove(filename)
                    # return None
            os.remove(filename)
            return None
            # ======== My modify end ===========
        except (IOError, OSError, pickle.PickleError):
            return None

    def add(self, key, value, timeout=None):
        # 仅在没有缓存过时进行缓存

    def set(self, key, value, timeout=None, mgmt_element=False):
        # Management elements have no timeout
        if mgmt_element:
            timeout = 0

        # Don't prune on management element update, to avoid loop
        else:
            self._prune()

        timeout = self._normalize_timeout(timeout)
        filename = self._get_filename(key)  # 使用 key 的 md5 值作为文件名
        try:
            # 创建一个临时文件
            fd, tmp = tempfile.mkstemp(suffix=self._fs_transaction_suffix,
                                       dir=self._path)
            # os.fdopen() 方法用于通过文件描述符 fd 创建一个文件对象
            with os.fdopen(fd, 'wb') as f:
                # 存入 timeout
                pickle.dump(timeout, f, 1)
                # 存入 value
                # 取值时, 第一次 load 获取的是 timeout, 第二次 load 获取的是 value
                pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)

            # 这里有一个 bug
            # ======== My add start ===========
            # 重复set时, 进行覆盖: 先删除, 然后重命名,
            # 否则直接 os.rename 导致异常
            if os.path.exists(filename):
                os.remove(filename)
            # ========  My add end  ===========
                
            # 重命名临时文件, 命名为 key 的 md5 值
            os.rename(tmp, filename)
            # 修改文件模式
            os.chmod(filename, self._mode)
        except (IOError, OSError):
            # set 失败
            return False
        else:
            # Management elements should not count towards threshold
            if not mgmt_element:
                # 缓存数据的个数 +1
                self._update_count(delta=1)
            return True

    def delete(self, key, mgmt_element=False):
        # 1. 删除指定 key 对应的缓存文件
        # 2. 缓存数据的个数 -1

    def has(self, key):
        # 源码逻辑类似 set, 实际上可以直接: return bool(self.get(key))

```



## MemcachedCache

- 使用 memcached 作为缓存后端,  需要 memcached 服务端,  参考标题 [使用 memcached] .

MemcachedCache 会按以下顺序选用模块,  并创建缓存客户端:

1. pylibmc
2. google.appengine.api.memcached
3. memcached
4. libmc

也可以在初始化时通过 servers 参数,  传入已创建的缓存客户端.





## RedisCache

- 使用 redis 作为缓存后端

```python
from cachelib import RedisCache

cache = RedisCache()
cache.set('my_key', 'my_val')
print(cache.get('my_key'))
```



## SimpleCache

- 使用 SimpleCache 实例属性作为存储后端
- 与一般属性不同的是, self._cache 属性字典中的 key 设置有失效时间, 且数据以 pickle 数据形式存储

```python
from cachelib import SimpleCache

cache = SimpleCache()
cache.set('k1', 'v1')
print(cache.get('k1'))
print(cache._cache)  # {'k1': (1584015023.3124013, b'xxxxx')}
```



## UWSGICache



# 扩展内容

## cacheout

- 后端使用字典进行缓存

- 使用缓存管理轻松访问多个缓存对象

- 当使用模块级缓存对象，重构运行时的缓存设置

- 最大缓存大小限制

- 默认的缓存时间设置以及缓存项自定义存活时间

- 批量的设置、获取、删除操作

- 线程安全

- 多种缓存机制的实现：
  1. FIFO(先进先出)
  2. LIFO(后进先出)
  3. LRU (最近最少使用机制)
  4. MRU (最近最多使用机制)
  5. LFU (最小频率使用机制)
  6. RR (随机替换机制)

### 资源

- github： https://github.com/dgilland/cacheout
- 文档:  https://cacheout.readthedocs.io/en/latest/

```python

import time
from cacheout.cache import Cache

cache = Cache(maxsize=256, ttl=0, timer=time.time, default=None)  # defaults
cache.set(1, 'foobar')
assert cache.get(1) == 'foobar'
assert cache.get(2, default=False) is False



# Provide a global default:
cache2 = Cache(default=True)
assert cache2.get('missing') is True
assert 'missing' not in cache2



# Memoize a function where cache keys are generated from the called function parameters:
# func(1, 2) has different cache key than func(1.0, 2.0), whereas,
# with "typed=False" (the default), they would have the same key
@cache.memoize(ttl=5, typed=True)
def func(a, b):
    pass



# Access the original memoized function:
@cache.memoize()
def func(a, b):
    pass

func.uncached(1, 2)



# Reconfigure the cache object after creation with cache.configure():
cache.configure(maxsize=1000, ttl=5 * 60)



# Manage multiple caches using CacheManager
from cacheout import CacheManager

settings = {
    'a': {'maxsize': 100},
    'b': {'maxsize': 200, 'ttl': 900},
    'c': {}
}
cacheman = CacheManager(settings, cache_class=Cache)

cacheman['a'].set('key1', 'value1')
value = cacheman['a'].get('key')

cacheman['b'].set('key2', 'value2')
assert cacheman['b'].maxsize == 200
assert cacheman['b'].ttl == 900

cacheman['c'].set('key3', 'value3')

cacheman.clear_all()
for name, cache in cacheman:
    assert name in cacheman
    assert len(cache) == 0
```



## wrapcache

一个轻量级 Python 装饰器的缓存库



### 资源

- github:  https://github.com/hustcc/wrapcache
- segmentfault:  https://segmentfault.com/a/1190000004243894



### 使用场景

经常会在某些很小的场合需要缓存一些数据，提高一些性能，而这种缓存又不是经常需要，比如：

- 两个进程共享数据库，其中只读进程读取数据做一些操作，这个时候，可以将数据库内容缓存一下，避免重复读数据库；
- 一个web页面数据太多，然而页面并不需要完全的实时性，这个时候就可以将页面内容完全缓存，在过期时间之后，不读数据库，不进行大量计算，这种在一些报告页面非常常见。

### 使用方法

```python
from time import sleep
import random

@wrapcache(timeout=60)
def need_cache_function(input, t=2, o=3):
    sleep(2)
    return random.randint(1, 100)

need_cache_function('input')
print('---------')
need_cache_function('input')
print('---------')
need_cache_function('input')
print('---------')
```

### 主要源代码

```python
def _wrap_key(function, args, kws):
	'''
	get the key from the function input.
	'''
	return hashlib.md5(pickle.dumps((function.__name__, args, kws))).hexdigest()


def wrapcache(timeout = -1, adapter = MemoryAdapter):
	'''
	the Decorator to cache Function.
	'''
	def _wrapcache(function):
		@wraps(function)
		def __wrapcache(*args, **kws):
			hash_key = _wrap_key(function, args, kws)
			try:
				adapter_instance = adapter()
				return pickle.loads(adapter_instance.get(hash_key))
			except CacheExpiredException:
				#timeout
				value = function(*args, **kws)
				set(hash_key, value, timeout, adapter)
				return value
		return __wrapcache
	return _wrapcache


class MemoryAdapter(BaseAdapter):
	'''
	use for memory cache
	'''
	def __init__(self, timeout = -1):
		super(MemoryAdapter, self).__init__(timeout = timeout)
		if MemoryAdapter.db is None:
			MemoryAdapter.db = {}

	def get(self, key):
		cache = MemoryAdapter.db.get(key, {})
		if time.time() - cache.get('time', 0) > 0:
			self.remove(key) #timeout, rm key, reduce memory
			raise CacheExpiredException(key)
		else:
			return cache.get('value', None)

	def set(self, key, value):
		cache = {
			'value' : value,
			'time'  : time.time() + self.timeout
		}
		MemoryAdapter.db[key] = cache
		return True

	def remove(self, key):
		return MemoryAdapter.db.pop(key, {}).get('value', None)

	def flush(self):
		MemoryAdapter.db.clear()
		return True
```

其他 Adaptor 见源码