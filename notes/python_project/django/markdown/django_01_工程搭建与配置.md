# ==== django ====

# 文档

```
主要文档:  https://docs.djangoproject.com/zh-hans/3.0/contents/

Django2.0入门教程:  https://www.django.cn/course/show-1.html
Django博客开发教程:  https://www.django.cn/course/show-32.html
Django REST Framework教程:  https://www.django.cn/course/course-3.html
```

# django 准备工作

## > 准备环境

```bash
# 创建虚拟环境
python -m venv myenv
# 进入虚拟环境
.\myenv\Scripts\activate
# 安装 django
.\myenv\Scripts\python.exe -m pip install django==3.0
# 查看 django 版本号
.\myenv\Scripts\python.exe -m django --version
```

## > 创建项目和应用

```bash
# 创建项目
django-admin startproject proj_dj
# 创建子应用
cd proj_dj
python manage.py startapp blog
# 注册子应用
# 在 settings.py 配置文件里的 INSTALLED_APPS 选项里注册应用,
# 在列表中添加一项:  'blog.apps.BlogConfig'
# migrate 命令只会为在 INSTALLED_APPS 里声明了的应用进行数据库迁移。
```

## > 定义一个视图

```python
# blog/views.py
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    print(request)
    return HttpResponse('Hello django!')
```

## > 添加路由

> 先不考虑在子应用 blog 下新建子路由文件 urls.py,  而是直接在主路由文件 urls.py 中添加路由

```python
# proj_dj/proj_dj/urls.py
import blog.views as blog_views  # 新导入的

urlpatterns = [
    path('admin/', admin.site.urls),

    # url(r'^blog/', include('blog.urls')),  # 先不考虑使用子路由
    url(r'^blog/', blog_views.index),    # 新添加的
]
```

## > 运行本地开发服务

```bash
python manage.py runserver  # 在虚拟环境中 `python` 可能要带上路径

# 访问测试:
# http://127.0.0.1:8000/blog/
```

## > 修改本地语言与时区

```python
# 中国大陆地区使用简体中文，时区使用亚洲/上海时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

## > 测试静态文件访问

```python
# 1.修改静态文件访问配置
STATIC_URL = '/static/'  # 请求URL中对应为 /static/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),  # 本地路径对应为 xxx/static_files
]

# 2.创建 static_files 目录, 并在其下面创建 index.html, 写入简单代码.

# 3.访问测试:
# http://127.0.0.1:8000/static/index.html
```



# python manage.py 命令帮助

> python manage.py -h

```
Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]
    remove_stale_contenttypes

[django]
    check
    compilemessages
    createcachetable
    dbshell
    diffsettings
    dumpdata
    flush
    inspectdb
    loaddata
    makemessages
    makemigrations
    migrate
    sendtestemail
    shell
    showmigrations
    sqlflush
    sqlmigrate   # 接收一个迁移的名称，然后返回对应的 SQL： python manage.py sqlmigrate myapp 0001
    sqlsequencereset
    squashmigrations
    startapp
    startproject
    test
    testserver

[sessions]
    clearsessions

[staticfiles]
    collectstatic  # 当DEBUG=False工作在生产模式时，Django不再对外提供静态文件，需要是用 collectstatic 命令来收集静态文件并交由其他静态文件服务器来提供。
    findstatic
    runserver
```

## 常用命令

```bash
# 同步或者更改生成 数据库：
python manage.py makemigrations
python manage.py migrate

# 清空数据库： 
python manage.py flush

# 创建管理员： 
python manage.py createsuperuser

# 修改用户密码： 
python manage.py changepassword username

# Django项目环境终端： 
python manage.py shell
# 这个命令和 直接运行 python 进入 shell 的区别是：你可以在这个 shell 里面调用当前项目的 models.py 中的 API，对于操作数据的测试非常方便。
```





# 路由配置系统URLconf

## 0. 路由定义

一般情况下，一个 URL 是这样写的：

```
urlpatterns = [
    path(正则表达式, views视图函数，默认参数字典，别名),
]
参数说明：
1、一个正则表达式字符串
2、一个可调用对象，通常为一个视图函数或一个指定视图函数路径的字符串
3、可选的要传递给视图函数的默认参数（字典形式）
4、一个可选的name参数(别名)
```

一个简单的URLconf例子:

```python
from django.urls import path
from . import views
urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```

更多路由定义的内容见文档:   https://www.django.cn/course/show-7.html ,  大概包括:

```
path 转换器
注册自定义路径转换器
使用正则表达式
指定视图参数的默认值
错误页面处理
嵌套参数
urls分层模块化（路由分发）
捕获参数
向视图传递额外的参数
传递额外的参数给include()
url的反向解析
命名的URL模式（URL别名）
URL命名空间和include的URLconf
```





## 1. 路由定义位置

Django的主要路由信息定义在工程同名目录下的urls.py文件中，该文件是Django解析路由的入口。

每个子应用为了保持相对独立，可以在各个子应用中定义属于自己的 urls.py 来保存该应用的路由。然后用主路由文件包含各应用的子路由数据。

除了上述方式外，也可将工程的全部路由信息都定义在主路由文件中，子应用不再设置urls.py。如：

```python
from django.conf.urls import url
from django.contrib import admin
import users.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/index/$', users.views.index)
]
```

## 2. 路由解析顺序

Django在接收到一个请求时，从主路由文件中的 urlpatterns 列表中以由上至下的顺序查找对应路由规则，如果发现规则为 include 包含，则再进入被包含的urls中的urlpatterns列表由上至下进行查询。

值得关注的**由上至下**的顺序，有可能会使上面的路由屏蔽掉下面的路由，带来非预期结果。例如：

```python
urlpatterns = [
    url(r'^say', views.say),
    url(r'^sayhello', views.sayhello),
]

# 即使访问 sayhello/ 路径，预期应该进入sayhello 视图执行，但实际优先查找到了 say 路由规则也与 sayhello/ 路径匹配，实际进入了say 视图执行。

# 注:  需要注意定义路由的顺序，避免出现屏蔽效应
```



## 3. 路由命名与reverse反解析

**3.1 路由命名**

在定义路由的时候，可以为路由命名，方便查找特定视图的具体路径信息。

1) 在使用 include 函数定义路由时，可以使用 namespace 参数定义路由的命名空间，如

```python
url(r'^users/', include('users.urls', namespace='users')),
```

命名空间表示，凡是 users.urls 中定义的路由，均属于 namespace 指明的 users 名下。

**命名空间的作用：避免不同应用中的路由使用了相同的名字发生冲突，使用命名空间区别开。**

2) 在定义普通路由时，可以使用 name 参数指明路由的名字，如

```python
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^say', views.say, name='say'),
]
```



**3.2 reverse反解析**

使用reverse函数，可以根据路由名称，返回具体的路径，如：

```python
from django.core.urlresolvers import reverse  # 注意导包路径

def index(request):
    return HttpResponse("hello the world!")

def say(request):
    url = reverse('users:index')  # 返回 /users/index/
    print(url)
    return HttpResponse('say')
```

- 对于未指明namespace的，reverse(路由name)
- 对于指明namespace的，reverse(命名空间namespace:路由name)

## 4. 路径结尾斜线 / 的说明

Django 中定义路由时，通常以斜线 / 结尾，其好处是用户访问不以斜线 / 结尾的相同路径时，Django 会把用户重定向到以斜线/结尾的路径上，而不会返回 404 不存在。如

```python
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
]
```

用户访问 index 或者 index/ 网址，均能访问到index视图。

**说明：**

虽然路由结尾带 / 能带来上述好处，但是却违背了 HTTP 中 URL 表示资源位置路径的设计理念。

是否结尾带 / 以所属公司定义风格为准。



# App应用配置

在每个应用目录中都包含了apps.py文件，用于保存该应用的相关信息。

在创建应用时，Django会向apps.py文件中写入一个该应用的配置类，如

```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'
```

我们将此类添加到工程 settings.py 中的 INSTALLED_APPS 列表中，表明注册安装具备此配置属性的应用。

- **AppConfig.name** 属性表示这个配置类是加载到哪个应用的，每个配置类必须包含此属性，默认自动生成。

- **AppConfig.verbose_name** 属性用于设置该应用的直观可读的名字，此名字在Django提供的Admin管理站点中会显示，如

  ```
  from django.apps import AppConfig
  
  class UsersConfig(AppConfig):
      name = 'users'
      verbose_name = '用户管理'
  ```





# 一种查看项目当前生效配置的方式

在 DEBUG 模式下请求一个报错的视图,  页面会提示一些项目信息,  包括当前 settings 所有值

如:

```python
# views.py
def demo(request):
    assert 0

# urls.py
urlpatterns = [
    url(r'^demo/$', views.demo, name='demo'),
]
```



# 查看配置文档

官方文档:   https://docs.djangoproject.com/zh-hans/3.0/ref/settings/ 

Django2.0入门教程:全局配置settings详解:   https://www.django.cn/course/show-10.html 









