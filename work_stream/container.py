from work_stream.branch import StreamBranch
from work_stream.line import StreamLine
from copy import deepcopy


class StreamContainer:
    """
        流水线容器， 用于给多个流水线分组/打包/编排
    """

    def __init__(self):
        """
        初始化容器
        """
        self.container = {}
        self.count = 0

    def create(self, name='default'):
        """
        创建容器，初始化容器状态
        :param name: 容器名称
        :return: self
        """
        self.container[name] = {}
        self.container[name]['lines'] = {}
        self.container[name]['status'] = {}
        self.container[name]['line_group'] = []
        return self

    def layout(self, layout_line: StreamLine | StreamBranch | list[StreamLine | StreamBranch, ...],
               container_name: str = 'default'):
        """
        编排流水线
        :param layout_line: 流水线, 分支
        :param container_name: 容器名称
        :return: None
        """
        if isinstance(layout_line, list):
            for i in layout_line:
                if not isinstance(i, StreamBranch | StreamLine):
                    raise TypeError(f'该"{i}"参数不为StreamBranch类型或StreamLine类型, 请传入一个正确的参数')
            self.container[container_name]['line_group'] += layout_line
        elif isinstance(layout_line, StreamLine) or isinstance(layout_line, StreamBranch):
            self.container[container_name]['line_group'].append(layout_line)

    def start(self, target=None, container_name='default'):
        """
        启动容器
        :param target:
        :param container_name: 容器名
        :return: Any
        """
        group = self.container[container_name]['line_group']
        assert not isinstance(group[0], StreamBranch), '第一个节点不能为分支'
        self.container[container_name]['status'][self.count] = deepcopy(group[0].line)
        value = group[0].start(target)
        if value == 'Error':
            return None

        for g in range(len(group[1:])):
            if isinstance(group[g + 1], StreamLine):
                self.count += 1
                self.container[container_name]['status'][self.count] = deepcopy(group[g + 1].line)
                value = group[g + 1].start(value)
                if value == 'Error':
                    return None

            elif isinstance(group[g + 1], StreamBranch):
                lines = group[g + 1].start(value)
                for i in lines:
                    self.count += 1
                    self.container[container_name]['status'][self.count] = deepcopy(i.line)
                    value = i.start(value)
                    if value == 'Error':
                        return None
        return value
