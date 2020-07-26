# Django Rest Swagger生成api文档

#### 关于swagger

**Swagger 能成为最受欢迎的REST APIs文档生成工具之一，有以下几个原因：**

- Swagger 可以生成一个具有互动性的API控制台，开发者可以用来快速学习和尝试API。
- Swagger 可以生成客户端SDK代码用于各种不同的平台上的实现。
- Swagger 文件可以在许多不同的平台上从代码注释中自动生成。
- Swagger 有一个强大的社区，里面有许多强悍的贡献者。

下面就实战 django rest swagger 为 drf 生成 api 接口文档

#### 环境

- Python3.6
- Django1.11
- django-rest-swagger
- djangorestframework

#### 安装

```
pip install django==1.11.6
pip instal djangorestframework
pip install django-rest-swagger
```

#### 创建项目和app

```
startproject apitest
startapp api
```

#### 配置 rest_api/settings.py

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 加入以下
    'api',
    'rest_framework',
    'rest_framework_swagger',

]
# swagger 配置项
SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        "basic":{
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}


```

#### 配置api/serializer.py

```
# 序列化
from django.contrib.auth.models import User,Group
from  rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =Group
        fields = "__all__"

```

#### 配置api/views.py

```
# 视图
from  django.contrib.auth.models import User,Group
from rest_framework import viewsets
from  api.serializers import UserSerializer,GroupSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    '''查看，编辑用户的界面'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    '''查看，编辑组的界面'''
    queryset = Group
    serializer_class = GroupSerializer

```

#### 配置apitest/urls.py

```
from django.conf.urls import url,include
from django.contrib import admin
from  rest_framework import routers
from  api import views

# 路由
router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet,base_name='user')
router.register(r'groups',views.GroupViewSet,base_name='group')


# 重要的是如下三行
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])



urlpatterns = [
    # swagger接口文档路由
    url(r'^docs/', schema_view, name="docs"),
    url(r'^admin/', admin.site.urls),
    url(r'^',include(router.urls)),
    # drf登录
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))

]

```

#### 最终效果

##### drf 自带的接口 UI

![img](https://upload-images.jianshu.io/upload_images/9505682-af5f900d59faea6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)



##### swagger UI

![img](https://upload-images.jianshu.io/upload_images/9505682-9fa3c0fd06629548.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

