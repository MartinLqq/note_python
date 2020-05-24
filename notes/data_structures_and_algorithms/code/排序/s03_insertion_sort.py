

def insertion_sort(seq):
    """插入排序.

    升序: 将整个序列看成两个子序列, 一个有序, 一个无序，
          对于未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入
    """
    n = len(seq)

    for j in range(1, n):
        # i = [j, j-1, j-2, , ... 1]
        for i in range(j, 0, -1):
            if seq[i] < seq[i-1]:
                seq[i], seq[i-1] = seq[i-1], seq[i]
            else:
                break


if __name__ == '__main__':
    seq = [3, 1, 5, 6, 4, 2]
    insertion_sort(seq)
    print(seq)
