"""
源码分析 | 记录

>>> from __future__ import *        # Done
>>> import records                  # Done
>>> from howdoi import howdoi       # TODO delay
>>> import appdirs                  # Done
>>> import cachelib                 # Done
>>> import pygments                 # Undo
>>> import pyquery                  # Undo
>>> import sqlalchemy               # TODO delay
>>> import collections              # Undo

# 函数式编程
>>> import functools                # Done
>>> import itertools                # Done
>>> import operator                 # Done

>>> import fnmatch                  # Done
>>> import tablib                   # Undo
>>> import clint                    # Done
>>> import pathlib                  # TODO delay
>>> import tempfile                 # TODO delay
>>>
"""
import threading
import asyncio

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()