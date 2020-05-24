"""
双向链表的实现.
双向链表的操作:
    empty               链表是否为空 (继承自 SingleLinkList)
    length              链表长度 (继承自 SingleLinkList)
    travel()            遍历链表 (继承自 SingleLinkList)
    add(item)           链表头部添加
    append(item)        链表尾部添加
    insert(pos, item)   指定位置添加
    remove(item)        删除节点
    find(item)          查找节点 (继承自 SingleLinkList)
"""
from t02_single_link_list import SingleLinkList


class Node:
    """双向链表节点."""

    def __init__(self, item):
        self.item = item
        self.pre = None
        self.next = None


class DLinkList(SingleLinkList):
    """双向链表."""

    def add(self, item):
        node = Node(item)
        if self.empty:
            self._head = node
        else:
            node.next = self._head
            self._head.pre = node
            self._head = node

    def append(self, item):
        node = Node(item)
        if self.empty:
            self._head = node
            return

        cur = self._head
        while cur.next:
            cur = cur.next
        cur.next = node
        node.pre = cur

    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
        elif pos >= self.length:
            self.append(item)
        else:
            count = 0
            cur = self._head
            while count < pos:
                cur = cur.next
                count += 1

            node = Node(item)
            cur.pre.next = node
            node.next = cur
            node.pre = cur.pre
            cur.pre = node

    def remove(self, item):
        cur = self._head
        while cur:
            if cur.item == item:
                if cur == self._head:
                    # 删除的是头节点
                    self._head = cur.next
                    # 如果存在下一个节点, 就设置下一个节点的 pre 为 None
                    if cur.next:
                        cur.next.pre = None
                else:
                    # 删除的不是头节点
                    cur.pre.next = cur.next
                    if cur.next:
                        cur.next.pre = cur.pre
                # 找到即退出循环
                break
            else:
                cur = cur.next
        else:
            # 查找完成, 仍没有找到
            raise ValueError('Not exists')


if __name__ == '__main__':
    dll = DLinkList()

    dll.add('a')
    dll.add('b')
    dll.append('c')

    print(list(dll.travel()))

    dll.insert(2, 'd')

    # print(dll.length)
    # print(dll.find('c'))
    print(list(dll.travel()))

    dll.remove('d')
    print(list(dll.travel()))
