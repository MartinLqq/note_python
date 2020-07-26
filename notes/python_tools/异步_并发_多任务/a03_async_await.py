import asyncio
from time import time

URL_GET = 'https://www.httpbin.org/get'


async def main(i):
    resp = await asyncio.sleep(3)
    print(i+1, resp.status_code if resp else 'Hello')


if __name__ == '__main__':
    s = time()
    loop = asyncio.get_event_loop()
    tasks = [main(i) for i in range(100)]
    future = asyncio.wait(tasks)
    loop.run_until_complete(future)

    print('time cost: ', time() - s)  # time cost:  3.0052223205566406
