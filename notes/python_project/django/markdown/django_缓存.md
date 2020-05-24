# Django 自带缓存

- [官方文档](https://docs.djangoproject.com/zh-hans/2.2/topics/cache/)



# 缓存粒度

1. 站点缓存
2. 视图缓存
   - 使用  `django.views.decorators.cache.cache_page()`  装饰器
   - 或者在 URLconf 路由配置中指定视图缓存
3. 模板片段缓存

# 缓存后端 (缓存位置)

1.  Memcached
   -  python-memcached
   -  pylibmc
2. 数据库缓存
   -  用一个数据库表作为缓存后端 
   -  在多数据库中使用缓存 
3. 文件系统缓存
4. 本地内存缓存
5. 虚拟缓存（用于开发模式）
6. 使用自定义的缓存后台

# 缓存配置

# 底层缓存 API

- django.core.cache.caches 
- django.core.cache.cache





# 下游缓存

-  ISP (互联网服务提供商)
-  代理缓存
-  浏览器缓存