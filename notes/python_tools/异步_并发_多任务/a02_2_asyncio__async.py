import asyncio
from time import time

URL_GET = 'https://www.httpbin.org/get'


@asyncio.coroutine
def main(i):
    resp = yield from asyncio.sleep(3)
    print(i+1, resp.status_code if resp else 'Hello')


if __name__ == '__main__':
    s = time()

    # 1.创建一个事件循环
    loop = asyncio.get_event_loop()
    # 2.将异步对象加入事件队列
    tasks = [main(i) for i in range(100)]
    future = asyncio.wait(tasks)
    # 3.执行事件队列, 直到最晚的一个事件被处理完毕后结束
    loop.run_until_complete(future)

    print('time cost: ', time() - s)  # time cost:  3.008030414581299
