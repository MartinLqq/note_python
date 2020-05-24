# asyncio

asyncio 是 python3.4 版本引入到标准库，python3.5又加入了 async/await 特性。

### 资源

- [python中asyncio模块](https://www.jianshu.com/p/50384d0d3940)
- [深入理解Python异步编程（上）](https://www.jianshu.com/p/fe146f9781d2)
- [Python Asyncio 精选资源列表](https://github.com/chenjiandongx/awesome-asyncio-cn)      (   [Awesome-asyncio](https://github.com/timofurrer/awesome-asyncio)  中文版 )
- [谈谈Python协程技术的演进](https://segmentfault.com/a/1190000012291369)





### 同步与异步

- 同步是指完成事务的逻辑，先执行第一个事务，如果阻塞了，会一直等待，直到这个事务完成，再执行第二个事务，顺序执行。

- 异步是和同步相对的，异步是指在处理调用这个事务的之后，不会等待这个事务的处理结果，直接处理第二个事务去了，通过状态、通知、回调来通知调用者处理结果。

### asyncio 是干什么的？

- 异步网络操作
- 并发
- 协程



### aio-libs

-  Github:  https://github.com/aio-libs 
- 基于 asyncio 的高质量的库集合,  例如: 
  1.  [aiohttp](https://github.com/aio-libs/aiohttp) :  Asynchronous HTTP client/server framework for asyncio and Python
     - aiohttp 框架的第三方插件:   https://docs.aiohttp.org/en/latest/third_party.html 
  2.  [aiopg](https://github.com/aio-libs/aiopg) :  aiopg is a library for accessing a PostgreSQL database from the asyncio
  3.  [aioredis](https://github.com/aio-libs/aioredis) :   asyncio (PEP 3156) Redis support 
  4.  [aiomysql](https://github.com/aio-libs/aiomysql) :  aiomysql is a library for accessing a MySQL database from the asyncio
  5.  [aiobotocore](https://github.com/aio-libs/aiobotocore) :   asyncio support for botocore library using aiohttp 
  6. [aiodocker](https://github.com/aio-libs/aiodocker)  :  Python Docker API client based on asyncio and aiohttp 
  7. ...

The set of asyncio-based libraries built with high quality 



# 异步 web 框架

### `Tornado`

### `Twisted`

### `Japronto`

- Github:   https://github.com/squeaky-pl/japronto 
- 此框架不再更新,  仅维护现有问题

### `aiohttp`

# python实现定时任务

## 1、while循环中使用sleep

缺点：不容易控制，而且是个阻塞函数

```
def timer(n):  
    ''''' 
    每n秒执行一次 
    '''  
    while True:    
        print(time.strftime('%Y-%m-%d %X',time.localtime()))    
        yourTask()  # 此处为要执行的任务    
        time.sleep(n)
```

## 2、schedule模块

优点：可以管理和调度多个任务,可以进行控制
 缺点：阻塞式函数

```
import schedule
import time
import datetime

def job1():
    print('Job1:每隔10秒执行一次的任务，每次执行2秒')
    print('Job1-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(2)
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

def job2():
    print('Job2:每隔30秒执行一次，每次执行5秒')
    print('Job2-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(5)
    print('Job2-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job3():
    print('Job3:每隔1分钟执行一次，每次执行10秒')
    print('Job3-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(10)
    print('Job3-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job4():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job5():
    print('Job5:每隔5秒到10秒执行一次，每次执行3秒')
    print('Job5-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(3)
    print('Job5-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
    schedule.every(10).seconds.do(job1)
    schedule.every(30).seconds.do(job2)
    schedule.every(1).minutes.do(job3)
    schedule.every().day.at('17:49').do(job4)
    schedule.every(5).to(10).seconds.do(job5)
    while True:
        schedule.run_pending()
```

## 3、Threading模块中的Timer

优点：非阻塞
 缺点：不易管理多个任务

```
from threading import Timer
import datetime
# 每隔两秒执行一次任务
def printHello():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = Timer(2, printHello)
    t.start()

if __name__ == "__main__":
    printHello()
```

## 4、sched模块

sched模块实现了一个时间调度程序，该程序可以通过单线程执行来处理按照时间尺度进行调度的时间。
 通过调用`scheduler.enter(delay,priority,func,args)`函数，可以将一个任务添加到任务队列里面，当指定的时间到了，就会执行任务(**func函数**)。

-  *delay*：任务的间隔时间。
-  *priority*：如果几个任务被调度到相同的时间执行，将按照priority的增序执行这几个任务。
-  *func*：要执行的任务函数
-  *args*：func的参数

```
import time, sched
import datetime

s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print('Now Time:',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),a)

def print_some_times():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    s.enter(10,1,print_time)
    s.enter(5,2,print_time,argument=('positional',))
    s.run()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print_some_times()
```

执行结果为：

```
2018-09-20 16:25:03
Now Time: 2018-09-20 16:25:08 positional
Now Time: 2018-09-20 16:25:13 default
2018-09-20 16:25:13

Process finished with exit code 0
```

按顺序执行任务：

```
import time, sched
import datetime

s = sched.scheduler(time.time, time.sleep)


def event_fun1():
    print("func1 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def perform1(inc):
    s.enter(inc, 0, perform1, (inc,))
    event_fun1()


def event_fun2():
    print("func2 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def perform2(inc):
    s.enter(inc, 0, perform2, (inc,))
    event_fun2()


def mymain(func, inc=2):
    if func == "1":
        s.enter(0, 0, perform1, (10,))# 每隔10秒执行一次perform1
    if func == "2":
        s.enter(0, 0, perform2, (20,))# 每隔20秒执行一次perform2
if __name__ == '__main__':
    mymain('1')
    mymain('2')
    s.run()
```

执行结果为：

```
E:\virtualenv\pachong\Scripts\python.exe F:/workspace/project_01/demo_09.py
func1 Time: 2018-09-20 16:30:28
func2 Time: 2018-09-20 16:30:28
func1 Time: 2018-09-20 16:30:38
func2 Time: 2018-09-20 16:30:48
func1 Time: 2018-09-20 16:30:48
func1 Time: 2018-09-20 16:30:58
func2 Time: 2018-09-20 16:31:08
func1 Time: 2018-09-20 16:31:08
func1 Time: 2018-09-20 16:31:18
func2 Time: 2018-09-20 16:31:28
func1 Time: 2018-09-20 16:31:28
func1 Time: 2018-09-20 16:31:38
```

s.run()会阻塞当前线程的执行
 可以用

```
t=threading.Thread(target=s.run)
t.start()
```

也可以用`s.cancal(action)`来取消sched中的某个action

## 5、定时框架APScheduler

> APSScheduler是python的一个定时任务框架，它提供了基于日期date、固定时间间隔interval、以及linux上的crontab类型的定时任务。该矿机不仅可以添加、删除定时任务，还可以将任务存储到数据库中、实现任务的持久化。

### APScheduler四种组件

- triggers（触发器）：触发器包含调度逻辑，每一个作业有它自己的触发器，用于决定接下来哪一个作业会运行，除了他们自己初始化配置外，触发器完全是无状态的。
- **job stores**（作业存储）：用来存储被调度的作业，默认的作业存储器是简单地把作业任务保存在内存中，其它作业存储器可以将任务作业保存到各种数据库中，支持MongoDB、Redis、SQLAlchemy存储方式。当对作业任务进行持久化存储的时候，作业的数据将被序列化，重新读取作业时在反序列化。
- **executors**（执行器）：执行器用来执行定时任务，只是将需要执行的任务放在新的线程或者线程池中运行。当作业任务完成时，执行器将会通知调度器。对于执行器，默认情况下选择ThreadPoolExecutor就可以了，但是如果涉及到一下特殊任务如比较消耗CPU的任务则可以选择ProcessPoolExecutor，当然根据根据实际需求可以同时使用两种执行器。
- **schedulers**（调度器）：调度器是将其它部分联系在一起，一般在应用程序中只有一个调度器，应用开发者不会直接操作触发器、任务存储以及执行器，相反调度器提供了处理的接口。通过调度器完成任务的存储以及执行器的配置操作，如可以添加。修改、移除任务作业。

### APScheduler七种调度器

- BlockingScheduler：适合于只在进程中运行单个任务的情况，通常在调度器是你唯一要运行的东西时使用。
- BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
- AsyncIOScheduler：适合于使用asyncio异步框架的情况
- GeventScheduler: 适合于使用gevent框架的情况
- TornadoScheduler: 适合于使用Tornado框架的应用
- TwistedScheduler: 适合使用Twisted框架的应用
- QtScheduler: 适合使用QT的情况

### APScheduler四种存储

- MemoryJobStore
- sqlalchemy
- mongodb
- redis

### APScheduler三种任务触发器

- **data**：固定日期触发器：任务只运行一次，运行完毕自动清除；若错过指定运行时间，任务不会被创建
- **interval**：时间间隔触发器
- **cron**：cron风格的任务触发

#### 示例1、阻塞+固定时间

```
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    # 该示例代码生成了一个BlockingScheduler调度器，使用了默认的任务存储MemoryJobStore，以及默认的执行器ThreadPoolExecutor，并且最大线程数为10。
    
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    scheduler = BlockingScheduler()
    # 采用阻塞的方式

    # 采用固定时间间隔（interval）的方式，每隔5秒钟执行一次
    scheduler.add_job(job, 'interval', seconds=5)
    
    scheduler.start()
```

#### 示例2、阻塞+特定时刻

```
import time
from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
if __name__ == '__main__':
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    scheduler = BlockingScheduler()
    # 采用阻塞的方式
    
    # 采用date的方式，在特定时间只执行一次
    scheduler.add_job(job, 'date', run_date='2018-09-21 15:30:00')

    scheduler.start() 
```

#### 示例3、非阻塞+固定时间

```
import time
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print('job:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
    scheduler = BackgroundScheduler()
    # 采用非阻塞的方式

    # 采用固定时间间隔（interval）的方式，每隔3秒钟执行一次
    scheduler.add_job(job, 'interval', seconds=3)
    # 这是一个独立的线程
    scheduler.start()
    
    # 其他任务是独立的线程
    while True:
        print('main-start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
        print('main-end:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
```

运行结果为：

```
main-start: 2018-09-21 15:54:28
main-end: 2018-09-21 15:54:30
main-start: 2018-09-21 15:54:30
job: 2018-09-21 15:54:31
main-end: 2018-09-21 15:54:32
main-start: 2018-09-21 15:54:32
main-end: 2018-09-21 15:54:34
main-start: 2018-09-21 15:54:34
job: 2018-09-21 15:54:34
main-end: 2018-09-21 15:54:36
main-start: 2018-09-21 15:54:36
```

#### 示例4、非阻塞+特定时刻

```
import time
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print('job:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

if __name__ == '__main__':
    # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
    scheduler = BackgroundScheduler()
    # 采用非阻塞的方式

    # 采用date的方式，在特定时间里执行一次
    scheduler.add_job(job, 'date', run_date='2018-09-21 15:53:00')
    # 这是一个独立的线程
    scheduler.start()

    # 其他任务是独立的线程
    while True:
        print('main-start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
        print('main-end:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
```

运行结果为：

```
main-start: 2018-09-21 15:52:57
main-end: 2018-09-21 15:52:59
main-start: 2018-09-21 15:52:59
job: 2018-09-21 15:53:00
main-end: 2018-09-21 15:53:01
```

#### 示例5、非阻塞+corn

```
import time
from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用
    scheduler = BackgroundScheduler()
    # 采用非阻塞的方式

    # 采用corn的方式
    scheduler.add_job(job, 'cron', day_of_week='fri', second='*/5')
    '''
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)
    day (int|str) – day of the (1-31)
    week (int|str) – ISO week (1-53)
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – hour (0-23)
    minute (int|str) – minute (0-59)
    econd (int|str) – second (0-59)
            
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
        
    *    any    Fire on every value
    */a    any    Fire every a values, starting from the minimum
    a-b    any    Fire on any value within the a-b range (a must be smaller than b)
    a-b/c    any    Fire every c values within the a-b range
    xth y    day    Fire on the x -th occurrence of weekday y within the month
    last x    day    Fire on the last occurrence of weekday x within the month
    last    day    Fire on the last day within the month
    x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
    '''
    scheduler.start()
    
    # 其他任务是独立的线程
    while True:
        print('main-start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
        print('main-end:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
```

运行结果：

```
main-start: 2018-09-21 16:02:55
main-end: 2018-09-21 16:02:57
main-start: 2018-09-21 16:02:57
main-end: 2018-09-21 16:02:59
main-start: 2018-09-21 16:02:59
2018-09-21 16:03:00
main-end: 2018-09-21 16:03:01
main-start: 2018-09-21 16:03:01
main-end: 2018-09-21 16:03:03
main-start: 2018-09-21 16:03:03
2018-09-21 16:03:05
main-end: 2018-09-21 16:03:05
main-start: 2018-09-21 16:03:05
main-end: 2018-09-21 16:03:07
main-start: 2018-09-21 16:03:07
main-end: 2018-09-21 16:03:09
main-start: 2018-09-21 16:03:09
2018-09-21 16:03:10
```

#### 示例6、阻塞+corn

```
import time
from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用
    scheduler = BackgroundScheduler()
    # 采用阻塞的方式

    # 采用corn的方式
    scheduler.add_job(job, 'cron', day_of_week='fri', second='*/5')
    '''
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)
    day (int|str) – day of the (1-31)
    week (int|str) – ISO week (1-53)
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – hour (0-23)
    minute (int|str) – minute (0-59)
    econd (int|str) – second (0-59)
            
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
        
    *    any    Fire on every value
    */a    any    Fire every a values, starting from the minimum
    a-b    any    Fire on any value within the a-b range (a must be smaller than b)
    a-b/c    any    Fire every c values within the a-b range
    xth y    day    Fire on the x -th occurrence of weekday y within the month
    last x    day    Fire on the last occurrence of weekday x within the month
    last    day    Fire on the last day within the month
    x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
    '''

    scheduler.start()
```

#### 示例7、mongodb存储job

```
import time
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore

def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
if __name__ == '__main__':
    # mongodb存储job
    scheduler = BlockingScheduler()
    client = MongoClient(host='127.0.0.1', port=27017)
    store = MongoDBJobStore(collection='job', database='test', client=client)
    scheduler.add_jobstore(store)
    scheduler.add_job(job, 'interval', second=5)
    scheduler.start()
```





## 6、异步框架celery

[Celery 中文手册 (不完整)](https://www.celerycn.io/)

4.3.0 英文手册 http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html

