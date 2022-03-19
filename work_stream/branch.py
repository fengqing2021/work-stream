from work_stream.line import StreamLine


class StreamBranch:
    """
        流分支，用于判断用哪条流水线。
    """
    def __init__(self, expression, branch1: list[StreamLine, ...], branch2: list[StreamLine, ...]):
        """
        创建分支选择
        :param expression: 分支表达式
        :param branch1: 分支1
        :param branch2: 分支2
        """
        self.branch1 = branch1
        self.branch2 = branch2
        self.expression = expression

    def start(self, value) -> list[StreamLine, ...]:
        """
        分支选择
        :param value: 上一个函数的返回值
        :return: 分支
        """
        res = (self.branch1, self.branch2)[eval(self.expression)]
        return res
