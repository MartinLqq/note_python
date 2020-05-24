class Node:
    """定义树的节点类."""

    def __init__(self, item):
        self.item = item
        self.lchild = None
        self.rchild = None


class BinaryTree:
    """二叉树的类."""

    def __init__(self, root: Node = None):
        self.root = root

    def add(self, item):
        """按照完全二叉树的结构去增加节点.

        广度优先遍历, 查找可以挂载的节点(左子节点为空则挂在左子节点, 右子节点为空则挂在右子节点),
        借助<队列>的先进先出数据结构, 实现广度优先遍历
        """
        node = Node(item)

        if not self.root:
            self.root = node
            return

        queue = list()
        queue.append(self.root)
        while queue:
            cur = queue.pop(0)
            if not cur.lchild:
                cur.lchild = node
                return
            else:
                queue.append(cur.lchild)
            if not cur.rchild:
                cur.rchild = node
                return
            else:
                queue.append(cur.rchild)

    def breadth_travel(self):
        """广度优先遍历 --- 借助队列
        """

        if not self.root:
            return

        queue = list()
        queue.append(self.root)
        while queue:
            cur = queue.pop(0)
            print(cur.item, end=" ")

            if cur.lchild:
                queue.append(cur.lchild)
            if cur.rchild:
                queue.append(cur.rchild)

    def pre_order(self, root: Node = None):
        """深度优先遍历 --- 借助递归

        先序遍历: 根->左->右
        """
        if root:
            print(root.item, end=" ")
            self.pre_order(root.lchild)
            self.pre_order(root.rchild)

    def in_order(self, root: Node = None):
        """深度优先遍历 --- 借助递归

        中序遍历: 左->根->右
        """
        if root:
            self.in_order(root.lchild)
            print(root.item, end=" ")
            self.in_order(root.rchild)

    def post_order(self, root: Node = None):
        """深度优先遍历 --- 借助递归

        后序遍历: 左->右->根
        """
        if root:
            self.in_order(root.lchild)
            self.in_order(root.rchild)
            print(root.item, end=" ")


if __name__ == '__main__':
    btree = BinaryTree()
    for i in range(10):
        btree.add(i)

    # 广度优先遍历
    # btree.breadth_travel()  # 0 1 2 3 4 5 6 7 8 9

    # 深度优先遍历之 先序遍历
    # btree.pre_order(btree.root)  # 0 1 3 7 8 4 9 2 5 6

    # 深度优先遍历之 中序遍历
    # btree.in_order(btree.root)   # 7 3 8 1 9 4 0 5 2 6

    # 深度优先遍历之 后序遍历
    btree.post_order(btree.root)   # 7 3 8 1 9 4 5 2 6 0
