# <Title>: Python 并行分布式框架 Celery

### [Celery 3.1 中文文档](http://docs.jinkan.org/docs/celery/getting-started/first-steps-with-celery.html)

### [Celery 4.2.0 documentation](http://docs.celeryproject.org/en/latest/index.html)



Celery(芹菜) 是一个异步任务队列/基于分布式消息传递的作业队列。

Celery用于生产系统每天处理数以**百万计**的任务。

Celery是用**Python**编写的，但该协议可以在任何语言实现。它也可以与其他语言通过 webhooks 实现。

Celery建议的消息队列是**RabbitMQ**，但提供有限支持Redis, Beanstalk, MongoDB, CouchDB, 和数据库（使用SQLAlchemy的或Django的 ORM）。

Celery是易于集成Django, Pylons and Flask，使用 django-celery, celery-pylons and Flask-Celery 附加包即可。





# Celery中几个基本的概念

### 什么是broker？

broker是一个消息传输的中间件,  消息队列,    每当应用程序调用celery的异步任务的时候，会向broker传递消息，而后celery的worker将会取到消息，进行对于的程序执行

这个Broker有几个方案可供选择：RabbitMQ (消息队列)，[Redis](http://lib.csdn.net/base/redis)（缓存数据库），[数据库](http://lib.csdn.net/base/mysql)（不推荐），等等

### 什么是backend？

通常程序发送的消息，发完就完了，可能都不知道对方时候接受了。为此，celery实现了一个backend，用于存储这些消息以及celery执行的一些消息和结果。



# Celery的[架构](http://lib.csdn.net/base/architecture)

**消息中间件**（broker），

**任务执行单元**（worker）

**任务执行结果存储**（task result store）

![img](http://static.open-open.com/lib/uploadImg/20150314/20150314100608_187.png)



### 消息中间件-Broker

**Celery本身不提供消息服务**，但是可以方便地和第三方提供的消息中间件集成。包括，RabbitMQ, [Redis](http://lib.csdn.net/base/redis), [MongoDB](http://lib.csdn.net/base/mongodb) , SQLAlchemy, Django ORM

### 任务执行单元-Worker

Worker是**Celery提供的任务执行的单元**，worker并发的运行在分布式的系统节点中。

### 任务结果存储-Backend

用来存储Worker执行的任务的结果，Celery支持以不同方式存储任务的结果，包括AMQP, [redis](http://lib.csdn.net/base/redis)，memcached, [mongodb](http://lib.csdn.net/base/mongodb)，SQLAlchemy, Django ORM等。

![img](https://i.loli.net/2016/12/10/584bbf78e1783.png)




# 开始使用 Celery

使用celery包含三个方面：1. 定义任务函数。 2. 运行celery服务。 3. 客户应用程序的调用。



### A 初始用法

(1)   创建一个文件 `tasks.py`输入下列代码：

```python
from celery import Celery
 
broker = 'redis://127.0.0.1:6379/5'
backend = 'redis://127.0.0.1:6379/6'
 

# 创建celery实例app, 指定任务名tasks（和文件名一致），传入broker和backend
app = Celery('tasks', broker=broker, backend=backend)		


@app.task
def add(x, y):			# 创建一个任务函数add
    return x + y
```

(2)   启动celery服务

```
#  进入tasks.py所在目录执行命令:

celery -A tasks worker  --loglevel=info
```

(3)  在交互式终端调用异步任务

**注意：**如果把返回值赋值给一个变量，那么原来的应用程序也会被阻塞，需要等待异步任务返回的结果。因此，实际使用中，不需要把结果赋值。

```python
In [0]:from tasks import add		# 导入任务函数
In [1]: r = add.delay(2, 2)			# 任务函数名.delay(传递参数)
In [2]: add.delay(2, 2)
Out[2]: <AsyncResult: 6fdb0629-4beb-4eb7-be47-f22be1395e1d>
 
In [3]: r = add.delay(3, 3)
 
In [4]: r.re
r.ready   r.result  r.revoke
 
In [4]: r.ready()
Out[4]: True
 
In [6]: r.result
Out[6]: 6
 
In [7]: r.get()
Out[7]: 6
```

(4)  在应用程序中调用异步任务

新建一个**\*main.py*** 文件

```python
from tasks import add  
 
add.delay(2, 2)  
```

执行:   python ./main.py

(5)   查看celery执行日志

在celery命令行可以看见celery执行的日志。打开 backend的redis，也可以看见celery执行的信息





### B 抽取Celery配置

Celery 的配置比较多,  查看官方配置文档：http://docs.celeryproject.org/en/latest/userguide/configuration.html



(1)   创建一个python包,  创建几个文件

如 celery_pkg 包

```
☁  celery_pkg   tree
.
├── __init__.py
├── celery.py			# 创建 celery 实例
├── config.py			# 配置文件
└── tasks.py			# 任务函数
```

**celery.py**

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
from celery import Celery
 
app = Celery('celery_pkg', include=['celery_pkg.tasks'])
 
app.config_from_object('celery_pkg.config')	  # 在此创建app没有直接指定broker和backend, 而是指定配置文件
 
if __name__ == '__main__':
    app.start()
```

**config.py**

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'
```

**tasks.py**

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from celery_pkg.celery import app

@app.task
def add(x, y):
    return x + y
```



(2)   启动celery服务

使用方法也很简单，**在 celery_pkg 的同一级目录执行 celery**：

```
celery -A celery_pkg worker -l info
```

(3)   调用异步任务

**main.py**

```python
from celery_pkg.tasks import add  
 
add.delay(2, 2)
```

##### 【----报错解决----】

在win10上运行 celery 4.x 会出现这个问题:

```
ValueError: not enough values to unpack (expected 3, got 0)
```

**解决方法有 2 种:**

第一种

```
启动 worker 时加一个参数 【--pool=solo】
	celery -A celery_pkg worker -l info --pool=solo

再调用任务执行
```

第二种

```
安装 eventlet
	pip install eventlet

启动worker时加一个参数 【-P eventlet】
	celery -A celery_pkg worker -l info -P eventlet

再调用任务执行
```







### C 指定路由到队列

(1)   **tasks.py**

```python
from celery import Celery
 
app = Celery()
app.config_from_object("celeryconfig")


@app.task
def taskA(x,y):				# taskA
    return x + y
 
@app.task
def taskB(x,y,z):			# taskB
     return x + y + z
 
@app.task
def add(x,y):				# add
    return x + y
```

(2)   **celeryconfig.py**

```python
from kombu import Exchange,Queue
 
BROKER_URL = "redis://10.32.105.227:6379/0" 
CELERY_RESULT_BACKEND = "redis://10.32.105.227:6379/0"

# 定义了三个Message Queue, 
# 指明了Queue对应的Exchange		(当使用 Redis 作为broker时，Exchange的名字必须和Queue的名字一样)
# 指明了Queue对应的routing_key
CELERY_QUEUES = (
　　　Queue("default",Exchange("default"),routing_key="default"), 
　　　Queue("for_task_A",Exchange("for_task_A"),routing_key="task_a"),
　　　Queue("for_task_B",Exchange("for_task_B"),routing_key="task_a") 
　)
    
CELERY_ROUTES = {
    'tasks.taskA':{"queue":"for_task_A","routing_key":"task_a"},
    'tasks.taskB":{"queue":"for_task_B","routing_key:"task_b"}
 } 
```

(3)   启动一个work,  并且执行一个任务

<1> 在一台主机上启动一个worker，只执行 for_task_A 队列中的消息

```
# -Q 指定Queue的名字
celery -A tasks worker -l info -n worker.%h -Q for_task_A
```

<2> 然后到另一台主机上执行 taskA 任务

```python
from tasks import *
 
task_A_re = taskA.delay(100,200)
```

执行完上面的代码之后，taskA消息会被立即发送到 for_task_A队列 中去。此时已经启动的worker.atsgxxx 会立即执行taskA任务。



(4)   重复上面的过程，在另外一台机器上启动一个worker专门执行for_task_B中的任务。修改上一步骤的代码，把 taskA 改成 taskB 并执行。

```python
from tasks import *
 
task_B_re = taskB.delay(100,200)
```

(5)   再启动一个 worker 专门执行 add 中的任务

```
from tasks import *
 
add_ret = add.delay(100,200)
```

在之前的 **tasks.py** 文件中还定义了add任务，但是在 celeryconfig.py 文件中没有指定这个任务 route 到哪个Queue中去执行，此时执行add任务的时候，add 会 route 到 **Celery 默认**的名字叫做 **celery** 的队列中去。

但是我们还没有启动worker执行celery中的任务。接下来我们在启动一个worker执行 **'celery'队列** 中的任务

```
celery -A tasks worker -l info -n worker.%h -Q celery 
```





### D  **[Scheduler ( 定时任务，周期性任务 )](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)**

一种常见的需求是每隔一段时间执行一个任务。

在celery中执行定时任务非常简单，只需要设置celery对象的 **CELERYBEAT_SCHEDULE属性** 即可。

(1)   配置如下

**config.py**

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'
 
CELERY_TIMEZONE = 'Asia/Shanghai'
 
from datetime import timedelta
 
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {				# 任务调度器名
         'task': 'celery_pkg.tasks.add',		# 指定任务函数
         'schedule': timedelta(seconds=30),		# 间隔时间, 可直接写一个整数(秒)
         'args': (16, 16)						# 任务函数参数
    },
}
```

注意配置文件需要指定时区。这段代码表示每隔30秒执行 add 函数。一旦使用了 scheduler, 启动 celery需要加上 **-B** 参数。

(2)   启动 celery 服务

```
celery -A proj worker -B -l info
```



(3)   设置多个定时任务

```python
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'taskA_schedule' : {
        'task':'tasks.taskA',
        'schedule':20,
        'args':(5,6)
    },
    'taskB_scheduler' : {
        'task':"tasks.taskB",
        "schedule":200,
        "args":(10,20,30)
    },
    'add_schedule': {
        "task":"tasks.add",
        "schedule":10,
        "args":(1,2)
    }
}
```

定义3个定时任务,   即每隔20s执行taskA任务，参数为(5,6) ;   每隔200s执行taskB任务,   参数为(10,20,30) ; 每隔10s执行add任务，参数为(1,2).   使用 **beat** 参数即可启动定时任务

(4)    启动 Celery 定时服务

```
celery -A tasks beat
```



### E  crontab 实现计划任务

计划任务当然也可以用crontab实现，celery也有crontab模式。

修改 config.py

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

 
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'
 
CELERY_TIMEZONE = 'Asia/Shanghai'
 
from celery.schedules import crontab
 
CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```



当然celery还有更高级的用法，比如 **多个机器 **使用，启用**\*多个 worker*****并发处理** 等。



### 发送任务到队列中

[apply_async( )](http://docs.celeryproject.org/en/master/userguide/calling.html)

[send_task( )](http://docs.celeryproject.org/en/master/reference/celery.html#celery.Celery.send_task)

```python
from celery import Celery
celery = Celery()
celery.config_from_object('celeryconfig')
send_task('tasks.test1', args=[hotplay_id, start_dt, end_dt], queue='hotplay_jy_queue')  
```





### Celery 监控 和 管理  以及 命令帮助

输入 celery -h 可以看到 celery 的命令和帮助

[Monitoring and Management Guide](http://docs.celeryproject.org/en/master/userguide/monitoring.html)







# celery如何使用mongodb保存数据

### **第一步**

安装好mongodb了！就可以使用它了，首先让我们修改celeryconfig.py文件，使celery知道我们有一个新成员要加入我们的项目，它就是mongodb配置的方式如下。

```python
CELERY_IMPORTS = ('tasks')
CELERY_IGNORE_RESULT = False
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 5672
BROKER_URL = 'amqp://'
#CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_BACKEND = 'mongodb'
CELERY_RESULT_BACKEND_SETTINGS = {
        "host":"127.0.0.1",
        "port":27017,
        "database":"jobs",
        "taskmeta_collection":"stock_taskmeta_collection",
}
```

把#CELERY_RESULT_BACKEND = 'amp'注释掉了，但是没有删除目的是对比前后的改变。为了使用mongodb我们简单了配置一下主机端口以及数据库名字等。



### **第二步**

启动 mongodb 数据库：mongod。修改客户端client.py让他能够动态的传人我们的数据，非常简单代码如下。

```python
import sys
from celery import Celery
 
app = Celery()
 
app.config_from_object('celeryconfig')
app.send_task("tasks.say",[sys.argv[1],sys.argv[2]])
```

任务tasks.py不需要修改！

```python
import time
from celery.task import task
 
 
@task
def say(x,y):
        time.sleep(5)
        return x+y
```

### **第三步**

测试代码，先启动celery任务。

```
celery worker -l info --beat
```

再来启动我们的客户端，注意这次启动的时候需要给两个参数！
mongo

```
python client.py welcome landpack
```

等上5秒钟，我们的后台处理完成后我们就可以去查看数据库了。

### **第四步**

查看mongodb，需要启动一个mongodb客户端，启动非常简单直接输入 mongo 。然后是输入一些简单的mongo查询语句。

最后查到的数据结果可能是你不想看到的，因为mongo已经进行了处理。想了解更多可以查看官方的文档。







