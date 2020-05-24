

def binary_search(seq, item) -> bool:
    """二分法查找.

    递归方式实现
    """

    # 递归退出的条件
    if len(seq) == 0:
        return False

    n = len(seq)
    mid = n // 2

    if seq[mid] == item:
        return True
    elif seq[mid] > item:
        return binary_search(seq[:mid], item)
    else:
        return binary_search(seq[mid+1:], item)


if __name__ == '__main__':
    # 准备一个升序序列
    seq = [17, 20, 26, 31, 44, 54, 55, 77, 93]
    print(binary_search(seq, 55))
    print(binary_search(seq, 100))
