"""
Python内置类型性能分析

timeit 模块

"""
from timeit import Timer

# ----------- 测试 list -------------
MAX = 2000

def append():
    li = []
    for i in range(MAX):
        li.append(i)

def insert():
    li = []
    for i in range(MAX):
        # li.insert(0, i)
        li.insert(-1, i)

def list_range():
    _ = list(range(MAX))

def list_comprehension():
    """列表推导式"""
    _ = [i for i in range(MAX)]

def main1():
    number = 1000
    t1 = Timer(stmt='append()', setup='from __main__ import append')
    t2 = Timer(stmt='insert()', setup='from __main__ import insert')
    t3 = Timer(stmt='list_range()', setup='from __main__ import list_range')
    t4 = Timer(stmt='list_comprehension()', setup='from __main__ import list_comprehension')
    print('append time: ', t1.timeit(number=number))
    print('insert time: ', t2.timeit(number=number))
    print('list_range time: ', t3.timeit(number=number))
    print('list_comprehension time: ', t4.timeit(number=number))


if __name__ == '__main__':
    main1()
