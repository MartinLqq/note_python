# Flask框架  02-模版

-  jinja2 中变量代码块和控制代码块的格式
-  模板中字典，列表的取值方式
-  数组反转的自定义过滤器（使用1种方式即可）
-  Flask中模板代码复用的三种方式
-  模板继承的功能
-  在模板中直接使用的 Flask 变量和函数
-  使用 Flask-WTF 扩展实现注册表单
-  CSRF 攻击的原理


####  

## 1  Jinja2模版引擎

### 1.1 什么是模版 ?

**— 视图函数** 的作用有:  `处理业务逻辑` 和 `返回简单的响应内容`。
— 在大型应用中，如果把业务逻辑和表现内容放在一起，会增加代码的复杂度和维护成本。
— 这时就需要用到**模板**，模板的作用即是承担视图函数的另一个作用，即 `返回响应内容`。

- 模板其实是一个包含响应文本的文件，其中用`占位符 (变量) `表示`动态部分`，告诉模板引擎其具体的值需要从使用的数据中获取
- **渲染**:  使用真实值替换变量，再返回最终得到的字符串，这个过程称为 `渲染`
- Flask 是使用` Jinja2` 这个模板引擎来渲染模板



使用模板的好处：

- 视图函数只负责业务逻辑和数据处理(业务逻辑方面)
- 而模板则取到视图函数的数据结果进行展示(视图展示方面)
- 代码结构清晰，耦合度低



### 1.2 Jinja2 模版引擎

- 模板语言：是一种被设计来自动生成文档的简单文本格式，在模板语言中，一般都会把一些变量传给模板，替换模板的特定位置上预先定义好的占位变量名。


- Jinja2：是 Python 下一个被广泛应用的模板引擎，是**由Python实现**的模板语言，他的**设计思想来源于 Django 的模板引擎**，并扩展了其语法和一系列强大的功能，其是 Flask 内置的模板语言。




#### 渲染模版函数 render_template( )

- 渲染模版函数的参数

  render_template(`"模板的文件名"`, `键值对1`, `键值对2`, `键值对3`)

  多个键值对 表示模板中变量对应的真实值



- `{{ }}` 来表示 **变量名**，这种 {{ }} 语法叫做 **变量代码块**

```
<h1>{{ post.title }}</h1>
```

Jinja2 模版中的变量代码块可以是任意 Python 类型或者对象，只要它能够被 Python 的 `str() `方法转换为一个字符串就可以，比如，可以通过下面的方式显示一个字典或者列表中的某个元素:

```
{{your_dict['key']}}
{{your_list[0]}}
```



- 用 **`{% %}`** 定义的 **控制代码块**，可以实现一些语言层次的功能，比如 `循环` 或者 `if语句`
- 2 个 '%' 替换了一个 { }
- 控制代码块后面可以有 {% else %} ,    if 语句结束时必须有 `{% endif %}`,   for语句结束时必须有 `{% endfor %}`

```
{% if user %}
    {{ user }}
{% else %}
    hello!
<ul>
    {% for index in indexs %}
    <li> {{ index }} </li>
    {% endfor %}
</ul>
```



- 使用 `{# #}` 进行注释，注释的内容不会在html中被渲染出来

```
{# {{ name }} #}
```

####   

## 2 模板的使用

### 2.1 模板文件默认存放目录

- 在项目下创建 `templates` 文件夹，用于存放所有的模板文件，并在目录下创建一个模板html文件 `temp_demo1.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
我的模板html内容
</body>
</html>
```



### 2.2 设置模板目录属性 - py智能提示

- 设置 templates 文件夹属性以便能够在代码中有 **智能提示**

![设置模板目录属性](.\Flask框架__02_images\设置模板目录属性.png)



### 2.3 设置模板语言 - html智能提示

- 设置 html 中的模板语言，以便在 html 有智能提示

![设置模板语言](.\Flask框架__02_images\设置模板语言.png)



### 2.4 使用模板

- 创建视图函数，将该模板内容进行渲染返回

```
@app.route('/')
def index():
    return render_template('temp_demo1.html')
```

- 代码中传入字符串，列表，字典到模板中

```python
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/demo1')
def demo1():

    # 往模板中传入数据
    # todo 只要数据能够被 Python 的 str()方法转换为一个字符串, 就可以传去模板
    my_name = "john"
    my_age = 18
    my_hobby = ["game", "film", "code"]
    my_food = {"fruits": "watermelon", 
               "vegetables": "qiezi"}
    my_hobby2 = {"game", "film", "code"}  # 集合
    my_hobby3 = ("game", "film", "code")  # 元组

    return render_template('temp_demo1.html',
                           name=my_name,
                           age=my_age,
                           hobby=my_hobby,
                           food=my_food,
                           my_hobby2=my_hobby2,
                           my_hobby3=my_hobby3
                           )


if __name__ == '__main__':
    app.run(debug=True)
```

- 模板中代码

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>模板的使用</title>
</head>
<body>
    {{ name }}<br />
    {{ name, age }}<br />

    food：{{ food }}<br /><br />
    fruits: {{ food['fruits'] }} <br>
    fruits: {{ food.fruits }} <br><br>

    hobby：{{ hobby }}<br />
    hobby-字典： {{ hobby[0] }}  <br>
    hobby-集合:  {{ my_hobby2 }} <br>

    hobby-元组:
    {{ my_hobby3[0] }}<br><br>

    计算: 年龄加10= {{ age + 10 }}<br>

</body>
</html>
```

- 页面渲染结果

  ```
  john
  ('john', 18)
  food：{'fruits': 'watermelon', 'vegetables': 'qiezi'}

  fruits: watermelon 
  fruits: watermelon 

  hobby：['game', 'film', 'code']
  hobby-字典： game 
  hobby-集合: {'game', 'film', 'code'} 
  hobby-元组: game

  计算: 年龄加10= 28
  ```

  

- 其他运算，取值举例

```
<br/> my_int + 10 的和为：{{ my_int + 10 }}
<br/> my_int + my_array第0个值的和为：{{ my_int + my_array[0] }}
<br/> my_array 第0个值为：{{ my_array[0] }}
<br/> my_array 第1个值为：{{ my_array.1 }}
<br/> my_dict 中 name 的值为：{{ my_dict['name'] }}
<br/> my_dict 中 age 的值为：{{ my_dict.age }}
```

- 结果

```
my_int + 10 的和为：20 
my_int + my_array第0个值的和为：13 
my_array 第0个值为：3 
my_array 第1个值为：4 
my_dict 中 name 的值为：xiaoming 
my_dict 中 age 的值为：18
```

####    

## 3 模板中 自带过滤器

### 3.1 什么是过滤器 ?

过滤器的本质就是函数。

有时候我们不仅仅只是需要输出变量的值，我们还需要修改变量的显示，甚至格式化、运算等等，而在模板中不能直接调用 Python 中的某些方法，那么这就用到了过滤器。

使用方式：

- 过滤器的使用方式为：**变量名 | 过滤器**

   过滤器传参:

```
{{variable | filter_name(*args)}}
```

- 如果没有任何参数传给过滤器, 则可以把括号省略掉

   过滤器不传参:

```
{{variable | filter_name}}
```



### 3.2 链式调用过滤器

在 jinja2 中，过滤器是可以支持链式调用的，示例如下：

```
{{ "hello world" | reverse | upper }}
```



### 3.3 常见内建过滤器

#### 字符串操作

| 过滤器        | 作用                           | 用例                                       |
| ---------- | ---------------------------- | ---------------------------------------- |
| safe       | 禁用转义   ('<' 和 '>' 等不转义为字符实体) | <p>{{ '<em>hello</em>' \| safe }}</p>    |
| capitalize | 首字母大写                        | <p>{{ 'hello' \| capitalize }}</p>       |
| lower      | 变量值全部小写                      | <p>{{ 'HELLO' \| lower }}</p>            |
| upper      | 变量值全部大写                      | <p>{{ 'hello' \| upper }}</p>            |
| title      | 每个单词的首字母大写                   | <p>{{ 'hello world' \| title }}</p>      |
| reverse    | 字符串反转                        | <p>{{ 'olleh' \| reverse }}</p>          |
| format     | 格式化输出                        | <p>{{ '%s is %d' \| format('name',17) }}</p> |
| striptags  | 渲染之前删除值中所有的HTML标签            | <p>{{ '<em>hello</em>' \| striptags }}</p> |
| truncate   | 字符串截断                        | <p>{{ 'hello every one' \| truncate(9)}}</p> |



#### 列表操作

| 过滤器    | 作用      | 用例                                   |
| :----- | :------ | :----------------------------------- |
| first  | 取第一个元素  | <p>{{ [1,2,3,4,5,6] \| first }}</p>  |
| last   | 取最后一个元素 | <p>{{ [1,2,3,4,5,6] \| last }}</p>   |
| length | 获取列表长度  | <p>{{ [1,2,3,4,5,6] \| length }}</p> |
| sum    | 列表求和    | <p>{{ [1,2,3,4,5,6] \| sum }}</p>    |
| sort   | 列表排序    | <p>{{ [6,2,3,1,5,4] \| sort }}</p>   |



### 3.4 语句块过滤

```
{% filter upper %}
    {# 一大堆文字 #}
{% endfilter %}
```

####     

## 4 自定义 过滤器

过滤器的本质是函数。

当模板内置的过滤器不能满足需求，可以自定义过滤器。

**注意**：自定义的过滤器名称如果和内置的过滤器重名，会覆盖内置的过滤器。



### 4.1 自定义过滤器的 2 种实现方式



**———————— 需求：添加列表反转的过滤器 ————————**



#### (1) app 对象的 **add_template_filter**( )

add_template_filter ( `"函数名"`, `"自定义的过滤器名称"` )

```python
def do_listreverse(li):
    # 通过原列表创建一个新列表
    temp_li = list(li)
    # 将新列表进行返转
    temp_li.reverse()
    return temp_li

app.add_template_filter(do_listreverse,'lireverse')
```



#### (2) 装饰器方式 @app.template_filter("filter_name")

用 `装饰器` 来实现自定义过滤器， 装饰器传入的参数是自定义的过滤器名称。

```python
@app.template_filter('lireverse')
def do_listreverse(li):
    # 通过原列表创建一个新列表
    temp_li = list(li)
    # 将新列表进行返转
    temp_li.reverse()
    return temp_li
```

- 在 html 中使用该自定义过滤器

```html
<br/> my_array 原内容：{{ my_array }}
<br/> my_array 反转：{{ my_array | lireverse }}
```

- 运行结果

```
my_array 原内容：[3, 4, 2, 1, 7, 9] 
my_array 反转：[9, 7, 1, 2, 4, 3]
```



示例代码:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/demo1")
def use_template():
    num_li = [3, 1, 6, 2]
    s = "abcd"
    return render_template("temp_demo3.html", num_li=num_li, s=s)


# 自定义 模板过滤器 实现列表的反转
# 第 1 种方式
# ————————————————————————————————————————————————————————————————————
@app.template_filter("my_li_reverse")
def li_reverse(li):
    # 根据传入的列表生成一个新列表, 避免修改传入的列表
    temp = list(li)
    temp.reverse()
    return temp
# ————————————————————————————————————————————————————————————————————


# 第 2 种方式
# ————————————————————————————————————————————————————————————————————
def sec_li_reverse(li):
    # 根据传入的列表生成一个新列表, 避免修改传入的列表
    temp = list(li)
    temp.reverse()
    return temp


app.add_template_filter(sec_li_reverse, name="my_sec_li_reverse")
# ————————————————————————————————————————————————————————————————————


if __name__ == '__main__':
    app.run(debug=True)
```

####     

## 5 控制代码块

控制代码块主要包含两个：

```
- if / elif / else / endif
- for / endfor
```



### 5.1 if 语句

#### Jinja2 语法中的 if 语句

```html
>>>> 判断用户是否登录 <<<<
{%if user.is_logged_in() %}
    <a href='/logout'>Logout</a>
{% else %}
    <a href='/login'>Login</a>
{% endif %}
```



#### ***过滤器可用于 if 语句中

```html
{% if comments | length > 0 %}
    There are {{ comments | length }} comments
{% else %}
    There are no comments
{% endif %}
```



### 5.2 for 循环

- 我们可以在 Jinja2 中使用循环来迭代任何列表或者生成器函数

```
>>>> posts 由 render_template() 以键值对形式传过来, 拥有title属性, text属性 <<<<

{% for post in posts %}
    <div>
        <h1>{{ post.title }}</h1>
        <p>{{ post.text | safe }}</p>
    </div>
{% endfor %}
```

- **循环和 if 语句可以组合使用**，以模拟 Python 循环中的 continue 功能
- 下面这个循环将只会渲染 post.text 不为 None的那些 post：

```
{% for ... in ... if ... %}

{% for post in posts if post.text %}
    <div>
        <h1>{{ post.title }}</h1>
        <p>{{ post.text | safe }}</p>
    </div>
{% endfor %}
```



#### for 循环中使用的特殊变量

| 变量             | 描述                     |
| -------------- | ---------------------- |
| loop.index     | 当前循环迭代的次数（从 1 开始）      |
| loop.index0    | 当前循环迭代的次数（从 0 开始）      |
| loop.revindex  | 到循环结束需要迭代的次数（从 1 开始）   |
| loop.revindex0 | 到循环结束需要迭代的次数（从 0 开始）   |
| loop.first     | 如果是第一次迭代，为 True 。      |
| loop.last      | 如果是最后一次迭代，为 True 。     |
| loop.length    | 序列中的项目数。               |
| loop.cycle     | 在一串序列间期取值的辅助函数。见下面的说明。 |



- 在循环内部,  使用loop 特殊变量来获得关于 for 循环的一些信息
  - 比如：要是我们想知道当前被迭代的元素序号，并模拟 Python 中的 enumerate 函数做的事情，则可以使用 loop 变量的 index 属性,例如:

```
{% for post in posts%}
{{loop.index}}, {{post.title}}
{% endfor %}
```

会输出这样的结果

```
1, Post title
2, Second Post
```



- cycle 函数会在每次循环的时候, 返回其参数中的下一个元素, 可以拿上面的例子来说明:

```
{% for post in posts%}
{{loop.cycle('odd','even')}} {{post.title}}
{% endfor %}
```

- 会输出这样的结果：

```
odd Post Title
even Second Post
```



### 5.3 for/if 示例

- 实现的效果

![img](.\Flask框架__02_images\控制语句效果.png)

- 准备数据

```
# 只显示4行数据，背景颜色依次为：黄，绿，红，紫
my_list = [
    {
        "id": 1,
        "value": "我爱工作"
    },
    {
        "id": 2,
        "value": "工作使人快乐"
    },
    {
        "id": 3,
        "value": "沉迷于工作无法自拔"
    },
    {
        "id": 4,
        "value": "日渐消瘦"
    },
    {
        "id": 5,
        "value": "以梦为马，越骑越傻"
    }
]
```

- 模板代码

```html
{% for item in my_list if item.id != 5 %}
    {% if loop.index == 1 %}
        <li style="background-color: orange">{{ item.value }}</li>
    {% elif loop.index == 2 %}
        <li style="background-color: green">{{ item.value }}</li>
    {% elif loop.index == 3 %}
        <li style="background-color: red">{{ item.value }}</li>
    {% else %}
        <li style="background-color: purple">{{ item.value }}</li>
    {% endif %}
{% endfor %}
```

####     

## 6 模板代码复用

在模板中，可能会遇到以下情况：

- 多个模板具有完全相同的顶部和底部内容
- 多个模板中具有相同的模板代码内容，但是内容中部分值不一样
- 多个模板中具有完全相同的 html 代码块内容

像遇到这种情况，可以使用 JinJa2 模板中的 `宏`、`继承`、`包含`来进行实现

### 6.1 宏 - macro

对宏 (macro) 的理解：

- 把它看作 Jinja2 中的一个函数，它会返回一个模板或者 HTML 字符串
- 为了避免反复地编写同样的模板代码，出现代码冗余，可以把他们写成函数以进行重用
- 需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复
- 带参数的宏 和 不带参数的宏

#### 在当前html中使用宏 

定义宏 (函数)

```
{% macro input(name,value='',type='text') %}
    <input type="{{type}}" name="{{name}}" value="{{value}}" class="form-control">
{% endmacro %}
```

调用宏

```
{{ input('name' value='zs')}}
```

输出:

```
<input type="text" name="name" value="zs" class="form-control">
```



#### 抽取宏,  封装成html文件

- 把宏单独抽取出来，封装成html文件，其它模板中导入使用，文件名可以自定义macro.html

```
{% macro function(type='text', name='', value='') %}
	<input type="{{type}}" name="{{name}}" value="{{value}}" class="form-control">
{% endmacro %}
```

- import 导入宏,  再调用

```
{% import 'macro.html' as func %}
<form>
    {% func.function() %}
    ...
</form>
```



#### 代码演练

- 使用宏之前代码

```
<form>
    <label>用户名：</label><input type="text" name="username"><br/>
    <label>身份证号：</label><input type="text" name="idcard"><br/>
    <label>密码：</label><input type="password" name="password"><br/>
    <label>确认密码：</label><input type="password" name="password2"><br/>
    <input type="submit" value="注册">
</form>
```

- 定义宏

```
{# 定义宏，相当于定义一个函数，在使用的时候直接调用该宏，传入不同的参数就可以了   #}
{% macro input(label="", type="text", name="", value="") %}
<label>{{ label }}</label><input type="{{ type }}" name="{{ name }}" value="{{ value }}">
{% endmacro %}
```

- 使用宏

```
<form>
    {{ input("用户名：", name="username") }}<br/>
    {{ input("身份证号：", name="idcard") }}<br/>
    {{ input("密码：", type="password", name="password") }}<br/>
    {{ input("确认密码：", type="password", name="password2") }}<br/>
    {{ input(type="submit", value="注册") }}
</form>
```

- 若导入宏使用:

```
{% import 'macro.html' as func %}
<form>
	{{ func.input("用户名：", name="username") }}<br/>
    {{ func.input("身份证号：", name="idcard") }}<br/>
    {{ func.input("密码：", type="password", name="password") }}<br/>
    {{ func.input("确认密码：", type="password", name="password2") }}<br/>
    {{ func.input(type="submit", value="注册") }}
</form>
```



### 6.2 继承 - block + extends

模板继承是为了重用模板中的公共内容。一般Web开发中，继承主要使用在网站的顶部菜单、底部。这些内容可以定义在父模板中，子模板直接继承，而不需要重复书写。

- 标签定义的内容

```
{% block top %} {% endblock %}
```

- 相当于在父模板中挖个坑，当子模板继承父模板时，可以进行填充。
- 子模板使用 extends 指令声明这个模板继承自哪个模板
- 父模板中定义的块在子模板中被重新定义，在子模板中调用父模板的内容可以使用super()



#### 父模板

- **block指令**  在父模板中挖个坑

```
{% block top %}
  顶部菜单
{% endblock top %}

{% block content %}
{% endblock content %}

{% block bottom %}
  底部
{% endblock bottom %}
```



#### 子模板

- **extends指令**  声明这个模板继承自哪

```
{% extends 'base.html' %}
{% block content %}
 需要填充的内容
{% endblock content %}
```

- 模板继承使用注意点：
  - 不支持多继承
  - 不能在一个模板文件中定义多个相同名字的block标签。
  - 当在页面中使用多个block标签时，需要给结束标签起名，当多个block嵌套时，阅读性更好。




### 6.3 包含 - include

Jinja2模板中，除了宏和继承，还支持一种代码重用的功能，叫包含(Include)。它的功能是将另一个模板整个加载到当前模板中，并直接渲染。

- include的使用

```
{% include 'hello.html' %}
```

包含在使用时，如果包含的模板文件不存在时，程序会抛出**TemplateNotFound**异常，可以加上 `ignore missing` 关键字。如果包含的模板文件不存在，会忽略这条include语句。

- include 的使用加上关键字ignore missing

```
{% include 'hello.html' ignore missing %}
```

### 6.4 小结

- 宏 (Macro)、继承 (Block)、包含 (include) 均能实现代码的复用。
- 继承 (Block) 的本质是代码替换，一般用来实现多个页面中重复不变的区域。
- 宏 (Macro) 的功能类似函数，可以传入参数，需要定义、调用。
- 包含 (include) 是直接将目标模板文件整个渲染出来。


####     

## 7 模板中特有变量和函数

可以在自己的模板中访问一些 Flask 默认内置的函数和对象

### 7.1 模板中特有变量 x 4

#### config

可以从模板中直接访问Flask当前的config对象:

```
{{config.SQLALCHEMY_DATABASE_URI}}
sqlite:///database.db
```

#### request

就是flask中代表当前请求的request对象：

```
{{request.url}}
http://127.0.0.1
```

#### session

为 Flask 的session对象

```
{{session.new}}
True
```

#### g 变量

"临时的全局变量",   在视图函数中设置g变量的 name 属性的值，然后在模板中直接可以取出

```
{{ g.name }}
```



### 7.1 模板中特有函数 x 2

#### url_for()

url_for会根据传入的路由器函数名,  返回该路由对应的URL, 在模板中始终使用url_for()就可以安全的修改路由绑定的URL,  则不必担心模板中渲染出错的链接:

```
{{url_for('home')}}
/
```

如果我们定义的路由URL是带有参数的,  则可以把它们作为关键字参数传入url_for(),  Flask会把他们填充进最终生成的URL中:

```
{{ url_for('post', post_id=1)}}
/post/1
```



#### get_flashed_messages()

获取flash()返回的消息列表中的 闪现消息

这个函数会返回之前在flask中通过  flash()  传入的消息的列表，flash函数的作用很简单,  可以把由Python字符串表示的消息加入一个消息队列中，再使用get_flashed_message()函数取出它们并消费掉：

```
{% for message in get_flashed_messages() %}
    {{ message }}
{% endfor %}
```

####  

## 8 Flask-WTF表单

Web 表单是 Web 应用程序的基本功能。
表单有三个部分组成：表单标签、表单域、表单按钮。
表单允许用户输入数据，负责HTML页面数据采集，通过表单将用户输入的数据提交给服务器。
在Flask中可以使用 Flask-WTF 扩展，它封装了 WTForms，并且有验证表单数据的功能

### 8.1 WTForms支持的HTML标准字段



| 字段对象               | 说明                             |
| ------------------ | ------------------------------ |
| StringField        | 文本字段                           |
| TextAreaField      | 多行文本字段                         |
| PasswordField      | 密码文本字段                         |
| HiddenField        | 隐藏文件字段                         |
| DateField          | 文本字段，值为 datetime.date 文本格式     |
| DateTimeField      | 文本字段，值为 datetime.datetime 文本格式 |
| IntegerField       | 文本字段，值为整数                      |
| DecimalField       | 文本字段，值为decimal.Decimal         |
| FloatField         | 文本字段，值为浮点数                     |
| BooleanField       | 复选框，值为True 和 False             |
| RadioField         | 一组单选框                          |
| SelectField        | 下拉列表                           |
| SelectMutipleField | 下拉列表，可选择多个值                    |
| FileField          | 文件上传字段                         |
| SubmitField        | 表单提交按钮                         |
| FormField          | 把表单作为字段嵌入另一个表单                 |
| FieldList          | 一组指定类型的字段                      |



### 8.2 WTForms常用验证器(validators=[ ])

| 验证函数         | 说明                   |
| ------------ | -------------------- |
| DataRequired | 确保字段中有数据             |
| EqualTo      | 比较两个字段的值，常用于比较两次密码输入 |
| Length       | 验证输入的字符串长度           |
| NumberRange  | 验证输入的值在数字范围内         |
| URL          | 验证URL                |
| AnyOf        | 验证输入值在可选列表中          |
| NoneOf       | 验证输入值不在可选列表中         |



**使用 Flask-WTF 需要配置参数 SECRET_KEY**

CSRF_ENABLED是为了**CSRF（跨站请求伪造）保护**。 SECRET_KEY用来 `生成加密令牌` ，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。



### 8.3 代码验证

#### 使用前端 html 自带的表单

- 创建模板文件 `temp_register.html`，在其中直接写form表单：

```python
<form method="post">
    <label>用户名：</label><input type="text" name="username" placeholder="请输入用户名"><br/>
    <label>密码：</label><input type="password" name="password" placeholder="请输入密码"><br/>
    <label>确认密码：</label><input type="password" name="password2" placeholder="请输入确认密码"><br/>
    <input type="submit" value="注册">
</form>

{% for message in get_flashed_messages() %}
    {{ message }}
{% endfor %}
```



- 视图函数中获取表单数据验证登录逻辑

```python
@app.route('/demo1', methods=["get", "post"])
def demo1():
    if request.method == "POST":
        # 取到表单中提交上来的三个参数
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not all([username, password, password2]):
            # 向前端界面弹出一条提示(闪现消息)
            flash("参数不足")
        elif password != password2:
            flash("两次密码不一致")
        else:
            # 假装做注册操作
            print(username, password, password2)
            return "success"

    return render_template('temp_register.html')
```



#### 使用后端 Flask-WTF 实现表单

- 配置参数，关闭 CSRF 校验

```
 app.config['WTF_CSRF_ENABLED'] = False
```

> CSRF: 跨站请求伪造

##### 模板页面

```
<form method="post">
    {{ form.username.label }} {{ form.username }}<br/>
    {{ form.password.label }} {{ form.password }}<br/>
    {{ form.password2.label }} {{ form.password2 }}<br/>
    {{ form.submit }}
</form>
```

##### 视图函数

```python
from flask import Flask,render_template, flash, request

from flask_wtf import FlaskForm   # 导入wtf扩展的[表单类]
from wtforms import SubmitField, StringField, PasswordField   # 导入自定义表单需要的[字段]
from wtforms.validators import DataRequired, EqualTo    # 导入wtf扩展提供的[表单验证器]

app = Flask(__name__)
app.config['SECRET_KEY']='SECRET_KEY'


class RegisterForm(FlaskForm):    # 自定义[表单类]，文本字段、密码字段、提交按钮
    username = StringField("用户名：", validators=[DataRequired("请输入用户名")], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField("密码：", validators=[DataRequired("请输入密码")])
    password2 = PasswordField("确认密码：", validators=[DataRequired("请输入确认密码"), EqualTo("password", "两次密码不一致")])
    submit = SubmitField("注册")

    
# 定义根路由视图函数，生成--表单对象--，获取表单数据，进行表单数据验证
@app.route('/demo2', methods=["get", "post"])
def demo2():
    register_form = RegisterForm()    # 实例化表单对象
    if request.method == "POST":
        if register_form.validate_on_submit():    # 判断表单所有的数据是否都合法
            # username = request.form.get("username")
            # password = request.form.get("password")
            # password2 = request.form.get("password2")
            username = register_form.username.data
            password = register_form.password.data
            password2 = register_form.password2.data
            
            # 假装做注册操作
            print(username, password, password2)
            return "success"
        else:
            flash('数据有误')
    return render_template('temp_register.html', form=register_form)

if __name__ == '__main__':
    app.run(debug=True)
```

>  WTF表单数据提取 2 种方式:   1. request.form.get('username')       2. register_form.username.data

####    

## 9 CSRF攻击 (跨站请求伪造)

### 9.1 什么是 CSRF 攻击 ?

Cross Site Request Forgery

`CSRF` 指攻击者盗用了你的身份，以你的名义发送恶意请求。包括：以你名义发送邮件，发消息，盗取你的账号，甚至于购买商品，虚拟货币转账......



### 9.2 CSRF 攻击过程

- 客户端访问服务器时没有同服务器做安全验证


![CSRF攻击过程](.\Flask框架__02_images\CSRF攻击过程.png)

### 9.3 如何防止 CSRF 攻击 ?

#### 步骤

1. 在客户端向后端请求界面数据的时候，后端会往响应中的 cookie 中设置  `csrf_token`  的值
2. 在 Form 表单中添加一个隐藏的的字段，值也是  `csrf_token`
3. 在用户点击提交的时候，会带上这两个值向后台发起请求
4. 后端接受到请求，开始以下几件事件：
   - 从 cookie中取出 csrf_token
   - 从 表单数据中取出来隐藏的 csrf_token 的值
   - 进行对比
5. 如果比较之后两值一样，那么代表是正常的请求，如果没取到或者比较不一样，代表不是正常的请求，不执行下一步操作




#### CSRF攻击的代码

**(1) 未进行 csrf 校验的 WebA**

———————————————————WebA后端————————————————

```python
from flask import Flask, render_template, make_response
from flask import redirect
from flask import request
from flask import url_for

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 取到表单中提交上来的参数
        username = request.form.get("username")
        password = request.form.get("password")

        if not all([username, password]):
            print('参数错误')
        else:
            print(username, password)
            if username == 'laowang' and password == '1234':
                # 状态保持，设置用户名到cookie中表示登录成功
                # --------- 注1: 这里的响应对象没有用 make_response 生成, 也能设置cookie ----------
                response = redirect(url_for('transfer'))
                response.set_cookie('username', username)
                return response
            else:
                print('密码错误')

    return render_template('temp_login.html')


@app.route('/transfer', methods=["POST", "GET"])
def transfer():
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for('index'))

    if request.method == "POST":
        to_account = request.form.get("to_account")
        money = request.form.get("money")
        print('假装执行转操作，将当前登录用户的钱转账到指定账户')
        return '转账 %s 元到 %s 成功' % (money, to_account)

    # 渲染转换页面
    # --------- 注2: 这里的响应对象用 make_response 生成, 传入渲染模板函数 ----------
    response = make_response(render_template('temp_transfer.html'))
    return response

if __name__ == '__main__':
    app.run(debug=True, port=9000)
```

​	———————————————————WebA前端登录————————————————

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>

<h1>我是网站A，登录页面</h1>

<form method="post">
    <label>用户名：</label><input type="text" name="username" placeholder="请输入用户名"><br/>
    <label>密码：</label><input type="password" name="password" placeholder="请输入密码"><br/>
    <input type="submit" value="登录">
</form>

</body>
</html>
```

———————————————————WebA前端转账————————————————

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>转账</title>
</head>
<body>
<h1>我是网站A，转账页面</h1>

<form method="post">
    <label>账户：</label><input type="text" name="to_account" placeholder="请输入要转账的账户"><br/>
    <label>金额：</label><input type="number" name="money" placeholder="请输入转账金额"><br/>
    <input type="submit" value="转账">
</form>

</body>
</html>
```

> 运行测试，如果在未登录的情况下，不能直接进入转账页面，测试转账是成功的



**(2) 攻击者网站B的代码**

———————————————————WebB后端————————————————

```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('temp_index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
```



———————————————————WebB前端————————————————

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>我是网站B</h1>

<form method="post" action="http://127.0.0.1:9000/transfer">
    <input type="hidden" name="to_account" value="999999">
    <input type="hidden" name="money" value="190000" hidden>
    <input type="submit" value="点击领取优惠券">
</form>

</body>
</html>
```

> 运行测试，在用户登录网站A的情况下，点击网站B的按钮，可以实现伪造访问



#### 防止CSRF攻击的代码

 在网站A中模拟实现 csrf_token 校验的流程

- 添加生成 csrf_token 的函数

```
# 生成 csrf_token 函数
def generate_csrf():
    return bytes.decode(base64.b64encode(os.urandom(48)))

```

- 在渲染转账页面的，做以下几件事情：
  - 生成 csrf_token 的值
  - 在返回转账页面的响应里面设置 csrf_token 到 cookie 中
  - 将 csrf_token 保存到表单的隐藏字段中

```
@app.route('/transfer', methods=["POST", "GET"])
def transfer():
    ...
    # 生成 csrf_token 的值
    csrf_token = generate_csrf()

    # 渲染转换页面，传入 csrf_token 到模板中
    response = make_response(render_template('temp_transfer.html', csrf_token=csrf_token))
    # 设置csrf_token到cookie中，用于提交校验
    response.set_cookie('csrf_token', csrf_token)
    return response

```

- 在转账模板表单中添加 csrf_token 隐藏字段

```
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <label>账户：</label><input type="text" name="to_account" placeholder="请输入要转账的账户"><br/>
    <label>金额：</label><input type="number" name="money" placeholder="请输入转账金额"><br/>
    <input type="submit" value="转账">
</form>

```

- 运行测试，进入到转账页面之后，查看 cookie 和 html 源代码


- 在执行转账逻辑之前进行 csrf_token 的校验

```python
if request.method == "POST":
    to_account = request.form.get("to_account")
    money = request.form.get("money")
    
    form_csrf_token = request.form.get("csrf_token")    	# 1 取出表单中的 csrf_token
    cookie_csrf_token = request.cookies.get("csrf_token")   # 2 取出 cookie 中的 csrf_token
    if cookie_csrf_token != form_csrf_token:   				# 3 进行对比
        return 'token校验失败，可能是非法操作'
    print('假装执行转操作，将当前登录用户的钱转账到指定账户')
    return '转账 %s 元到 %s 成功' % (money, to_account)
```

运行测试，用户直接在网站 A 操作没有问题，再去网站B进行操作，发现转账不成功，因为网站 B 获取不到表单中的 csrf_token 的隐藏字段，而且浏览器有**同源策略**，网站B是获取不到网站A的 cookie 的，所以就解决了**跨站请求伪造**的问题



#### 在 Flask-wtf扩展中解决 CSRF 攻击

Flask-wtf 扩展有一套完善的 csrf 防护体系，对于我们开发者来说，使用起来非常简单

###### 在 FlaskForm 中实现校验

- 设置应用程序的 secret_key
  - 用于加密生成的 csrf_token 的值

```
app.secret_key = "#此处可以写随机字符串#"
```

- 在模板的表单中添加以下代码

```
<form method="post">
    {{ form.csrf_token() }}
    {{ form.username.label }} {{ form.username }}<br/>
    {{ form.password.label }} {{ form.password }}<br/>
    {{ form.password2.label }} {{ form.password2 }}<br/>
    {{ form.submit }}
</form>

```

- 渲染出来的前端页面中：
  - input隐藏标签的name="scrf_token",  type="scrf_token",  value="设置的secret_key"

> 设置完毕，cookie 中的 csrf_token 不需要我们关心，会自动帮我们设置



###### 单独使用

- 设置应用程序的 secret_key,   用于加密生成的 csrf_token 的值

```
app.secret_key = "#此处可以写随机字符串#"

```

- 导入 flask_wtf.csrf 中的 CSRFProtect 类，进行初始化，并在初始化的时候关联 app

```
from flask.ext.wtf import CSRFProtect
CSRFProtect(app)
```



- 如果模板中用**WTF表单**，需要在模板中表单一栏加入:

```
<form method="post">
	...
    {{ form.csrf_token }}	或	{{ form.hidden_tag() }}
    ...
</form>
```



- 但如果模板中用**普通表单**，仍需要 CSRF 令牌:

```html
添加input隐藏标签, name="csrf_token"   value="{{ csrf_token() }}"

<form method="post" action="/">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
</form>
```



###### 关闭不需要的CSRF保护

自然，我们很可能有的表单不需要保护，那么，以下三种：

1. 全局禁用：app.config中设置  `WTF_CSRF_ENABLED = False`
2. 单个表单禁用：生成表单时加入参数   `form = Form(csrf_enabled=False)`
3. 不使用Flask-WTF





### flask 内置的保护机制

有些时候，我们根本就用不到Flask-WTF,   那么我可以使用flask自身提供的保护机制。

###### 开启保护

要开启csrf攻击保护，需要一下几个步骤:

导入方法，设置密钥，进行保护

```python
from flask_wtf.csrf import CSRFProtect

app.config['SECRET_KEY'] = 'you never guess'
CSRFProtect(app)
```


这时候对于一个普通的form，如果你没有

```
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
```

flask会抛出http错误。



###### 临时关闭保护

那么，如何临时关闭csrf保护呢。 
上面的代码做修改：

```python
# 1
#去掉 CSRFProtect(app), 改为:
csrf = CSRFProtect()

# 2
if __name__ == '__main__':
	csrf.init_app(app)
    ...

# 3
# 在不需要保护的路由上方加上装饰器:
@csrf.exempt
```



