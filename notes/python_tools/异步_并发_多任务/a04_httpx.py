import asyncio
import httpx
from time import time

URL_GET = 'https://www.httpbin.org/get'


async def _spend_time_to_do():
    # 同步的 httpx, httpx.get 与 requests.get 一样, 也不是异步
    # return httpx.get(URL_GET, params=dict(name='Martin'))

    # 异步的 httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get(URL_GET, timeout=20)  # 源码timeout默认是5秒
        return resp


async def main(i):
    # 测试的耗时操作
    # resp = await asyncio.sleep(3)
    # 真实的耗时操作
    resp = await _spend_time_to_do()
    print(i+1, resp.status_code if resp else 'Hello')


if __name__ == '__main__':
    s = time()
    loop = asyncio.get_event_loop()
    tasks = [main(i) for i in range(100)]
    future = asyncio.wait(tasks)
    loop.run_until_complete(future)
    print('time cost: ', time() - s)  # time cost:  10秒左右  迅速完成100个请求
