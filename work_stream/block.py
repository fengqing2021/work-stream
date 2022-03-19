import time


class StreamBlock:
    """
        块, 用于对一个未知的函数/方法座一层封装，以便于维护、管理改函数/方法的状态
    """
    def __init__(self, func, mode=True, args=(), kwargs=None):
        """
        初始化
        :param func: 自定义方法
        :param mode: 是否继承上一个方法的返回值
        :param args: args
        :param kwargs: kwargs
        """
        if kwargs is None:
            kwargs = {}

        self.func = func
        self.mode = mode
        self.status = {'status': '', 'result': '', 'cost': '', 'mode': self.mode, 'param': ''}
        self.args = args
        self.kwargs = kwargs
        if args or kwargs:
            self.mode = False

    def start(self, target=None):
        """
        执行内部方法
        :param target:
        :return: Any
        """
        start_time = time.perf_counter()
        self.status['status'] = 'running'
        try:
            if self.mode:
                value = self.func(target)
                self.status['param'] = str(target)
            else:
                value = self.func(*self.args, **self.kwargs)
                self.status['param'] = str(f'args:{str(self.args)}, kwargs:{str(self.kwargs)}')

            self.status['cost'] = '%sms' % ((time.perf_counter() - start_time) * 1000)
            self.status['result'] = value
            self.status['status'] = 'completed'
            return value
        except Exception as e:
            self.status['status'] = 'error'
            self.status['result'] = str(e)
        return None
