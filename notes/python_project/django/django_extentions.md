# django-celery

- Github:   https://github.com/celery/django-celery 
- DOC:   http://celery.github.io/django-celery/ 
- Celery:   https://docs.celeryproject.org/en/stable/ 







# django 对接 搜索引擎 

### django-haystack

- Django:  django-haystack 插件
- [文档](https://django-haystack.readthedocs.io/en/master/toc.html)

django-haystack 提供了一个搜索的接口，底层可以根据自己需求更换搜索引擎.    它其实有点类似于 django 中的 ORM 插件，提供l了一个操作数据库接口，但是底层具体使用哪个数据库是可以自己设置的。

django-haystack 支持的搜索引擎有  [Solr](http://lucene.apache.org/solr/), [Elasticsearch](https://www.elastic.co/products/elasticsearch), [Whoosh](https://bitbucket.org/mchaput/whoosh/), [Xapian](http://xapian.org/),  等。 Whoosh 是基于纯 Python 的搜索引擎，检索速度快，集成方便。 



##### django-haystack 集成 Whoosh

资源:

-  https://blog.csdn.net/ac_hell/article/details/52875927 

工具:

- 搜索框架使用 django-haystack 开源搜索框架
- 搜索引擎使用 Whoosh，这是一个由纯 Python 实现的全文搜索引擎，没有二进制文件等，比较小巧，配置比较简单，当然性能略低。
- 中文分词使用 Jieba，由于 Whoosh 自带的是英文分词，不支持中文分词，故用 jieba 替换 whoosh 的分词组件。

步骤:

1. 安装第三方库

```bash
$ pip install  django-haystack  whoosh  jieba
```

2. 在项目 `INSTALLED_APPS` 中安装 django-haystack

   ```python
   INSTALLED_APPS = [
       # ...
       'haystack',  # 先注册 haystack
       'app1',      # 后注册自己的app
   
   ]
   ```

3. 配置搜索引擎后端

```python
# settings.py
# 配置搜索引擎后端
HAYSTACK_CONNECTIONS = {
    'default': {
        # 设置haystack的搜索对象
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 设置索引文件的位置, 存在本地项目下的 whoosh_index 下
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE  =  8

# 模型数据修改时自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 更多配置项见: https://django-haystack.readthedocs.io/en/master/settings.html
```

4. 创建索引类

如果想针对某个 app 例如`app1`做全文检索，则必须在`app1`的目录下面建立`search_indexes.py`文件，文件名不能修改 

```python
import datetime
from haystack import indexes
from .models import Note


# 类名为需要检索的 模型类名 + Index，这里需要检索Note，所以创建 NoteIndex
class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    """

    说明:

    1. 每个索引里面必须有且只能有一个字段为 document=True，
    这代表 haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。
    其他的字段只是附属的属性，方便调用，并不作为检索数据。

    2. 如果使用一个字段设置了document=True，则一般约定此字段名为text，
    这是在SearchIndex类里面一贯的命名，以防止后台混乱.

    3. text 字段指定 use_template=True 时，允许使用数据模板去建立搜索引擎索引的文件，
    数据模板路径为 templates/search/indexes/应用名/被索引模型类名的小写_text.txt
    """
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')

    def get_model(self):  # 必须重载 get_model 方法
        return Note

    def index_queryset(self, using=None):  # 重载index_..函数
        """Used when the entire index for model is updated."""

        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

```

对应的模型类是 app1/models.py::Note

```python
from django.db import models


class Note(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

    # 创建好模型后不要忘了迁移
    # python manage.py makemigrations
    # python manage.py migrate
```



5. 添加 url 映射

```python
urlpatterns = [
    # ...
    path('search/', include('haystack.urls'))
]
```

6. 添加模板

```
在 templates 文件夹下创建以下结构的目录：
templates -- search -- indexes -- news(app的名字) -- news(app的名字)_text.txt

即:
django_demo\app1\templates\search\indexes\app1\note_text.txt

note_text.txt 文件中添加需要被索引的字段，示例代码如下：
    {{ object.pub_date }}
    {{ object.title }}
    {{ object.body }}
```

这个数据模板的作用是对`Note.pub_date`, `Note.title`,`Note.body`这三个字段建立索引，当检索的时候会对这三个字段做全文检索匹配 

7. (可选)  自定义搜索视图  (针对特定需求)

```python
# demo/app1/views.py

from haystack.views import SearchView
# from .models import Topic   # 还没有定义这个类, 假设存在

class MySeachView(SearchView):
    def extra_context(self):  # 重载 extra_context 可以添加额外的context内容
        context = super().extra_context()
        # 假设另外有一个 Topic 模型类, 需要把它通过 context 传给模板
        # side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
        # context['side_list'] = side_list
        return context
```

更新 url 映射

```python
    # path('search/', include('haystack.urls')),
    url(r'^search/', views.MySeachView(), name='haystack_search'),
```



8. 添加搜索页面 HTML

> 注:  此时先测试一下 haystack 在 HTML 模板中的使用,  后面会直接返回 JSON 响应

`SearchView()`视图函数默认使用的 html 模板路径为`templates/search/search.html（推荐在根目录创建templates，并在settings.py里设置好）`
所以创建`templates/search/search.html`文件

> 注:  下面的 `page.object_list` 是一个列表,  由 `SearchResult` 对象组成,  而不是自定义模型的对象

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h2>Search</h2>
<form method="get" action=".">
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Search">
            </td>
        </tr>
    </table>

    {% if query %}
        <h3>Results</h3>

        {% for result in page.object_list %}
            <p>
                <a href="{{ result.object.get_absolute_url }}">{{ result.object.title }}</a>
            </p>
        {% empty %}
            <p>No results found.</p>
        {% endfor %}

        {% if page.has_previous or page.has_next %}
            <div>
                {% if page.has_previous %}<a href="?q={{ query }}&page={{ page.previous_page_number }}">{% endif %}«
                Previous{% if page.has_previous %}</a>{% endif %}
                |
                {% if page.has_next %}<a href="?q={{ query }}&page={{ page.next_page_number }}">{% endif %}Next »
                {% if page.has_next %}</a>{% endif %}
            </div>
        {% endif %}
    {% else %}
        {# Show some example queries to run, maybe query syntax, something else? #}
    {% endif %}
</form>
</body>
</html>
```



9. 构建索引

```bash
python manage.py rebuild_index
# 或者使用 update_index 命令
```

10. 向数据库添加几个测试数据

由于目前没有集成 jieba 分词,  故应该创建全英文数据  (可以试试带中文,  试过好像搜索不到对应内容)

```python
# 在终端输入 python manage.py shell 进入交互式终端, 操作数据库
from datetime import datetime
from app1.models import Note    # Note 是当前建立了索引的模型类

Note(1, datetime.now(), '池田大作', '不要回避苦恼和困难，挺起身来向它挑战，进而克服它。').save()
Note(2, datetime.now(), '别林斯基', '好的书籍是最贵重的珍宝。').save()
Note(3, datetime.now(), '朱熹', '读书之法，在循序而渐进，熟读而精思。').save()
Note(4, datetime.now(), '达尔文', '敢于浪费哪怕一个钟头时间的人，说明他还不懂得珍惜生命的全部价值。').save()
Note(5, datetime.now(), '朱熹', '读书之法，在循序而渐进，熟读而精思。').save()
Note(6, datetime.now(), '朱熹', '读书有三到，谓心到，眼到，口到。').save()
Note(7, datetime.now(), '屈原', '路漫漫其修道远，吾将上下而求索。').save()
Note(8, datetime.now(), '莎士比亚', '人的一生是短的，但如果卑劣地过这一生，就太长了。').save()
Note(9, datetime.now(), '拉罗什夫科', '取得成就时坚持不懈，要比遭到失败时顽强不屈更重要。').save()
```



11. 测试搜索功能.   页面访问  http://127.0.0.1:8000/app1/search 

12. 集成 jieba 分词

将文件 whoosh_backend.py（该文件路径为 site-packages/haystack/backends/whoosh_backend.py）拷贝到 app 下面，并重命名为 whoosh_cn_backend.py，例如 app1/whoosh_cn_backend.py

修改为如下

```python
from jieba.analyse import ChineseAnalyzer   #在顶部添加
 
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(),field_boost=field_class.boost, sortable=True)   #注意先找到这个再修改，而不是直接添加
```

也可以用继承的方式,  只修改 `WhooshSearchBackend` 类的 `build_schema` 方法,  但还是有些代码要复制过来

```python
# 导入 jieba 分词的中文分析器
from jieba.analyse import ChineseAnalyzer

# ... 复制一些 import


class WhooshCNBackend(WhooshSearchBackend):
    def build_schema(self, fields):
        # ... 复制一些代码
        
        schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(),field_boost=field_class.boost, sortable=True)
        
        # ... 复制一些代码


# 定义一个 whoosh 引擎类, 继承自 WhooshEngine, 
# 重载 backend 类属性, 指向上面定义好的 WhooshCNBackend
class MyWhooshCNEngine(WhooshEngine):
    backend = WhooshCNBackend

```

修改 settings.py

```python
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'app1.whoosh_cn_backend.MyWhooshCNEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
```



13. 测试 jieba 分词,  不出意外的话,  现在可以搜索中文 (同样可以搜索英文)

14. 高亮显示匹配文本

在 search.html 中先 load 一下 `highlight`,  然后就可以用 `{% highlight ... %}` 语法,  对于匹配的子字符串会用一个标签包裹 (默认 span 标签),  并添加了` class="highlighted" `.   最后只需要手动给 ` class="highlighted" ` 加一个样式即可.

```jinja2
{# 在开头 load 一下 highlight #}
{% load highlight %}

{# ... #}

    {% if query %}
        <h3>Results</h3>
        {% for result in page.object_list %}
            <div>标题: {% highlight result.object.title with query %}</div>
            <div>内容: {% highlight result.object.body with query %}</div>
            <hr>
        {% empty %}
            <p>No results found.</p>
        {% endfor %}

        {# ... #}
    {% endif %}
```

查看 django-haystack 文档看如何高亮显示匹配内容:  [文档](https://django-haystack.readthedocs.io/en/master/toc.html)

问题:  django-haystack 默认只显示高亮的部分,  把其他很多文本都用 `...` 省略了,  如果想展示,  应该怎么做 ?

> 仔细考虑一下这个问题,  其实不是问题,  因为大部分情况下搜索结果的文本是很长的



前后端分离模式下怎么返回搜索内容的 JSON 数据?

1. 不需要 search.html 模板了,  可以直接删除
2. 视图类仍然继承自 haystack 的 SearchView,  重写 create_response 方法,  如果有特殊需求,  也重写 extra_context 方法
3. postman 访问测试:    http://127.0.0.1:8000/app1/search/?q=朱熹&models=app1.note&page=1

> 当前只有一个模型: Note,  所以先不测试不同模型返回不同结果了
>
> q 为空时返回空,  page 默认为 1,  models 默认为空 (会从所有建立了索引的模型中搜索数据)

```python
from haystack.views import SearchView

class MySeachView(SearchView):
    def extra_context(self):
        context = super().extra_context()
        return context

    def create_response(self):
        """
        重写 create_response, 返回 JSON 响应
        遗留问题: 怎么拿到高亮处理后的 html 字符串, 然后通过 json 返回给前端?
        2020-5-19 解决遗留问题: 使用 haystack 的 Highlighter 类, 详见官方文档.
        """
        context = self.get_context()
        objs = context['page'].object_list
        paginator = context['paginator']
        results = []
        for search_ret in objs:
            results.append({
                'title': search_ret.title,
                'pub_date': str(search_ret.pub_date),
                'body': search_ret.body,
            })
        data = {
            'count': paginator.count,
            'per_page': paginator.per_page,
            'page': context['page'].number,
            'results': results
        }
        return JsonResponse({'data': data})

```





### drf-haystack  -------  待续

- DRF:  drf-haystack 插件

##### drf-haystack 集成 elasticsearch





```bash
pip install drf-haystack
pip install elasticsearch==2.4.1
```







# drf-extensions 扩展集

包含 DRF 框架的许多扩展

- Viewsets
  - [DetailSerializerMixin](http://chibisov.github.io/drf-extensions/docs/#detailserializermixin)
  - [PaginateByMaxMixin](http://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin)
  - [Cache/ETAG mixins](http://chibisov.github.io/drf-extensions/docs/#cache-etag-mixins)
- Routers
  - [Pluggable router mixins](http://chibisov.github.io/drf-extensions/docs/#pluggable-router-mixins)
- Nested routes
  - [Nested router mixin](http://chibisov.github.io/drf-extensions/docs/#nested-router-mixin)
  - [Usage with generic relations](http://chibisov.github.io/drf-extensions/docs/#usage-with-generic-relations)
- Serializers
  - [PartialUpdateSerializerMixin](http://chibisov.github.io/drf-extensions/docs/#partialupdateserializermixin)
- Fields
  - [ResourceUriField](http://chibisov.github.io/drf-extensions/docs/#resourceurifield)
- Permissions
  - [Object permissions](http://chibisov.github.io/drf-extensions/docs/#object-permissions)
- [Caching](http://chibisov.github.io/drf-extensions/docs/#caching)
  - [Cache response](http://chibisov.github.io/drf-extensions/docs/#cache-response)
  - [Timeout](http://chibisov.github.io/drf-extensions/docs/#timeout)
  - [Usage of the specific cache](http://chibisov.github.io/drf-extensions/docs/#usage-of-the-specific-cache)
  - [Cache key](http://chibisov.github.io/drf-extensions/docs/#cache-key)
  - [Default key function](http://chibisov.github.io/drf-extensions/docs/#default-key-function)
  - [Caching errors](http://chibisov.github.io/drf-extensions/docs/#caching-errors)
  - [CacheResponseMixin](http://chibisov.github.io/drf-extensions/docs/#cacheresponsemixin)



# coreapi 生成 DRF 接口文档

- REST framewrok生成接口文档需要`coreapi`库的支持。 
- 接口文档以网页的方式呈现。
- 自动接口文档能生成的是继承自`APIView`及其子类的视图。

# djangorestframework-jwt

 JSON Web Token Authentication support for Django REST Framework  

- [Github](https://github.com/jpadilla/django-rest-framework-jwt)

我们在验证完用户的身份后（检验用户名和密码），需要向用户签发JWT，在需要用到用户身份信息的时候，还需核验用户的JWT。

关于签发和核验JWT，我们可以使用 Django REST framework JWT 扩展来完成。

# django-cors-headers

- [Github](https://github.com/adamchainz/django-cors-headers)

解决后端对跨域访问的支持 



#  CKEditor

富文本编辑器 



# django-crontab

 在 Django 中执行定时任务 



# xadmin

 Django 的第三方扩展，可是使 Django 的 admin 站点使用更方便 

