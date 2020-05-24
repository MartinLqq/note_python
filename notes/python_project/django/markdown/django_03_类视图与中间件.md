# ==== django 3.0 ====

# 类视图

## 类视图引入

以函数的方式定义的视图称为**函数视图**，函数视图便于理解。但是遇到一个视图对应的路径提供了多种不同HTTP请求方式的支持时，便需要在一个函数中编写不同的业务逻辑，代码可读性与复用性都不佳。

```python
 def register(request):
    """处理注册"""

    # 获取请求方法，判断是GET/POST请求
    if request.method == 'GET':
        # 处理GET请求，返回注册页面
        return render(request, 'register.html')
    else:
        # 处理POST请求，实现注册逻辑
        return HttpResponse('这里实现注册逻辑')
```

使用类视图可以将视图对应的不同请求方式以类中的不同方法来区别定义。

定义类视图需要继承自 Django 提供的父类 **View**，可使用`from django.views.generic import View`或者`from django.views.generic.base import View` 导入

```python
from django.views.generic.base import View


class RegisterView(View):

    def get(self, request):

        # return render(request, 'register.html')
        register = """
        <form action='/blog/register/' method='post'>
            用户名: <input type='text' name='username' /> <br/>
            密码: <input type='password' name='password' /> <br/>
            确认密码: <input type='password' name='password1' /> <br/>
            <input type='submit' value='提交' />
        </form>
        """
        return HttpResponse(register)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if not all([username, password, password1]):
            return HttpResponse('参数不全')
        if password != password1:
            return HttpResponse('两次输入的密码不一致')

        # 注册...
        # 注册成功, 设置 session
        request.session['username'] = username

        return HttpResponse('注册成功')
```



## 类视图使用

配置路由时，使用类视图的`as_view()`方法来添加。

```python
urlpatterns = [
    # 视图函数：注册
    # url(r'^register/$', views.register, name='register'),
    # 类视图：注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
```

## 类视图原理

```python
class View:
    
    # ...
    
    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        ...省略代码...

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            # 调用dispatch方法，按照不同请求方式调用不同请求方法
            return self.dispatch(request, *args, **kwargs)

        # ...省略代码...

        # 返回真正的函数视图
        return view


    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

# django/urls/decorators.py
class classonlymethod(classmethod):
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("This method is available only on the class, not on instances.")
        return super().__get__(instance, cls)
```



## 类视图使用装饰器

为类视图添加装饰器，可以使用 3 种方法。

为了理解方便，我们先来定义一个为函数视图准备的装饰器（在设计装饰器时基本都以函数视图作为考虑的被装饰对象），及一个要被装饰的类视图。

```python
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了,  请求路径:　%s' % request.path)
        return func(request, *args, **kwargs)
    return wrapper

class DemoView(View):
    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')
```

### a . 在URL配置中装饰

```python
urlpatterns = [
    url(r'^demo/$', my_decorator(DemoView.as_view()))
]
```

- 此种方式最简单，但因装饰行为被放置到了 url 配置中，单看视图的时候无法知道此视图还被添加了装饰器，不利于代码的完整性，不建议使用。

- **此种方式会为类视图中的所有请求方法都加上装饰器行为**（因为是在视图入口处，分发请求方式前）。

### b.  在类视图中装饰

在类视图中使用为函数视图准备的装饰器时，不能直接添加装饰器，需要使用 **method_decorator** 将其转换为适用于类视图方法的装饰器。

```python
from django.utils.decorators import method_decorator

# 为全部请求方法添加装饰器
class DemoView(View):

    @method_decorator(my_decorator)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')


# 为特定请求方法添加装饰器
class DemoView(View):

    @method_decorator(my_decorator)
    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')
```

**method_decorator 装饰器还支持使用 name 参数指明被装饰的方法**

```python
# 为全部请求方法添加装饰器
@method_decorator(my_decorator, name='dispatch')
class DemoView(View):
    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')


# 为特定请求方法添加装饰器
@method_decorator(my_decorator, name='get')
class DemoView(View):
    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')
```

为什么使用 method_decorator ?

- method_decorator 的作用是为函数视图装饰器补充第一个 self 参数，以适配类视图方法。

- 如果将装饰器本身改为可以适配类视图方法的，类似如下，则无需再使用 method_decorator。

```python
def my_decorator(func):
    def wrapper(self, request, *args, **kwargs):  # 此处增加了self
		print('自定义装饰器被调用了,  请求路径:　%s' % request.path)
        return func(self, request, *args, **kwargs)  # 此处增加了self
    return wrapper
```



### c.  构造 Mixin 扩展类

- 使用面向对象多继承的特性。

- 使用Mixin扩展类，也会为类视图的所有请求方法都添加装饰行为。

```python
class MyDecoratorMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        
        view = my_decorator(view)
        
        return view

class DemoView(MyDecoratorMixin, View):
    def get(self, request):
        return HttpResponse('response for get')

    def post(self, request):
        return HttpResponse('response for post')
```



# 内置通用(generic)类视图

- django 2.2 官方文档:  https://docs.djangoproject.com/zh-hans/2.2/topics/class-based-views/#class-based-views

```
django\views\generic\
    __init__.py
    base.py
    dates.py
    detail.py
    edit.py
    list.py
```

> 关注通用类视图的同时也要看一下那些 Mixin 类和 Basexxx 的实现,  下面不列出 Mixin 类和 Basexxx



```
# base.py
    View
    TemplateView  (TemplateResponseMixin, ContextMixin, View)
    RedirectView  (View)

# dates.py
    ArchiveIndexView  (MultipleObjectTemplateResponseMixin, BaseArchiveIndexView)
    YearArchiveView  (MultipleObjectTemplateResponseMixin, BaseYearArchiveView)
    MonthArchiveView  (MultipleObjectTemplateResponseMixin, BaseMonthArchiveView)
    WeekArchiveView  (MultipleObjectTemplateResponseMixin, BaseWeekArchiveView)
    DayArchiveView  (MultipleObjectTemplateResponseMixin, BaseDayArchiveView)
    TodayArchiveView  (MultipleObjectTemplateResponseMixin, BaseTodayArchiveView)
    DateDetailView  (SingleObjectTemplateResponseMixin, BaseDateDetailView)

# detail.py
    √ DetailView  (SingleObjectTemplateResponseMixin, BaseDetailView)

# edit.py
    ProcessFormView  (View)
    √ FormView  (TemplateResponseMixin, BaseFormView)
    √ CreateView  (SingleObjectTemplateResponseMixin, BaseCreateView)
    √ UpdateView  (SingleObjectTemplateResponseMixin, BaseUpdateView)
    √ DeleteView  (SingleObjectTemplateResponseMixin, BaseDeleteView)
    
# list.py
    √ ListView  (MultipleObjectTemplateResponseMixin, BaseListView)
```

## 示例

> 以官网一个 投票应用 作为例子:   https://docs.djangoproject.com/zh-hans/2.2/intro/tutorial06/ 

```python
"""Views based on class and functions."""

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


# https://docs.djangoproject.com/zh-hans/3.0/intro/tutorial04/#use-generic-views-less-code-is-better
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

```





## DetailView 的 UML

> Pycharm 如何生成 UML 类图 ?

```
1. 选中一个 py 文件
2. 鼠标右键, 选择 Diagrams --> Show Diagram --> Python Class Diagram
```

> 以 DetailView 的 UML 类图为例:

![django-generic-detail.py](images\django-generic-detail.py-DetailView.jpg)





# 中间件

 可以使用中间件，在 Django 处理视图的不同阶段对输入或输出进行干预。 类似 flask 的请求钩子.

## 自定义中间件

例如，在 blog 应用中新建一个 middlewares.py 文件，

### a.中间件工厂函数

```python
"""
定义一个中间件工厂函数，然后返回一个可以被调用的中间件。
中间件工厂函数需要接收一个可以调用的 get_response 对象 (BaseHandler._get_response)。
返回的中间件也是一个可以被调用的对象，并且像视图一样需要接收一个 request 对象参数，返回一个 response 对象。
"""

def simple_middleware(get_response):
    print('第一次配置和初始化的时候执行一次')

    def middleware(request):
        print('每个请求处理视图前被执行')

        response = get_response(request)

        # 此处代码会在每个请求处理视图之后被执行
        print('每个请求处理视图之后被执行')

        return response

    return middleware

```

### b.中间件类

```Python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
```



### c.  中间件类自定义其他函数

> `django\core\handlers\base.py` 中有一个  `BaseHandler` 类,  它有个 `load_middleware`  方法

在中间件类的基础上,  可以自定义 5 中钩子函数

```python
"""
1. process_request
2. process_view
3. process_response
4. process_template_response
5. process_exception

继承自 MiddlewareMixin,
不再重写 __call__ 方法了,  __init__ 方法如果没有特殊需求, 也可以不重写
"""

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """Request 预处理方法.

        Return:
            None --> 交给下一个中间件继续处理
            HttpResponse() --> 不再执行任何其它的中间件以及相应的 view,  立即返回该 HttpResponse
        """
        print(request.path)
        print('process_request')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """View 预处理方法.

        Return:
            None --> Django 将继续处理这个 request, 执行后续的中间件, 然后调用相应的 view
            HttpResponse() --> Django 将不再执行任何其它的中间件以及相应的 view, 立即返回
        """
        print('process_view')
        return None
        # return response

    def process_response(self, request, response):
        """Response 后处理方法.

        Return:
            必须返回 HttpResponse 对象.
            可以新生成一个 HttpResponse 对象来返回
        """
        print('process_response')
        return response

    def process_template_response(self, request, response):
        """在模板渲染前执行.
        Return: 返回实现了 render 方法的响应对象
        """
        print('process_template_response')
        return response

    def process_exception(self, request, exception):
        """Exception 后处理方法.

        Return:
            None --> Django 将用框架内置的异常处理机制继续处理相应 request
            HttpResponse() --> Django 将使用该 response，而短路框架内置的异常处理机制
        """
        print('process_exception')
        print('log: ', exception)
        return HttpResponse('Emm, Error!')

```



#### > 测试中间件方法的调用时机

创建一个 demo 项目,  然后创建一个 app1 应用,  定义以下视图,  写好主路由和子路由:

```python
# demo/app1/views.py
from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    """
    访问视图对应路由时, 类中间件方法的打印顺序:
        process_request
        process_view
        process_response
    """
    return HttpResponse('Hello index.')


def exc(request):
    """
    访问视图对应路由时, 类中间件方法的打印顺序:
        process_request
        process_view
        process_exception
        process_response
    """
    raise ValueError('I"m so sorry!')


def template(request):
    """
    访问视图对应路由时, 类中间件方法的打印顺序:
        process_request
        process_view
        process_template_response
        process_response
    """
    # 注: 返回 render 结果时不会走类中间件的 process_template_response,
    # 要测试它, 可以返回 TemplateResponse(), 因为这个对象具备 render 方法
    # return render(
    #     request,
    #     'app1/test.html',
    #     context={'data': 'Hello template.'}
    # )
    return TemplateResponse(
        request,
        'app1/test.html',  # 去找 app1/templates/app1/test.html
        context={'data': 'Hello template.'}
    )

```

附:  主路由

```python
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app1/', include('app1.urls'))
]
```

附:  子路由

```python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^exc$', views.exc),
    url(r'^template$', views.template),
]
```

另需注册中间件





## 注册中间件

定义好中间件后，需要在 settings.py 文件中添加注册中间件

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.my_middleware',  # 注册中间件
]
```

定义一个视图进行测试

```python
def demo_view(request):
    print('view 视图被调用')
    return HttpResponse('OK')
```

> 注：Django 运行在调试模式下，中间件 init 部分有可能被调用两次。



## 多个中间件的执行顺序

- 在请求视图被处理**前**，中间件**由上至下**依次执行
- 在请求视图被处理**后**，中间件**由下至上**依次执行

例如,   在前面类中间件的基础上再定义一个类中间件:

````python
class MyMid:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, *args, **kwargs):
        print('MyMid: process request')
        response = self.get_response(*args, **kwargs)
        print('MyMid: process response')
        return response
````

再注册 MyMid

```python
MIDDLEWARE = [
    ...
    'middlewares.mid_test1.MyMiddleware',
    'middlewares.mid_test2.MyMid',
]
```

再请求一次,  打印顺序如下

```
process_request
MyMid: process request
process_view
MyMid: process response
process_response
```









# 信号 Signal

```python
"""
django 信号的使用步骤

1. 定义信号:  在某个文件中自定义一些信号, (Signal)
2. 连接信号:  在应用的 __init__.py 下导入信号, 并连接信号 (connect)
3. 发送信号:  在需要用到自定义信号的地方(如视图中)，导入自定义信号，并发送信号 (send)

"""
```

1. 自定义信号,   如在 `demo\app1\signals\signal_test1.py` 中定一个 信号

```python
from django.dispatch import Signal

my_signal = Signal(providing_args=['arg1', 'arg2'])

```

2. 连接信号,  如在 `demo\app1\__init__.py`  中连接内置信号、自定义信号

```python
"""
连接内置信号
"""
from django.core.signals import request_finished

# 信号接收函数
def callback(sender, **kwargs):
    print("Builtin Signal: request finished!  sender: ", sender)

request_finished.connect(callback)


"""
连接自定义信号
"""
from .signals.signal_test1 import my_signal

def my_callback(sender, **kwargs):
    print("my_signal received! sender: ", sender)
    print("my_signal args: ", kwargs)
    print("my_signal done.")

my_signal.connect(my_callback)

```

3. 发送信号,  如在 `demo\app1\views.py` 中发送信号

```python
def t_signal(request):
    # sender 可传一个 obj 或 None, arg1,arg2 为定义信号时指定的参数名
    my_signal.send(sender=t_signal, arg1='Hello', arg2='Signal')
    return HttpResponse('Test signal success')
```

