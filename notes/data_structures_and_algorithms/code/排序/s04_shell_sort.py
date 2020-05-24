

def shell_sort(seq):
    """希尔排序. (缩小增量排序)"""
    n = len(seq)
    gap = n // 2  # 初始步长
    while gap >= 1:
        for j in range(gap, n):  # 按步长进行插入排序
            i = j
            # 插入排序
            while i-gap>=0 and seq[i-gap] > seq[i]:
                seq[i-gap], seq[i] = seq[i], seq[i-gap]
                i -= gap
        # 得到新的步长
        gap //= 2


if __name__ == '__main__':
    seq = [3, 1, 5, 6, 4, 2]
    shell_sort(seq)
    print(seq)
