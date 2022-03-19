# 快速开始

首先你需要自定义一个方法,例如：

    >>> def add(n):
    ...     return n + n
    ...

接下来导入`StreamLine`。你可以把它当成一条流水线/一个流程/一个动作，下文均以流水线为例。

    >>> from work_stream import StreamLine
    >>>
    >>> line = StreamLine()
    >>> line
    <work_stream.line.StreamLine object at 0x000001BF1C5DA680>
    >>>

`StreamLine`是一个可迭代的对象，可以通过调用其`length`和`ready`属性来查看流水线长度和是否完成的状态。

    >>> line.length
    0
    >>> line.ready
    False
    >>>

<br>

现在我们把最开始定义好的`add`方法添加到流水线中,并调用`line`属性查看其流水线当前的状态/属性/值。`param`字段值为`''`，是因为流水线还未执行。

    >>> line.add(add)
    >>>
    >>> line.line
    [{'id': 0, 'status': {'status': '', 'result': '', 'cost': '', 'mode': True, 'param': ''}, 'block': <work_stream.block.StreamBlock object at 0x000001BF1C5DACE0>}]
    >>>

如上所示，`add`方法被添加到`line`对象中之后变成了`block`对象。`block`重新封装了`add`是为了能够管理`add`的执行生命周期的状态以便于维护，其字段含义顾名思义。

<br>

当然，`add`还还能接收自定义参数。

```
>>> line.add(add, args=(1,))
>>> line.add(add, kwargs={'n': 123})

```

如果你有很多个方法需要`add`，可以使用`append`方法提交：

```
>>> line.append(
...     [
...         (add, False, (1,)),
...         (add, False, (), {'n': 1}),
...         {'func': add, 'mode': False, 'kwargs': {'n': 1}}
...     ]
... )
```

<br>

**特别说明：**

`add`的方法自带`inherit=True`参数，该参数决定**是否使用上一参数的返回值**。当流水线中**第一个**方法执行时，默认接收`start`方法中的`target`参数。

`inherit`参数与自定义参数(`args`,`kwargs`)是**互斥**的，但是两者都写也不会报错**，在`StreamLine`的内部，**自定义参数的优先级比`inherit`更高**。

<br>

一切准备就绪，通过调用`line.start()`执行流水线。

```
>>> from work_stream import StreamLine
>>>
>>>
>>> def add(n):
...     return n + n
...
>>>
>>> if __name__ == '__main__':
...     line = StreamLine()
...     line.add(add)
...     line.add(add)
...     res = line.start(12)
...     print(line.line)
...     print(res)
...
[{'id': 0, 'status': {'status': 'completed', 'result': 24, 'cost': '0.004399975296109915ms', 'mode': True}, 'block': <work_stream.block.StreamBlock object at 0x000001BF1C647970>}, {'id': 1, 'status': {'status': 'completed', 'result': 48, 'cost': '0.000700005330145359ms', 'mode': True}, 'block': <work_stream.block.StreamBlock object at 0x000001BF1C6468F0>}]
48
```

最终得到了一个`12+12+24+24`的结果。

<br>
更进一步的玩法：关于如何编排多个流水线。请在进阶中查看。
