"""
栈

栈的操作:
    Stack()         创建一个新的空栈
    push(item)      添加一个新的元素item到栈顶
    pop()           弹出栈顶元素
    peek()          返回栈顶元素
    is_empty()      判断栈是否为空
    size()          返回栈的元素个数
"""

class Stack:
    """栈."""

    def __init__(self):
        self.__items = list()

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        return self.__items.pop()

    def peek(self):
        return self.__items[-1]

    @property
    def empty(self):
        return bool(self.__items)

    @property
    def size(self):
        return len(self.__items)

    @property
    def items(self):
        yield from self.__items


if __name__ == '__main__':
    stack = Stack()
    stack.push(100)
    stack.push(200)
    stack.push('d')
    print(list(stack.items))
    stack.pop()
    print(list(stack.items))
    print(stack.peek())
    print(stack.size)
