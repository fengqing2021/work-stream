import sys
from work_stream.block import StreamBlock


class StreamLine:
    """
        流水线，用于编排块。
    """

    def __init__(self):
        """
            初始化创建一个流水线(列表）。
        """
        self.line = []  # 流水线
        self.count = 0  # block id
        self.current_num = 0
        self.__length = None
        self.ready = False

    @property
    def length(self):
        self.__length = len(self.line)
        return self.__length

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_num < len(self.line):
            ret = self.line[self.current_num]
            self.current_num += 1
            return ret
        else:
            raise StopIteration

    def add(self, func, args=(), kwargs=None, inherit=True):
        """
        向流水线中添加块。
        :param func: 加工方法
        :param args: *arg参数
        :param kwargs: **kwargs参数
        :param inherit: 是否继承，
        :return: None

        特别说明：参数inherit优先级大于args, kwargs即当inherit=Ture时，函数会传入上一个函数的返回值，此时指定的args,kwargs均无效。
        """
        if kwargs is None:
            kwargs = {}

        block = StreamBlock(func, inherit, args, kwargs)
        self.line.append(
            {
                'id': self.count,
                'status': block.status,
                'block': block
            }
        )
        self.count += 1

    def start(self, target=None):
        """
        开启流水线加工
        :param target: 原材料
        :return: 成品(数据)
        """
        value = self.line[0]['block'].start(target)
        if self.line[0]['status']['status'] == 'error':
            return 'Error'

        for stuff in self.line[1:]:
            value = stuff['block'].start(value)
            if stuff['status']['status'] == 'error':
                return 'Error'
        self.ready = True
        return value

    def __str__(self):
        return str(self.line)
