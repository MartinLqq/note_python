import asyncio
from time import time

URL_GET = 'https://www.httpbin.org/get'


@asyncio.coroutine
def main(i):
    resp = yield from asyncio.sleep(3)
    print(i+1, resp.status_code if resp else 'Hello')


if __name__ == '__main__':
    s = time()
    for i in range(100):
        # asyncio.run 方式启动
        asyncio.run(main(i))
    print('time cost: ', time() - s)  # time cost:  300+
