# ==== django 3.0 ====

# 1.请求 HttpRequest 

需要考虑的内容:  
1. 传参方式
2. 取参方式

## HTTP 协议传参途径

```
1. URL 路径参数
	取参: 在服务器端的路由中用正则表达式截取, Django会将提取的参数直接传递到视图的传入参数中
2. 查询字符串参数
	取参: request.GET  --> QueryDict
3. 请求体 - 表单类型字符串
	取参: request.POST  --> QueryDict
4. 请求体 - 非表单类型字符串 (json / xml)
	取参: request.body  --> bytes
5. 请求头
	取参: request.headers  --> HttpHeaders 对象
```



HttpRequest 对象获取请求参数的属性

```python
request.GET   # 获取 GET/POST/... 请求中的查询字符串数据, 不区分请求方式
request.POST  # 获取请求体的表单数据, 请求方式包括 POST、PUT、PATCH、DELETE
request.body  # 获取请求体的 非表单类型二进制字符串
request.headers  #　获取请求头 headers 中的数据

# Django默认开启了 CSRF 防护，会对 POST、PUT、PATCH、DELETE 请求方式进行 CSRF 防护验证，
# 在测试时可以关闭 CSRF 防护机制，
# 在 settings.py 文件中注释掉 CSRF 中间件  django.middleware.csrf.CsrfViewMiddleware
```



### URL路径参数说明

在定义路由 URL 时，可以使用正则表达式提取参数的方法从 URL 中获取请求参数，Django 会将提取的参数直接传递到视图的传入参数中。

- 未命名参数按定义顺序传递

  ```python
  url(r'^weather/([a-z]+)/(\d{4})/$', views.weather)
  
  def weather(request, city, year):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```

- 命名参数按名字传递

  ```python
  url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather),
  
  def weather(request, year, city):
      print('city=%s' % city)
      print('year=%s' % year)
      return HttpResponse('OK')
  ```



## QueryDict 对象

- 定义在 `django.http.QueryDict`

- HttpRequest 对象的属性 GET、POST 都是 QueryDict 类型的对象

- 与 python 字典不同，QueryDict 类型的对象可以用来处理同一个键带有多个值的情况

- get()：根据键获取值

  如果一个键同时拥有多个值将获取最后一个值

  如果键不存在则返回None值，可以设置默认值进行后续处理

  ```python
  dict.get('键', 默认值)
  # 可简写为
  dict['键']
  ```

- getlist()：根据键获取值，值以列表返回，可以获取指定键的所有值

  如果键不存在则返回空列表 [ ]，可以设置默认值进行后续处理

  ```python
  dict.getlist('键', 默认值)
  ```



## HttpRequest 一些属性 / 方法

```
headers   # property, 返回 HttpHeaders 对象
get_host
get_port
get_full_path
get_full_path_info
get_signed_cookie
get_raw_uri
build_absolute_uri
scheme
is_secure
is_ajax
encoding
upload_handlers
parse_file_upload
body       # 获取请求体的 非表单类型二进制字符串
close
read
readline
__iter__
readlines
COOKIES		# 获取请求携带的 cookie
FILES		# 一个类似于字典的对象，包含所有的上传文件。
GET			# 获取 GET/POST/... 请求中的查询字符串数据, 不区分请求方式
META
POST		# 获取请求体的表单数据, 请求方式包括 POST、PUT、PATCH、DELETE
content_params
content_type
encoding
method		# 获取当前请求的请求方式
path		# 获取当前请求的请求地址
path_info
resolver_match

user		# 请求的用户对象, 默认为 AnonymousUser
```



# 2.响应 HttpResponse

- ` django.http.HttpResponse `

- ```python
  HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
  ```

- 视图在接收请求并处理后，必须返回 HttpResponse 对象或子对象。HttpRequest 对象由 Django 创建，HttpResponse 对象由开发人员创建。 



```python
# 构建响应体, content默认为 b''
HttpResponse(content=b'', content_type=None, status=None, reason=None, charset=None)

# 添加响应头,
# 可以直接将 HttpResponse 对象当做字典进行响应头键值对的设置：
response = HttpResponse('Ok')
response.status_code = 400
response['X-My-Header'] = 'Python'
```

## HttpResponse 的子类

```python
# 用于返回json数据:
JsonResponse

# 用于快速设置状态码的 HttpResponse子类
HttpResponseRedirect			# 301,  也可以直接用 django 的 redirect 函数
HttpResponsePermanentRedirect	 # 302
HttpResponseNotModified			# 304
HttpResponseBadRequest			# 400
HttpResponseNotFound 			# 404
HttpResponseForbidden 			# 403
HttpResponseNotAllowed 			# 405
HttpResponseGone 			    # 410
HttpResponseServerError 		# 500
```

# 3.Cookie

设置 cookie

```python
def demo_view(request):
    response = HttpResponse('ok')
    response.set_cookie('user', 'Martin')  # 临时cookie
    response.set_cookie('user', 'Martin', max_age=3600)  # 有效期一小时
    return response
```

获取 cookie

```python
def demo_view(request):
    cookie1 = request.COOKIES.get('user')
    print(cookie1)
    return HttpResponse('OK')
```

# 4.Session

## 启用 session

```python
# Django项目默认启用Session

# settings.py, MIDDLEWARE 列表:
# 'django.contrib.sessions.middleware.SessionMiddleware'
```



## 选择 session 存储方式并配置

1. 根据不同的 session 存储方式配置不同的 `SESSION_ENGINE`

```python
# a. 本地缓存.  如果丢失则不能找回，比数据库的方式读写更快。
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# b. 关系型数据库存储
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# c. 混合存储.   优先从本机内存中存取，如果没有则从数据库中存取。
SESSION_ENGINE='django.contrib.sessions.backends.cached_db'

# d. Redis缓存.  在redis中保存session，需要引入第三方扩展，可以使用 django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

2. 配置 session 过期时间

```python
# session有效期系统默认为两周，可以通过 SESSION_COOKIE_AGE 来设置全局默认值
SESSION_COOKIE_AGE = 60 * 60 * 24  # 1 天
```



**使用 Redis 缓存时注意**

如果redis的ip地址不是本地回环127.0.0.1，而是其他地址，访问Django时，可能出现Redis连接错误 `Connection refused`

解决方法： 修改redis的配置文件，添加特定 ip 地址。

打开redis的配置文件

```shell
#　打开redis的配置文件
sudo vim /etc/redis/redis.conf
#  修改 bind 配置, 添加具体IP（如添加一个10.211.55.5地址）
#  重启 redis
sudo service redis-server restart
```



## 操作 session

```python
# 设置
request.session['键']=值
# 获取
request.session.get('键',默认值)

# 删除session中的指定键及值，在存储中只删除某个键及对应的值。
del request.session['键']
# 清除session数据，在存储中删除session的整条数据。
request.session.flush()
# 清除所有session，在存储中删除值部分。
request.session.clear()

# 设置session的有效期
request.session.set_expiry(value)
#如果value是一个整数，session将在value秒没有活动后过期。
#如果value为0，那么用户session的Cookie将在用户的浏览器关闭时过期。
#如果value为None，那么session有效期将采用系统默认值，默认为两周，可以通过在settings.py中设置 SESSION_COOKIE_AGE 来设置全局默认值。
```

## 获取 session

```python
request.session.get('键',默认值)
```





session 操作示例

```python
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.


def index(request):
    if request.method.lower() == 'get':
        print(request.__dict__)
        return HttpResponse('Hello django!')
    else:
        return HttpResponse('Not found', status=404)

def login(request):
    if request.method.lower() == 'get':
        login_form = """
        <form action='/blog/login/' method='post'>
            用户名: <input type='text' name='username' /> <br/>
            密 码: <input type='password' name='password' /> <br/>
            <input type='submit' value='提交' />
        </form>
        """
        return HttpResponse(login_form)

    if request.method.lower() == 'post':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return HttpResponse('参数不全')
        print(username)
        print(password)
        if request.session.get('username') == username:
            return HttpResponse('已登录')
        if username != 'Martin':
            return HttpResponse('用户不存在')
        if password != '123456':
            return HttpResponse('密码错误')

        request.session['username'] = username
        return HttpResponse('login success')


def logout(request):
    if request.method.lower() != 'post':
        return HttpResponseNotFound()
    username = request.POST.get('username')
    sess_uname = request.session.get('username')
    if sess_uname and sess_uname == username:
        del request.session['username']
        return HttpResponse('退出成功')
    return HttpResponse('退出成功')

```

