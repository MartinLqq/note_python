# ==== django 3.0 ====

# 数据库

## ORM 框架

```
ORM  对象-关系映射
    O - object
    R - relation
    M - Mapping
```

ORM 框架帮我们把类和数据表进行了一个映射，可以让我们**通过类和类对象就能操作它所对应的表格中的数据**。ORM 框架还有一个功能，它可以**根据我们设计的类自动帮我们生成数据库中的表格**，省去了我们自己建表的过程。

django 内嵌了 ORM 框架，不需要直接面向数据库编程，而是定义模型类，通过模型类和对象完成数据表的增删改查操作。

使用 django 进行数据库开发的步骤：

1. 配置数据库连接信息
2. 在 models.py 中定义模型类
3. 迁移
4. 通过类和对象完成数据增删改查操作



## 配置使用 mysql

Django 默认初始配置使用 sqlite 数据库。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

使用 mysql

```python
# 1.安装 mysqlclient 驱动
# pip install mysqlclient

# 2.修改DATABASES配置信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',   # 数据库主机
        'PORT': 3306,          # 数据库端口
        'USER': 'root',        # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'django_blog'  # 数据库名字
    }
}
```

django 2.0 之前有一种使用 mysql 的方法,  但会出现兼容性问题.  **建议用上面的 `mysqlclient`**

> 异常提示:  `django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.`

```python
# 1.安装 pymysql 驱动
# pip install pymysql

# 2.在Django的工程同名子目录的__init__.py文件中添加如下语句, 让Django的ORM能以mysqldb的方式来调用PyMySQL
import pymysql
# ======= 兼容性问题解决前 ========
# pymysql.install_as_MySQLdb()
# ======= 兼容性问题解决后 ========
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

# 3.修改DATABASES配置信息
DATABASES = " ... 同上 ... "
```



## 定义模型类

- 模型类被定义在 `项目/应用/models.py` 文件中。
- 模型类必须继承自 `Model` 类，位于包 `django.db.models` 中。

创建应用 booktest，在 models.py 文件中定义模型类。

```python
from django.utils import timezone

from django.db import models


#定义图书模型类BookInfo
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateTimeField(verbose_name='发布时间', default=timezone.now)
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return self.btitle


#定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    hname = models.CharField(max_length=20, verbose_name='名称')
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    hcomment = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    hbook = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname
```



**1） 数据库表名**

- 模型类如果未指明表名，Django默认以 **小写app应用名_小写模型类名** 为数据库表名。

- 可通过**db_table** 指明数据库表名。

**2） 关于主键**

- django 会为表创建自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置某属性为主键列后django不会再创建自动增长的主键列。

- 默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。

**3） 属性命名限制**

- 不能是 python 的保留关键字。

- 不允许使用连续的下划线，这是由 django 的查询方式决定的。

- 定义属性时需要指定字段类型，通过字段类型的参数指定选项，语法如下：

  ```python
  属性 = models.字段类型(选项)
  ```



### 字段类型

| 类型             | 说明                                                         |
| :--------------- | :----------------------------------------------------------- |
| AutoField        | 自动增长的 IntegerField，通常不用指定，不指定时 Django 会自动创建属性名为 id 的自动增长属性 |
| BooleanField     | 布尔字段，值为 True 或 False                                 |
| NullBooleanField | 支持 Null、True、False 三种值                                |
| CharField        | 字符串，参数 max_length 表示最大字符个数                     |
| TextField        | 大文本字段，一般超过 4000 个字符时使用                       |
| IntegerField     | 整数                                                         |
| DecimalField     | 十进制浮点数， 参数 max_digits 表示总位数， 参数 decimal_places 表示小数位数 |
| FloatField       | 浮点数                                                       |
| DateField        | 日期， <br />auto_now 表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为False； <br />auto_now_add 表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False; <br />*auto_now_add 和 auto_now是相互排斥的，组合将会发生错误* |
| TimeField        | 时间，参数同 DateField                                       |
| DateTimeField    | 日期时间，参数同 DateField                                   |
| FileField        | 上传文件字段                                                 |
| ImageField       | 继承于 FileField，对上传的内容进行校验，确保是有效的图片     |



### 一些选项

| 选项        | 说明                                                         |
| :---------- | ------------------------------------------------------------ |
| null        | 如果为 True，表示允许为空，默认值是 False.  null 是数据库范畴的概念 |
| blank       | 如果为 True，则该字段允许为空白，默认值是 False,  blank是表单验证范畴的 |
| db_column   | 字段的名称，如果未指定，则使用属性的名称                     |
| db_index    | 若值为 True, 则在表中会为此字段创建索引，默认值是 False      |
| default     | 默认                                                         |
| primary_key | 若为 True，则该字段会成为模型的主键字段，默认值是False，一般作为 AutoField 的选项使用 |
| unique      | 如果为 True, 这个字段在表中必须有唯一值，默认值是 False      |



### 外键

在设置外键时，需要通过 **on_delete** 选项指明主表删除数据时，对于外键引用表数据如何处理，在 django.db.models 中包含了可选常量：

- **CASCADE** 级联，删除主表数据时连通一起删除外键表中数据

- **PROTECT** 保护，通过抛出 **ProtectedError** 异常，来阻止删除主表中被外键应用的数据

- **SET_NULL** 设置为 NULL，仅在该字段 null=True 允许为 null 时可用

- **SET_DEFAULT** 设置为默认值，仅在该字段设置了默认值时可用

- **SET()** 设置为特定值或者调用特定方法，如

  ```python
  from django.conf import settings
  from django.contrib.auth import get_user_model
  from django.db import models
  
  def get_sentinel_user():
      return get_user_model().objects.get_or_create(username='deleted')[0]
  
  class MyModel(models.Model):
      user = models.ForeignKey(
          settings.AUTH_USER_MODEL,
          on_delete=models.SET(get_sentinel_user),
      )
  ```

- **DO_NOTHING** 不做任何操作，如果数据库前置指明级联性，此选项会抛出 **IntegrityError** 异常



## 定义抽象模型类

```python
class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
```



## 迁移

将模型类同步到数据库中。

```python
# 1. 生成迁移文件
python manage.py makemigrations

# 2. 同步到数据库中
python manage.py migrate
```



添加测试数据

```mysql
insert into tb_books(btitle,bread,bcomment,is_delete) values
('射雕英雄传','1980-5-1',12,34,0),
('天龙八部','1986-7-24',36,40,0),
('笑傲江湖','1995-12-24',20,80,0),
('雪山飞狐','1987-11-11',58,24,0);
insert into tb_heros(hname,hgender,hbook_id,hcomment,is_delete) values
('郭靖',1,1,'降龙十八掌',0),
('黄蓉',0,1,'打狗棍法',0),
('黄药师',1,1,'弹指神通',0),
('欧阳锋',1,1,'蛤蟆功',0),
('梅超风',0,1,'九阴白骨爪',0),
('乔峰',1,2,'降龙十八掌',0),
('段誉',1,2,'六脉神剑',0),
('虚竹',1,2,'天山六阳掌',0),
('王语嫣',0,2,'神仙姐姐',0),
('令狐冲',1,3,'独孤九剑',0),
('任盈盈',0,3,'弹琴',0),
('岳不群',1,3,'华山剑法',0),
('东方不败',0,3,'葵花宝典',0),
('胡斐',1,4,'胡家刀法',0),
('苗若兰',0,4,'黄衣',0),
('程灵素',0,4,'医术',0),
('袁紫衣',0,4,'六合拳',0);
```



## shell工具

Django 的 manage 工具提供了 **shell** 命令，帮助我们配置好当前工程的运行环境（如连接好数据库等），以便可以直接在终端中执行测试python语句。

```python
# 进入shell
python manage.py shell

# 导入两个模型类，以便后续使用
from booktest.models import BookInfo, HeroInfo
```



## 查看 MySQL 日志

查看 mysq l数据库日志可以查看对数据库的操作记录。 mysql 日志文件默认没有产生，需要做如下配置：

```shell
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

把 68，69 行前面的#去除，然后保存并使用如下命令重启 mysql 服务。

> 68 行:  general_log_file
>
> 69 行:  genreal_log

```shell
sudo service mysql restart

# 实时查看数据库的日志内容
tail -f /var/log/mysql/mysql.log
```





## 数据库操作

### 增加

增加数据有两种方法。

**1）`模型类对象.save()`**

```python
>>> from datetime import date
>>> book = BookInfo(
    btitle='西游记',
    bput_date=date(1988,1,1),
    bread=10,
    bcomment=10
)
>>> book.save()
>>> hero = HeroInfo(
    hname='孙悟空',
    hgender=0,
    hbook=book
)
>>> hero.save()
>>> hero2 = HeroInfo(
    hname='猪八戒',
    hgender=0,
    hbook_id=book.id
)
>>> hero2.save()
```

**2）`模型类.objects.create()`**

```python
>>> HeroInfo.objects.create(
    hname='沙悟净',
    hgender=0,
    hbook=book
)
<HeroInfo: 沙悟净>
```



### 查询

#### > 基本查询

```python
BookInfo.objects.get(id=3)   # 如果不存在会抛出 BookInfo.DoesNotExist 异常
BookInfo.objects.all()
BookInfo.objects.count()
```

#### > 过滤查询

```python
# filter
BookInfo.objects.filter(id__exact=1)
BookInfo.objects.get(id=1)
BookInfo.objects.filter(id__in=[1, 3, 5])
BookInfo.objects.filter(btitle__contains='传')
BookInfo.objects.filter(btitle__endswith='部')
BookInfo.objects.filter(btitle__isnull=False)
BookInfo.objects.filter(id__gt=3)  # gt, gte, lt, lte
# 不区分大小写的写法:
# iexact、icontains、istartswith、iendswith

# exclude
BookInfo.objects.exclude(id=3)  # 不等于

# year、month、day、week_day、hour、minute、second
# 对日期时间类型的属性进行运算
BookInfo.objects.filter(bpub_date__year=1980)
BookInfo.objects.filter(bpub_date__gt=date(1990, 1, 1))

# F 对象, 跨字段比较
# from django.db.models import F
BookInfo.objects.filter(bread__gte=F('bcomment'))
BookInfo.objects.filter(bread__gt=F('bcomment') * 2)  # 在F对象上使用算数运算

# Q 对象, 逻辑查询:  Q(属性名__运算符=值)
# Q 对象可以使用 &, |, ~
"""
例：查询阅读量大于20，并且编号小于3的图书
BookInfo.objects.filter(bread__gt=20,id__lt=3)
或
BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)
或
BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))

例：查询编号不等于3的图书
BookInfo.objects.filter(~Q(pk=3))  # 非, not
或
BookInfo.objects.exclude(pk=3)
"""

# aggregate() 过滤器, 调用聚合函数 Avg, Count, Max, Min, Sum
BookInfo.objects.aggregate(Sum('bread'))  # aggregate的返回值是一个字典类型, {'bread__sum': 3}
```



#### > 排序

```python
# 使用order_by对结果进行排序
BookInfo.objects.all().order_by('bread')  # 升序
BookInfo.objects.all().order_by('-bread')  # 降序
```

#### > 关联查询

```python
# 一 到 多
# `一对应的模型类对象.多对应的模型类名小写_set`
b = BookInfo.objects.get(id=1)
b.heroinfo_set.all()
# 通过一的一方, 创建多的一方:
# 获取一个BookInfo --> 获取其对应的 HeroInfo --> 调用 create 方法
HeroInfo.objects.get(id=1).heroinfo_set.create()


# 多 到 一
# `多对应的模型类对象.多对应的模型类中的关系类属性名`
h = HeroInfo.objects.get(id=1)
h.hbook
# 访问一对应的模型类关联对象的id语法:  `多对应的模型类对象.关联类属性_id`
h.book_id
```



##### 关联过滤查询

**由多模型类条件查询一模型类数据**:

语法如下：

```python
关联模型类名小写__属性名__条件运算符=值
```

注意：如果没有"__运算符"部分，表示等于。

```python
# 查询图书，要求图书英雄为"孙悟空"
BookInfo.objects.filter(heroinfo__hname='孙悟空')

# 查询图书，要求图书中英雄的描述包含"八"
BookInfo.objects.filter(heroinfo__hcomment__contains='八')
```

**由一模型类条件查询多模型类数据**:

语法如下：

```
一模型类关联属性名__一模型类属性名__条件运算符=值
```

**注意：如果没有"__运算符"部分，表示等于。**

```python
# 查询书名为“天龙八部”的所有英雄。
HeroInfo.objects.filter(hbook__btitle='天龙八部')

# 查询图书阅读量大于30的所有英雄
HeroInfo.objects.filter(hbook__bread__gt=30)
```



### 修改

```python
# 1. save,  修改模型类对象的属性，然后执行 save() 方法
hero = HeroInfo.objects.get(hname='猪八戒')
hero.hname = '猪悟能'
hero.save()

# 2.update,  模型类.objects.filter().update()，会返回受影响的行数
HeroInfo.objects.filter(hname='沙悟净').update(hname='沙僧')
```

### 删除

```python
# 1）模型类对象.delete()
hero = HeroInfo.objects.get(id=13)
hero.delete()

# 2）模型类.objects.filter().delete()
HeroInfo.objects.filter(id=14).delete()
```





## 查询集 QuerySet

- Django2.0入门教程:ORM之QuerySet API:   https://www.django.cn/course/show-18.html 
- Django2.0入门教程:ORM QuerySet查询:   https://www.django.cn/course/show-31.html 



### QuerySet 类

```
# django\db\models\query.py :: QuerySet

__deepcopy__
__getstate__
__setstate__
__repr__
__len__
__iter__
__bool__
__getitem__
__and__
__or__
iterator
aggregate           # 使用聚合函数
count               # 返回数据库中匹配查询(QuerySet)的对象数量。
get(**kwargs)       # 返回与所给筛选条件相匹配的对象，返回结果有且只有一个，如果符合筛选条件的对象超过一个或者没有都会抛出错误。
create              # 新增一条数据
bulk_create         # 批量新增
bulk_update         # 批量更新
get_or_create       # 获取, 如果不存在则新增
update_or_create    # 更新, 如果不存在则新增
earliest
latest
first               # 返回第一条记录
last                # 返回最后一条记录
in_bulk(self, id_list=None, *, field_name='pk')  # 批量查询
delete              # 删除当前结果或结果集
update              # 更新
exists              # 如果 QuerySet 是否包含数据
explain
raw                 # 接收一个原始的SQL查询
values(*field)      # 返回一个ValueQuerySet, 特殊的QuerySet，运行后得到的并不是一系列model的实例化对象，而是一个可迭代的字典序列
values_list(*field) # 与values()相似，它返回的是一个元组序列，values返回的是一个字典序列
dates              # 根据日期获取查询集
datetimes(field_name, kind, order='ASC', tzinfo=None)   # 根据时间获取查询集
none               # 创建空的查询集
all                # 查询所有结果
filter(**kwargs)   # 它包含了与所给筛选条件相匹配的对象
exclude            # 它包含了与所给筛选条件不匹配的对象
complex_filter
union               # 并集
intersection        # 交集
difference          # 差集
select_for_update   # 锁住选择的对象，直到事务结束。
select_related      # 附带查询关联对象
prefetch_related    # 预先查询
annotate
order_by(*field)    # 对查询结果排序
distinct         # 从返回结果中剔除重复纪录
extra            # 附加SQL查询
reverse          # 对查询结果反向排序
defer            # 不加载指定字段
only             # 只加载指定的字段
using            # 选择数据库
ordered          # property, Return True if the QuerySet is ordered
db
resolve_expression
alters_data
as_manager
model
query
queryset_only
```



查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。

当调用如下过滤器方法时，Django 会返回查询集（而不是简单的列表）：

- all()：返回所有数据。
- filter()：返回满足条件的数据。
- exclude()：返回满足条件之外的数据。
- order_by()：对结果进行排序。

对查询集可以再次调用 过滤器 进行过滤，如

```python
BookInfo.objects.filter(bread__gt=30).order_by('bpub_date')
```

**从SQL的角度讲，查询集与select语句等价，过滤器像where、limit、order by子句。**

**判断某一个查询集中是否有数据**：

- exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。



### 特性 - 惰性执行

创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用

例如，当执行如下语句时，并未进行数据库查询，只是创建了一个查询集qs

```python
qs = BookInfo.objects.all()
```

继续执行遍历迭代操作后，才真正的进行了数据库的查询

```python
for book in qs:
    print(book.btitle)
```

### 特性 - 缓存

使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

**情况一**：如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。

```python
from booktest.models import BookInfo
[book.id for book in BookInfo.objects.all()]
[book.id for book in BookInfo.objects.all()]
```

**情况二**：经过存储后，可以重用查询集，第二次使用缓存中的数据。

```python
qs=BookInfo.objects.all()
[book.id for book in qs]
[book.id for book in qs]
```



### 限制查询集

可以对查询集进行取下标或切片操作，等同于 sql 中的 limit 和 offset 子句。

> 注意：不支持负数索引。

**对查询集进行切片后返回一个新的查询集，不会立即执行查询。**

如果获取一个对象，直接使用 [0]，等同于 [0:1].get()，但是如果没有数据，[0] 引发 IndexError 异常，[0:1].get() 如果没有数据引发 DoesNotExist 异常。

示例：获取第1、2项，运行查看。

```python
qs = BookInfo.objects.all()[0:2]
```





## 管理器 Manager

管理器是Django的模型进行数据库操作的接口，Django应用的每个模型类都拥有至少一个管理器。

我们在通过模型类的 **objects** 属性提供的方法操作数据库时，即是在使用一个管理器对象objects。当没有为模型类定义管理器时，Django 会为每一个模型类生成一个名为 objects 的管理器，它是 **models.Manager** 类的对象。

### 自定义管理器的方法和用途

可以自定义管理器，并应用到模型类上。

自定义管理器类主要用于两种情况：

**1. 修改原始查询集，重写all()方法。**

1）打开 booktest/models.py 文件，定义类 BookInfoManager

```python
#图书管理器
class BookInfoManager(models.Manager):
    def all(self):
        #默认查询未删除的图书信息
        #调用父类的成员语法为：super().方法名
        return super().filter(is_delete=False)
```

2）在模型类 BookInfo 中定义管理器

```python
class BookInfo(models.Model):
    # ...
    books = BookInfoManager()
```

3）使用方法

```python
BookInfo.books.all()
```



**2. 在管理器类中补充定义新的方法**

1）打开 booktest/models.py 文件，定义方法 create。

```python
class BookInfoManager(models.Manager):
    #创建模型类，接收参数为属性赋值
    def create_book(self, title, pub_date):
        book = self.model()  # 创建模型类对象, self.model 可以获得模型类
        book.btitle = title
        book.bpub_date = pub_date
        book.bread=0
        book.bcommet=0
        book.is_delete = False
        book.save()  # 将数据插入进数据表
        return book
```

2）为模型类 BookInfo 定义管理器 books 语法如下

```python
class BookInfo(models.Model):
    # ...
    books = BookInfoManager()
```

3）调用语法如下：

```python
book=BookInfo.books.create_book("abc", date(1980,1,1))
```



