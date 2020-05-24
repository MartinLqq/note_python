"""
单向队列
操作:
    Queue() 创建一个空的队列
    enqueue(item) 往队列中添加一个item元素
    dequeue() 从队列头部删除一个元素
    empty 判断一个队列是否为空
    size 返回队列的大小
"""


class Queue:

    def __init__(self):
        self.__items = []
        self.__index = 0

    def enqueue(self, item):
        self.__items.insert(0, item)

    def dequeue(self):
        return self.__items.pop()

    @property
    def empty(self):
        return not bool(self.__items)

    @property
    def size(self):
        return len(self.__items)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index >= len(self.__items):
            raise StopIteration
        item = self.__items[self.__index]
        self.__index += 1
        return item


if __name__ == '__main__':
    q = Queue()
    q.enqueue(123)
    q.enqueue(456)
    q.enqueue(789)
    q.dequeue()
    print(list(q))
    print(q.size)
    print(q.empty)
