# django3.0 Admin 登录问题

django3.0，创建超级管理员后，登录admin页面，python提示已经停止:   https://www.zhihu.com/question/363575690/answer/990182539 

# 资源

- Django2.0入门教程:定制Admin管理后台:   https://www.django.cn/course/show-16.html 

# 使用Admin站点

假设我们要设计一个新闻网站，我们需要编写展示给用户的页面，网页上展示的新闻信息是从哪里来的呢？**是从数据库中查找到新闻的信息，然后把它展示在页面上**。但是我们的网站上的新闻每天都要更新，这就意味着对数据库的增、删、改、查操作，那么我们需要每天写sql语句操作数据库吗? 如果这样的话，是不是非常繁琐，所以我们可以设计一个页面，通过对这个页面的操作来实现对新闻数据库的增删改查操作。那么问题来了，老板说我们需要在建立一个新网站，是不是还要设计一个页面来实现对新网站数据库的增删改查操作，但是这样的页面具有一个很大的重复性，那有没有一种方法能够让我们很快的生成管理数据库表的页面呢？**有，那就是我们接下来要给大家讲的Django的后台管理**。Django能够根据定义的模型类自动地生成管理页面。

使用Django的管理模块，需要按照如下步骤操作：

1. 管理界面本地化
2. 创建管理员
3. 注册模型类
4. 自定义管理页面

## 1 管理界面本地化

在settings.py中设置语言和时区

```python
LANGUAGE_CODE = 'zh-hans' # 使用中国语言
TIME_ZONE = 'Asia/Shanghai' # 使用中国上海时间
```

## 2 创建超级管理员

创建管理员的命令如下，按提示输入用户名、邮箱、密码。

```shell
python manage.py createsuperuser
```

打开浏览器，在地址栏中输入如下地址后回车。

```html
http://127.0.0.1:8000/admin/
```

输入前面创建的用户名、密码完成登录。

登录成功后的界面并没有我们自己应用模型的入口，接下来进行第三步操作。



## 3 注册模型类

登录后台管理后，默认没有我们创建的应用中定义的模型类，需要在自己应用中的 admin.py 文件中注册，才可以在后台管理中看到，并进行增删改查操作。

打开 booktest/admin.py 文件，编写如下代码：

```python
from django.contrib import admin
from booktest.models import BookInfo,HeroInfo

admin.site.register(BookInfo)
admin.site.register(HeroInfo)
```

到浏览器中刷新页面，可以看到模型类 BookInfo 和 HeroInfo 的管理了。



## 4 定义与使用 Admin 管理类

Django 提供的 Admin 站点的展示效果可以通过自定义 **ModelAdmin** 类来进行控制。

定义管理类需要继承自 **admin.ModelAdmin** 类，如下

```python
from django.contrib import admin

class BookInfoAdmin(admin.ModelAdmin):
    pass
```

使用管理类有两种方式：

- 注册参数

  ```python
  admin.site.register(BookInfo, BookInfoAdmin)
  ```

- 装饰器

  ```python
  @admin.register(BookInfo)
  class BookInfoAdmin(admin.ModelAdmin):
      pass
  ```





# 调整列表页展示

## 1 页大小

每页中显示多少条数据，默认为每页显示100条数据，属性如下：

```python
list_per_page = 100
```

1）打开 booktest/admin.py 文件，修改 AreaAdmin 类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    list_per_page = 2
```

2）在浏览器中查看区域信息的列表页面



## 2 "操作选项"的位置

顶部显示的属性，设置为True在顶部显示，设置为False不在顶部显示，默认为True。

```python
actions_on_top=True
```

底部显示的属性，设置为True在底部显示，设置为False不在底部显示，默认为False。

```python
actions_on_bottom=False
```

1）打开 booktest/admin.py 文件，修改 BookInfoAdmin 类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    actions_on_top = True
    actions_on_bottom = True
```

2）在浏览器中刷新



## 3 列表中的列

属性如下：

```
list_display = [模型字段1,模型字段2,...]
```

1）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    list_display = ['id','btitle']
```

2）在浏览器中刷新

**点击列头可以进行升序或降序排列。**



## 4 将方法作为列

列可以是模型字段，还可以是模型方法，要求方法有返回值。

**通过设置short_description属性，可以设置在admin站点中显示的列名。**

1）打开 booktest/models.py 文件，修改BookInfo类如下：

```python
class BookInfo(models.Model):
    ...
    def pub_date(self):
        return self.bpub_date.strftime('%Y年%m月%d日')

    pub_date.short_description = '发布日期'  # 设置方法字段在admin中显示的标题
```

2）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    list_display = ['id','atitle','pub_date']
```

3）在浏览器中刷新



方法列是不能排序的，如果需要排序需要为方法指定排序依据。

```
admin_order_field = 模型类字段
```

1）打开booktest/models.py文件，修改BookInfo类如下：

```python
class BookInfo(models.Model):
    ...
    def pub_date(self):
        return self.bpub_date.strftime('%Y年%m月%d日')

    pub_date.short_description = '发布日期'
    pub_date.admin_order_field = 'bpub_date'
```

2）在浏览器中刷新



## 5 关联对象

无法直接访问关联对象的属性或方法，可以在模型类中封装方法，访问关联对象的成员。

1）打开booktest/models.py文件，修改HeroInfo类如下：

```python
class HeroInfo(models.Model):
    ...
    def read(self):
        return self.hbook.bread

    read.short_description = '图书阅读量'
```

2）打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

```python
class HeroInfoAdmin(admin.ModelAdmin):
    ...
    list_display = ['id', 'hname', 'hbook', 'read']
```

3）在浏览器中刷新



## 6 右侧栏过滤器

属性如下，只能接收字段，会将对应字段的值列出来，用于快速过滤。一般用于有重复值的字段。

```
list_filter=[]
```

1）打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

```python
class HeroInfoAdmin(admin.ModelAdmin):
    ...
    list_filter = ['hbook', 'hgender']
```

2）在浏览器中刷新



## 7 搜索框

属性如下，用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。

```
search_fields = []
```

1）打开booktest/admin.py文件，修改HeroInfoAdmin类如下：

```python
class HeroInfoAdmin(admin.ModelAdmin):
    ...
    search_fields = ['hname']
```





# 调整编辑页展示

## 1. 显示字段

属性如下：

```
fields = []
```

1）点击某行ID的链接，可以转到修改页面



2）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    fields = ['btitle', 'bpub_date']
```

3）刷新浏览器



## 2. 分组显示

属性如下：

```
fieldset = (
    ('组1标题',{'fields':('字段1','字段2')}),
    ('组2标题',{'fields':('字段3','字段4')}),
)
```

1）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    # fields = ['btitle', 'bpub_date']
    fieldsets = (
        ('基本', {'fields': ['btitle', 'bpub_date']}),
        ('高级', {
            'fields': ['bread', 'bcomment'],
            'classes': ('collapse',)  # 是否折叠显示
        })
    )
```

2）刷新浏览器

> 说明：fields与fieldsets两者选一使用。

## 3. 关联对象

在一对多的关系中，可以在一端的编辑页面中编辑多端的对象，嵌入多端对象的方式包括表格、块两种。

- 类型 InlineModelAdmin：表示在模型的编辑页面嵌入关联模型的编辑。
- 子类 TabularInline：以表格的形式嵌入。
- 子类 StackedInline：以块的形式嵌入。

1）打开booktest/admin.py文件，创建HeroInfoStackInline类。

```python
class HeroInfoStackInline(admin.StackedInline):
    model = HeroInfo  # 要编辑的对象
    extra = 1  # 附加编辑的数量
```

2）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    inlines = [HeroInfoStackInline]
```

3）刷新浏览器



可以用表格的形式嵌入。

1）打开booktest/admin.py文件，创建HeroInfoTabularInline类。

```python
class HeroInfoTabularInline(admin.TabularInline):
    model = HeroInfo
    extra = 1
```

2）打开booktest/admin.py文件，修改BookInfoAdmin类如下：

```python
class BookInfoAdmin(admin.ModelAdmin):
    ...
    inlines = [HeroInfoTabularInline]
```

3）刷新浏览器



# 调整站点信息

Admin 站点的名称信息也是可以自定义的。

- **admin.site.site_header** 设置网站页头
- **admin.site.site_title** 设置页面标题
- **admin.site.index_title** 设置首页标语

在booktest/admin.py文件中添加一下信息

```python
from django.contrib import admin

admin.site.site_header = 'My后台管理'
admin.site.site_title = 'My后台管理'
admin.site.index_title = '欢迎使用My后台管理'
```

刷新网站







# 上传图片

Django有提供文件系统支持，在Admin站点中可以轻松上传图片。

使用Admin站点保存图片，需要安装Python的图片操作包

```python
pip install Pillow
```

## 1 配置

默认情况下，Django会将上传的图片保存在本地服务器上，需要配置保存的路径。

我们可以将上传的文件保存在静态文件目录中，如我们之前设置的static_files目录中在settings.py 文件中添加如下上传保存目录信息

```python
MEDIA_ROOT=os.path.join(BASE_DIR,"static_files/media")
```

## 2 为模型类添加 ImageField 字段

我们为之前的BookInfo模型类添加一个ImageFiled

```python
class BookInfo(models.Model):
    # ...
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
```

- upload_to 选项指明该字段的图片保存在 MEDIA_ROOT 目录中的哪个子目录

进行数据库迁移操作

```python
python manage.py makemigrations
python manage.py migrate
```

## 3 使用 Admin 站点上传图片

进入 Admin 站点的图书管理页面，选择一个图书，能发现多出来一个上传图片的字段

选择一张图片并保存后，图片会被保存在 **static_files/media/booktest/** 目录下。

在数据库中，我们能看到 image 字段被设置为图片的路径.