from time import time

import requests

URL_GET = 'https://www.httpbin.org/get'


def _spend_time_to_do():
    return requests.get(URL_GET, params=dict(name='Martin'))


def main(i):
    resp = _spend_time_to_do()
    print(i+1, resp.status_code)


if __name__ == '__main__':
    s = time()
    for i in range(100):
        main(i)
    print('time cost: ', time() - s)
