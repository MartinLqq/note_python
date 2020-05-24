"""
单链表的实现.
单链表的操作:
    empty               链表是否为空
    length              链表长度
    travel()            遍历整个链表
    add(item)           链表头部添加元素
    append(item)        链表尾部添加元素
    insert(pos, item)   指定位置添加元素
    remove(item)        删除节点
    find(item)          查找节点
"""


class SingleNode:
    """单链表的一个节点."""

    def __init__(self, item):
        self.item = item  # item: 存放节点的数据
        self.next = None  # next: 存放下一个节点的位置（python中的标识）


class SingleLinkList:
    """单链表."""

    def __init__(self):
        self._head = None  # _head: 存放头节点

    @property
    def empty(self):
        return self._head is None

    @property
    def length(self):
        if self.empty:
            return 0

        leng = 1
        cur = self._head
        while cur.next:
            leng += 1
            cur = cur.next
        return leng

    def add(self, item):
        # 1.创建一个节点
        node = SingleNode(item)

        if self.empty:
            self._head = node
            return

        # 2.将单链表的头节点保存到新创建节点的 next 属性中
        node.next = self._head
        # 3.将单链表的头节点更新为新创建的节点
        self._head = node

    def append(self, item):
        node = SingleNode(item)
        if self.empty:
            self._head = node
            return

        cur = self._head
        while cur.next:
            cur = cur.next

        cur.next = node

    def insert(self, pos: int, item):
        if pos <= 0:
            self.add(item)
        elif pos >= self.length:
            self.append(item)
        else:
            cur_pos = 0
            pre = None
            cur = self._head
            while cur_pos < pos:
                cur_pos += 1
                pre = cur
                cur = cur.next
            node = SingleNode(item)
            pre.next = node
            node.next = cur

    def remove(self, item):
        pre = None
        cur = self._head
        while cur is not None:
            if cur.item == item:
                # 如果第一个就是要删除的节点
                if not pre:
                    self._head = cur.next
                else:
                    pre.next = cur.next
                # 找到即退出循环
                break
            else:
                # 没找到, 继续下一个节点
                pre = cur
                cur = cur.next
        else:
            # 查找完成, 仍没有找到
            raise ValueError('Not exists')

    def travel(self):
        cur = self._head
        while cur:
            yield cur.item
            cur = cur.next

    def find(self, item):
        pos = -1
        cur = self._head
        while cur:
            pos += 1
            if cur.item == item:
                return pos
            cur = cur.next
        return -1


if __name__ == '__main__':
    # 创建一个单链表
    sll = SingleLinkList()

    sll.add([1,2,3])
    sll.append(100)
    sll.append(100)
    sll.insert(-3, 500)
    sll.remove(100)
    print(sll.length)
    print(list(sll.travel()))

    sll.append('a')
    sll.append('b')
    sll.append('c')
    print(list(sll.travel()))
    print(sll.find(500))
