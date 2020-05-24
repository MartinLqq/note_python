"""
双端队列  (可参考 collections.dequeue)

操作:
    Deque() 创建一个空的双端队列
    add_front(item) 从队头加入一个item元素
    add_rear(item) 从队尾加入一个item元素
    remove_front() 从队头删除一个item元素
    remove_rear() 从队尾删除一个item元素
    empty 判断双端队列是否为空
    size 返回队列的大小
"""

class Deque(object):
    """双端队列"""
    def __init__(self):
        self.items = []

    @property
    def empty(self):
        """判断队列是否为空"""
        return not bool(self.items)

    def add_front(self, item):
        """在队头添加元素"""
        self.items.insert(0,item)

    def add_rear(self, item):
        """在队尾添加元素"""
        self.items.append(item)

    def remove_front(self):
        """从队头删除元素"""
        return self.items.pop(0)

    def remove_rear(self):
        """从队尾删除元素"""
        return self.items.pop()

    @property
    def size(self):
        """返回队列大小"""
        return len(self.items)
