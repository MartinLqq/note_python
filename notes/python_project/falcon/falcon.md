# falcon 微框架

- 当您的目标是构建快速、可扩展的 REST 风格 API 微服务时， [Falcon](https://falconframework.org/) 是个不错的选择。
- falcon 是一个可靠的、高性能的 Python Web 框架，用于构建大规模应用后端和微服务。Falcon 鼓励 REST 架构风格的 URI 到资源的映射，以花费尽可能少的精力同时又保持高效。
- Falcon 重点关注四个方面：速度、可靠性、灵活性和可调试性。它通过"响应者（responder）" （诸如 `on_get()`、 `on_put()` 等）来实现HTTP。这些响应者接收直接的请求，以及响应对象。

# 资源





# 基本使用

### 安装

Falcon 同时支持 CPython 和 PyPy。 

```bash
 $ pip install falcon 
```

> CPython
>
>  尽管 falcon 已经足够快，但是如果想在生产环境中获得额外的速度提升，可以使用 Cython 扩展来编译Falcon。 

### WSGI 服务器

1. Linux 上可以使用 Gunicorn

```bash
$ pip install gunicorn
$ gunicorn -b '0.0.0.0:8000'  main:app
```

2. Windows 上没有 Gunicorn 和 uWSGI ,  可以使用 Waitress WSGI server

```bash
$ pip install waitress
$ waitress-serve --port=8000 main:app
# 或
$ python -m waitress --port=8000 main:app
```



### 快速开始

创建一个 main.py

```python
import falcon

class HelloResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'hello world\n'

app = falcon.App()
app.add_route('/', HelloResource())
```

运行

```bash
$ gunicorn -b '0.0.0.0:8000'  main:app
```

测试

```bash
$ curl localhost:8000/

# 或安装 httpie 命令, 进行测试
$ pip install httpie
$ http :8000/
# 或
$ python -m httpie :8000/
```





# 较完整的应用

见当前路径下的代码





# 更多

- 见文档:   https://falcon.readthedocs.io/en/stable/user/tutorial.html#tutorial 



1.  use [MessagePack](http://msgpack.org/) instead of JSON 
2. Testing your application
3. Refactoring for testability
4. Functional tests
5. Serving Images
6. Introducing Hooks
7. Error Handling

较完整的例