from logging import Filter, LogRecord


class myFilter1(Filter):

    def __init__(self, name):
        # print('filter name: ', name)
        super().__init__(name)

    def filter(self, record: LogRecord):
        """
            返回 True 时, 此条日志过滤, 不会打印和保存
            返回 False 时, 不过滤, 会打印或保存
        """
        # 如果日志 message 中带有`test filter`, 则忽略此条日志
        if 'test filter' in record.getMessage():
            return False
        return True
