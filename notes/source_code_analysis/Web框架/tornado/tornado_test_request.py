# coding=utf-8
from threading import Thread

import requests


def fetch():
    while True:
        try:
            # res = requests.get('http://127.0.0.1:8005/blocking/')
            res = requests.get('http://127.0.0.1:8005/non-blocking/')
        except Exception as err:
            print(err)
            continue
        print(res)


if __name__ == '__main__':
    th_lst = []
    for i in range(2):
        th = Thread(target=fetch)
        th_lst.append(th)
        th.start()
    for th in th_lst:
        th.join()


"""
non-blocking 打印结果示例:
    Non-Blocking
    Non-Blocking
    deal with one request 1594897552.41
    deal with one request 1594897552.41
    Non-Blocking
    Non-Blocking
    deal with one request 1594897557.42
    deal with one request 1594897557.42
结果: 同一时刻打印两条, 然后睡5秒, 下一次也同时处理所有请求


blocking 打印结果示例:
    deal with one request 1594897625.2
    deal with one request 1594897630.2
    deal with one request 1594897635.21
    deal with one request 1594897640.21
    deal with one request 1594897645.21
    deal with one request 1594897650.21

结果: 无论请求有多少个, 挨个处理, 处理一次请求睡5秒
"""
