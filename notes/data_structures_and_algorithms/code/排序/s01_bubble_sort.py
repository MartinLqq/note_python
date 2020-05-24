
def bubble_sort(seq):
    """冒泡排序.

    升序: 循环比较相邻两项, 大的放后面, 小的放前面
    """

    times = len(seq) - 1

    # 先了解怎么实现第一次排序
    # for i in range(times):
    #     if seq[i] > seq[i + 1]:
    #         seq[i], seq[i + 1] = seq[i + 1], seq[i]

    # 完整排序
    for j in range(times, 0, -1):
        # j => 每次排序需要比较的次数
        # j==times 时, 第一次排序

        # 优化点: 记录交换次数, 如果一次内部循环后交换次数仍为 0, 则直接完成排序
        count = 0

        for i in range(j):
            if seq[i] > seq[i+1]:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                count += 1

        if count == 0:
            break

if __name__ == '__main__':
    seq = [3, 1, 5, 6, 4, 2]
    bubble_sort(seq)
    print(seq)
