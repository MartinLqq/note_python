# ==== django 3.0 ====

# 模板

## 1 配置

- 在工程中创建模板目录 templates。

- 在settings.py配置文件中修改**TEMPLATES**配置项的DIRS值：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 此处修改
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## 2 定义模板

在templates目录中新建一个模板文件，如index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{ city }}</h1>
</body>
</html>
```

## 3 模板渲染

使用 render 渲染模板

> render(request对象, 模板文件路径, 模板数据字典)

```python
from django.shortcuts import render

def index(request):
    context={'city': '北京'}
    return render(request,'index.html',context)
```



render 实际调用模板分为三步骤：

1. 找到模板
2. 定义上下文
3. 渲染模板

```python
from django.http import HttpResponse
from django.template import loader, RequestContext

def index(request):
    # 1.获取模板
    template = loader.get_template('booktest/index.html')
    # 2.定义上下文
    context = RequestContext(request, {'city': '北京'})
    # 3.渲染模板
    return HttpResponse(template.render(context))
```



## 4 模板语法

### 4.1 模板变量

变量名必须由字母、数字、下划线（不能以下划线开头）和点组成。

语法如下：

```python
{{变量}}
```

模板变量可以使python的内建类型，也可以是对象。

```python
def index(request):
    context = {
        'city': '北京',
        'adict': {
            'name': '西游记',
            'author': '吴承恩'
        },
        'alist': [1, 2, 3, 4, 5]
    }
    return render(request, 'index.html', context)
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{ city }}</h1>
    <h1>{{ adict }}</h1>
    <h1>{{ adict.name }}</h1>  注意字典的取值方法
    <h1>{{ alist }}</h1>  
    <h1>{{ alist.0 }}</h1>  注意列表的取值方法
</body>
</html>
"""
```

### 4.2 模板语句

**1）for循环：**

```python
{% for item in 列表 %}

循环逻辑
{{forloop.counter}}表示当前是第几次循环，从1开始
{%empty%} 列表为空或不存在时执行此逻辑

{% endfor %}
```

**2）if条件：**

```python
{% if ... %}
逻辑1
{% elif ... %}
逻辑2
{% else %}
逻辑3
{% endif %}
```

比较运算符：

```
==, !=, <, >, <=, >=
```

布尔运算符：

```
and, or, not
```

**注意：运算符左右两侧不能紧挨变量或常量，必须有空格。**

```python
{% if a == 1 %}  # 正确
{% if a==1 %}  # 错误
```

### 4.3 过滤器

语法如下:

- 使用管道符号|来应用过滤器，用于进行计算、转换操作，可以使用在变量、标签中。

- 如果过滤器需要参数，则使用冒号:传递参数。

  ```python
  变量|过滤器:参数
  ```

列举几个如下：

- **safe**，禁用转义，告诉模板这个变量是安全的，可以解释执行

- **length**，长度，返回字符串包含字符的个数，或列表、元组、字典的元素个数。

- **default**，默认值，如果变量不存在时则返回默认值。

  ```
  data|default:'默认值'
  ```

- **date**，日期，用于对日期类型的值进行字符串格式化，常用的格式化字符如下：

  - Y表示年，格式为4位，y表示两位的年。
  - m表示月，格式为01,02,12等。
  - d表示日, 格式为01,02等。
  - j表示日，格式为1,2等。
  - H表示时，24进制，h表示12进制的时。
  - i表示分，为0-59。
  - s表示秒，为0-59。

  ```
  value|date:"Y年m月j日  H时i分s秒"
  ```

### 4.4 注释

单行注释

```
{#...#}
```

多行注释使用comment标签

```python
{% comment %}
...
{% endcomment %}
```

### 4.5 模板继承

模板继承和类的继承含义是一样的，主要是为了提高代码重用，减轻开发人员的工作量。

**父模板**

如果发现在多个模板中某些内容相同，那就应该把这段内容定义到父模板中。

标签block：用于在父模板中预留区域，留给子模板填充差异性的内容，名字不能相同。 为了更好的可读性，建议给endblock标签写上名字，这个名字与对应的block名字相同。父模板中也可以使用上下文中传递过来的数据。

```python
{% block 名称 %}
预留区域，可以编写默认内容，也可以没有默认内容
{% endblock  名称 %}
```

**子模板**

标签 extends 写在子模板文件的第一行。

```
{% extends "父模板路径" %}
```

子模版不用填充父模版中的所有预留区域，如果子模版没有填充，则使用父模版定义的默认值。

填充父模板中指定名称的预留区域。

```
{% block 名称 %}
实际填充内容
{{ block.super }} 用于获取父模板中block的内容
{% endblock 名称 %}
```





# 表单

## 1 定义表单类

表单系统的核心部分是 Django 的 Form 类。 Django 的数据库模型描述一个对象的逻辑结构、行为以及展现给我们的方式，与此类似，Form类描述一个表单并决定它如何工作和展现。

假如我们想在网页中创建一个表单，用来获取用户想保存的图书信息，可能类似的 html 表单如下：

```html
<form action="" method="post">
    <input type="text" name="title">
    <input type="date" name="pub_date">
    <input type="submit">
</form>
```

我们可以据此来创建一个 Form 类来描述这个表单。

新建一个 **forms.py** 文件，编写 Form 类。

```python
from django import forms

class BookForm(forms.Form):
    title = forms.CharField(label="书名", required=True, max_length=50)
    pub_date = forms.DateField(label='出版日期', required=True)
```

> 注：[表单字段类型参考资料连接](https://yiyibooks.cn/xx/Django_1.11.6/ref/forms/fields.html)



## 2 视图中使用表单类

```python
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .forms import BookForm

class BookView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'book.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():  # 验证表单数据
            print(form.cleaned_data)  # 获取验证后的表单数据
            return HttpResponse("OK")
        else:
            return render(request, 'book.html', {'form': form})
```

- form.is_valid() 验证表单数据的合法性
- form.cleaned_data 验证通过的表单数据

## 3 模板中使用表单类

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>书籍</title>
</head>
<body>
    <form action="" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
</body>
</html>
```

- csrf_token 用于添加CSRF防护的字段
- form 快速渲染表单字段的方法

## 4 模型类表单

如果表单中的数据与模型类对应，可以通过继承 **forms.ModelForm** 更快速的创建表单。

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        fields = ('btitle', 'bpub_date')
```

- model 指明从属于哪个模型类
- fields 指明向表单中添加模型类的哪个字段