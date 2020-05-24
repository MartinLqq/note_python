
def selection_sort(seq):
    """选择排序.

    升序:
        方法1: 在一个子序列中选择一个最大的, 放到后面
        方法2: 在一个子序列中选择一个最小的, 放到前面
    """
    times = len(seq) - 1

    # 先了解怎么实现第一次排序
    # max_index = 0
    # for i in range(times):
    #     if seq[max_index] < seq[i+1]:
    #         max_index = i + 1
    # seq[max_index], seq[-1] = seq[-1], seq[max_index]

    # 完整排序
    for j in range(times, 0, -1):
        max_index = 0
        for i in range(j):
            if seq[max_index] < seq[i + 1]:
                max_index = i + 1

        if max_index != j:
            seq[max_index], seq[j] = seq[j], seq[max_index]


if __name__ == '__main__':
    import random
    seq = [3, 1, 5, 6, 4, 2]
    random.shuffle(seq)

    print("排序前: ", seq)
    selection_sort(seq)
    print("排序后: ", seq)

    seq = []
    selection_sort(seq)
    print(seq)
