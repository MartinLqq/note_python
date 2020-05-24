# python 进程的创建，守护进程

https://www.cnblogs.com/WiseAdministrator/articles/10711227.html





# python实现守护进程、守护线程、守护非守护并行

##  守护进程

将子进程设置为守护进程后，若父进程退出则子进程也退出。防止产生僵尸进程。 



### 1、守护子进程

主进程创建守护进程

1. 守护进程会在主进程代码执行结束后就终止
2. 守护进程内无法再开启子进程,否则抛出异常：`AssertionError: daemonic processes are not allowed to havechildren`

注意：进程之间是互相独立的，主进程代码运行结束，守护进程随即终止

```python
from multiprocessing import Process
import os,time,random
 
def task():
  print('%s is running' %os.getpid())
  time.sleep(2)
  print('%s is done' %os.getpid())
 
  #守护进程内无法再开启子进程,否则抛出异常
  # p = Process(target=time.sleep, args=(3,))
  # p.start()
 
if __name__ == '__main__':
  p=Process(target=task)
  p.daemon = True #1、必须在p.start()之前
  p.start()
  print('主')
```

输出结果如下：

> 主

原因如下：

> 主进程程序启动执行到p子进程，由于子进程需要开辟内存空间，由于需要耗费时间，所以主进程会首先输出“主”，由于主进程执行完毕，那么守护子进程p也就被干掉了，随之主进程也就退出了.

如果上面代码加上 `p.join()`

```python
if __name__ == '__main__':
  p=Process(target=task)
  p.daemon = True #1、必须在p.start()之前
  p.start()
  p.join()
  print('主')
```

那么程序会输出如下：

> 14732 is running
>
> 14732 is done
> 主

原因如下:

> `join` 是起到阻塞作用，子进程执行完毕，才执行主进程，所以加上 `join`.
>
> 1、执行到 `join`，是起到阻塞作用，就会执行子进程，然后执行完毕，再执行主进程.
>
> 2、也可以这样理解，执行到 `join`，由于主进程`print(“主”)` 没有执行完，所以守护进程不会被干掉，继续执行



###  2、守护子进程、非守护子进程并存

再来看一个，子进程既有守护子进程，又包含非守护子进程

```python
from multiprocessing import Process
import time

def foo():
  print(123)
  time.sleep(1)
  print("end123")
 
def bar():
  print(456)
  time.sleep(3)
  print("end456")
 
if __name__ == '__main__':
  p1=Process(target=foo)
  p2 = Process(target=bar)
  p1.daemon=True
  p1.start()
  p2.start()
  print("main-------")
```

输出如下：

> main-------
> 456
> end456

 原因如下:

> 由于p1,p2都是子进程，需要开辟内存空间，需要耗费时间，所以会优先输出主进程“main”,由于p1是守护子进程，p2是非守护子进程，当主进程执行完毕（注意之类主进程还没有退出，因为还有p2非守护进程），p1守护进程也就退了，但是还有一个p2非守护进程，所以p2会执行自己的代码任务，当p2执行完毕，那么主进程也就退出了，进而整个程序就退出了 





##  守护线程

### 1、守护子线程

无论是进程还是线程，都遵循：`守护xxx` 会等待 `主xxx` 运行完毕后被销毁 

需要强调的是：运行完毕并非终止运行

1.对主进程来说，运行完毕指的是主进程代码运行完毕 

2.对主线程来说，运行完毕指的是主线程所在的进程内所有非守护线程统统运行完毕，主线程才算运行完毕

详细解释： 

1 主进程在其代码结束后就已经算运行完毕了（守护进程在此时就被回收）,然后主进程会一直等非守护的子进程都运行完毕后回收子进程的资源(否则会产生僵尸进程)，才会结束.

2 主线程在其他非守护线程运行完毕后才算运行完毕（守护线程在此时就被回收）。因为主线程的结束意味着进程的结束，进程整体的资源都将被回收，而进程必须保证非守护线程都运行完毕后才能结束。

我们先来看一个例子

```python
from multiprocessing import Process
from threading import Thread
import os,time,random

def task():
  # t=Thread(target=time.sleep,args=(3,))
  # t.start()
  print('%s is running' %os.getpid())
  time.sleep(2)
  print('%s is done' %os.getpid())
 
if __name__ == '__main__':
  t=Thread(target=task)
  t.daemon = True
  t.start()
  print('主')
```

 输出如下：

> 13368 is running
> 主

原因是： 

> 在执行到守护子线程t，由于主线程子线程通用一块内存，所以不存在不同进程创建各自空间，所以就先输出子进程的执行任务代码，所以输出 `print(‘%s is running' %os.getpid())`，由于`time.sleep(2)`，所以就会执行主线程“main”,然后主线程执行完毕，那么即使2秒过后，由于主线程执行完毕，那么子守护线程也就退出了，所以 `print(‘%s is done' %os.getpid())` 就不会执行了



### 2、守护子线程非守护子进程并存 

```python
from threading import Thread
import time

def foo():
  print(123)
  time.sleep(1)
  print("end123")
 
def bar():
  print(456)
  time.sleep(3)
  print("end456")
 
if __name__ == '__main__':
  t1=Thread(target=foo)
  t2 = Thread(target=bar)
 
  t1.daemon=True
 
  t2.start()
  t1.start()
  print("main-------")
```

输出如下：

> 456
> 123
> main-------
>
> end123
>
> end456

原因是： 

> t1是守护子线程，t2非守护子线程，跟主线程使用一块内存，所以会输出t1,t1子线程的任务代码，所以执行456，123由于t1,t2都有睡眠时间，所以执行主线程代码，然后对主线程来说，运行完毕指的是主线程所在的进程内所有非守护线程统统运行完毕，主线程才算运行完毕，所以会执行t1,t2睡眠后的任务代码，然后程序退出。 
>
> 我们会问为什么t1守护子线程，也会执行sleep后的代码，不是说主线程代码执行完毕，守护线程就被干掉了吗？这里要注意是对主线程来说，运行完毕指的是主线程所在的进程内所有非守护线程统统运行完毕，主线程才算运行完毕，当时t2还没执行完毕





# multiprocessing.pool

Pool可以提供指定数量的进程供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来它。 

## 1、使用进程池（阻塞）

```python
import multiprocessing
import time

def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in range(4):
        msg = "hello %d" %(i)
        pool.apply(func, (msg, ))   # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()   # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print("Sub-process(es) done.")
```

**一次执行结果:**

```python
msg: hello 0
end
msg: hello 1
end
msg: hello 2
end
msg: hello 3
end
Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~
Sub-process(es) done.
```





## 2、使用进程池（非阻塞）

```python
import multiprocessing
import time

def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=3)
    for i in range(4):
        msg = "hello %d" % i
        pool.apply_async(func, (msg, ))
    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()
    print("Sub-process(es) done.")

```

**一次执行结果:**

```python
Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~
msg: hello 0
msg: hello 1
msg: hello 2
end
msg: hello 3
end
end
end
Sub-process(es) done.
```

**函数解释**：

- `apply_async(func[, args[, kwds[, callback]]])` 它是**非阻塞**，`apply(func[, args[, kwds]])` 是**阻塞**的.
- `close()`   关闭pool，使其不在接受新的任务。
- `terminate()`   结束工作进程，不在处理未完成的任务。
- `join()`   主进程阻塞，等待子进程的退出，`join` 方法要在 `close` 或 `terminate` 之后使用。

**执行说明**：

> 创建一个进程池pool，并设定进程的数量为3，range(4)会相继产生四个对象[0, 1, 2, 4]，四个对象被提交到pool中，因pool指定进程数为3，所以0、1、2会直接送到进程中执行，当其中一个执行完事后才空出一个进程处理对象3，所以会出现输出`“msg: hello 3”`出现在`"end"`后。因为为非阻塞，主函数会自己执行自个的，不搭理进程的执行，所以运行完for循环后直接输出`“mMsg: hark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~”`，主程序在`pool.join()`处等待各个进程的结束。



## 3、使用进程池，并关注结果

```python
import multiprocessing
import time

def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")
    return "done " + msg

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(3):
        msg = "hello %d" %(i)
        result.append(pool.apply_async(func, (msg, )))
    pool.close()
    pool.join()
    for res in result:
        print(":::", res.get())  # get()函数得出每个返回结果的值
    print("Sub-process(es) done.")
```

**一次执行结果:**

```python
msg: hello 0
msg: hello 1
msg: hello 2
end
end
end
::: done hello 0
::: done hello 1
::: done hello 2
Sub-process(es) done.
```



## 4、使用多个进程池

```python
import multiprocessing
import os, time, random

def lee():
    print("\nRun task Lee-%s" % (os.getpid()))  # os.getpid()获取当前的进程的ID)
    start = time.time()
    time.sleep(random.random() * 10)  # random.random()随机生成0-1之间的小数
    end = time.time()
    print('Task Lee, runs %0.2f seconds.' % (end - start))

def marlon():
    print("\nRun task Marlon-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 40)
    end = time.time()
    print('Task Marlon runs %0.2f seconds.' % (end - start))

def allen():
    print("\nRun task Allen-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 30)
    end = time.time()
    print('Task Allen runs %0.2f seconds.' % (end - start))

def frank():
    print("\nRun task Frank-%s" % (os.getpid()))
    start = time.time()
    time.sleep(random.random() * 20)
    end = time.time()
    print('Task Frank runs %0.2f seconds.' % (end - start))

if __name__ == '__main__':
    function_list = [lee, marlon, allen, frank]
    print("parent process %s" % (os.getpid()))

    pool = multiprocessing.Pool(4)
    for func in function_list:
        pool.apply_async(func)  # 当有一个进程执行完毕后，会添加一个新的进程到pool中

    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()  # 调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print('All subprocesses done.')
```

 **一次执行结果:**

```python
parent process 7324
Waiting for all subprocesses done...

Run task lee-1096

Run task marlon-5808

Run task allen-8848

Run task frank-12416
Task lee, runs 0.27 seconds.
Task allen runs 17.90 seconds.
Task frank runs 18.78 seconds.
Task marlon runs 19.86 seconds.
All subprocesses done.
```





# multiprocessing.Pool实现守护进程

在 `multiprocessing.Process` 中可以使用`p.daemon=True` 将子进程p设置为守护进程。
那么在 `multiprocessing.Pool` 进程池中怎么实现这个功能呢？ 

```
换句话说：主进程退出后(如Ctrl+C退出)怎么自动停止子进程？
```

 这个模块只能在 `Linux` 中使用.

```python
from multiprocessing import Pool

def run_proc(name):		#子进程要执行的代码
	...

p = Pool(4)		#最多同时执行4个进程(一般为CPU核数),有进程运行完腾出的空间再分配给其他进程运行
for i in range(5):
	p.apply_async(run_proc, args=(i,))	#在进程池中添加进程
p.close()		#执行join()前必须执行close(),表示不能继续添加新的进程了
p.join()		#等待子进程结束再往下执行
```

我们可以通过异常处理的方式，停止进程池中的所有进程来实现

```python
try:
	p = Pool(4)
	for i in range(5):
		p.apply_async(run_proc, args=(i,))
	p.close()
	p.join()
except:
	p.terminate()	#停止进程池中的所有进程
```



#  进程间的通信(Pool+Queue) 

 在 `Manager()` 中引用 `Queue()` 方法来创建通信队列. 

```python
from multiprocessing import Manager, Pool


def write_func(queue):
    for i in "WANG":
        queue.put(i)
        print("写入：%s" % i)


def read_func(queue):
    while True:
        if not queue.empty():
            print("读取：%s" % queue.get())


if __name__ == "__main__":
    # 创建队列,在进程池中专用方法,使用Manager中的Queue来初始化
    queue = Manager().Queue()
    # 创建进程池,不做限制
    pool = Pool(3)
    # 创建写入进程
    write_p = pool.apply(func=write_func, args=(queue,))
    # 创建读取进程
    read_p = pool.apply(func=read_func, args=(queue,))
    # 关闭进程池
    pool.close()

```



pool.apply_async

```python
from multiprocessing import Manager, Pool


def write_func(queue):
    for i in "WANG":
        queue.put(i)
        print("写入：%s" % i)


def read_func(queue):
    result = []
    while len(result) != len("WANG"):
        if not queue.empty():
            result.append(queue.get())
    return result


if __name__ == "__main__":
    ret = []
    # 创建队列,在进程池中专用方法,使用Manager中的Queue来初始化
    queue = Manager().Queue()
    # 创建进程池,不做限制
    pool = Pool(3)
    # 创建写入进程
    ret.append(pool.apply_async(func=write_func, args=(queue,)))
    # 创建读取进程
    ret.append(pool.apply_async(func=read_func, args=(queue,)))
    # 关闭进程池
    pool.close()
    pool.join()
    for i in ret:
        print(i.get())

```

