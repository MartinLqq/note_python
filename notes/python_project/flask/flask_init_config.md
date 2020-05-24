# Flask项目初始化

# 搭建虚拟环境

**为什么要搭建虚拟环境?**

在开发过程中, 当需要使用python的某些工具包/框架时需要联网安装,  比如联网安装Flask框架`flask-0.10.1`版本

```
sudo pip install flask==0.10.1
```

- **提示**：使用如上命令, 会将`flask-0.10.1`安装到`/usr/local/lib/python2.7/dist-packages`路径下

- **问题**：如果在一台电脑上, 想开发多个不同的项目, 需要用到同一个包的不同版本, 如果使用上面的命令, 在同一个目录下安装或者更新, 新版本会覆盖以前的版本, 其它的项目就无法运行了.

解决方案:  虚拟环境

  - **作用** : `虚拟环境`可以搭建独立的`python运行环境`, 使得单个项目的运行环境与其它项目互不影响.
  - 所有的`虚拟环境`都位于`/home/`下的隐藏目录`.virtualenvs`下



**如何搭建虚拟环境?**

- 安装虚拟环境的命令 :

```
sudo pip install virtualenv
sudo pip install virtualenvwrapper
```

> 安装完虚拟环境后，如果提示找不到 `mkvirtualenv` 命令，须配置环境变量：

```
# 1、创建目录用来存放虚拟环境
mkdir 
$HOME/.virtualenvs

# 2、打开~/.bashrc文件，并添加如下：
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

# 3、运行
source ~/.bashrc
```

- 创建虚拟环境的命令 :

  - 提示：如果不指定python版本，默认安装的是python2的虚拟环境

  - 在python2中，创建虚拟环境

    ```
    mkvirtualenv 虚拟环境名称
    例 ：
    mkvirtualenv py_flask
    ```

  - 在python3中，创建虚拟环境

    ```
    mkvirtualenv -p python3 虚拟环境名称
    例 ：
    mkvirtualenv -p python3 py3_flask
    ```

- 提示 :

  - 创建虚拟环境需要联网
  - 创建成功后, 会自动工作在这个虚拟环境上
  - 工作在虚拟环境上, 提示符最前面会出现 “虚拟环境名称”



**如何使用虚拟环境?**

- 查看虚拟环境 :

```
# 查看虚拟环境
workon 两次tab键

# 使用虚拟环境
workon 虚拟环境名称

# 退出虚拟环境
deactivate

# 删除虚拟环境
先退出：deactivate
再删除：rmvirtualenv 虚拟环境名称
```



- 查看虚拟环境中安装的包 :  

```
pip freeze
```





# 7行实现Flask应用服务器

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
```



# 运行配置

## 初始化参数

```python
from flask import Flask

app = Flask(__name__, )
```

- import_name
  - Flask程序所在的包(模块)，传 `__name__` 就可以
  - 其可以决定 Flask 在访问静态文件时查找的路径
- static_path
  - 静态文件访问路径(不推荐使用，使用 static_url_path 代替)
- static_url_path
  - 静态文件访问路径，可以不传，默认为：`/ + static_folder`
- static_folder
  - 静态文件存储的文件夹，可以不传，默认为 `static`
- template_folder
  - 模板文件存储的文件夹，可以不传，默认为 `templates`





## 程序加载配置

在 Flask 程序运行的时候，可以给 Flask 设置相关配置，比如：配置 Debug 模式，配置数据库连接地址等等，设置 Flask 配置有以下三种方式：

- 从配置对象中加载(常用):  `app.config.from_object()`
- 从配置文件中加载:  `app.config.from_pyfile()`
- 从环境变量中加载(了解):  `app.config.from_envvar()`



SECRET_KEY 的作用主要是提供一个值做各种 HASH 在加密过程中作为算法的一个参数(salt 或其他). 所以这个值的复杂度也就影响到了数据传输和存储时的复杂度. 





**读取配置**

- app.config.get()
- 在视图函数中使用 current_app.config.get()

> 注：Flask 应用程序将一些常用的配置设置成了应用程序对象的属性，也可以通过属性直接设置/获取某些配置：app.debug = True



## app.run的参数

- 可以指定运行的主机IP地址，端口，是否开启调试模式

```python
app.run(host="0.0.0.0", port=5000, debug = True)
```







# 异常捕获

**HTTP 异常主动抛出**

- abort 方法
  - 抛出一个给定状态代码的 HTTPException 或者 指定响应，例如想要用一个页面未找到异常来终止请求，你可以调用 abort(404)。
- 参数：
  - code – HTTP的错误状态码

```python
# abort(404)
abort(500)
```

> 抛出状态码的话，只能抛出 HTTP 协议的错误状态码



**捕获错误**

- errorhandler 装饰器
  - 注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
- 参数：
  - code_or_exception – HTTP的错误状态码或指定异常
- 例如统一处理状态码为500的错误给用户友好的提示：

```python
@app.errorhandler(500)
def internal_server_error(e):
    return '服务器搬家了'
```

- 捕获指定异常

```python
@app.errorhandler(ZeroDivisionError)
def zero_division_error(e):
    return '除数不能为0'
```







# Flask-Script 扩展

通过使用Flask-Script扩展，可以在Flask服务器启动的时候，通过命令行的方式传入参数，而不仅仅通过app.run()方法中传参.

```python
python hello.py runserver -h ip地址
```

安装 Flask-Script 扩展

```bash
pip install flask-script
```

集成 Flask-Script

```python
from flask import Flask
from flask_script import Manager

app = Flask(__name__)
# 把 Manager 类和应用程序实例进行关联
manager = Manager(app)

@app.route('/')
def index():
    return 'index'

if __name__ == "__main__":
    manager.run()
```

> Flask-Script 还可以为当前应用程序添加脚本命令





# Flask-SQLAlchemy











flask 上下文的实现:   https://segmentfault.com/a/1190000004223296