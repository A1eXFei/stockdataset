# -*- coding: UTF-8 -*-


class NoDataReceiveException(RuntimeError):
    def __init__(self, arg):
        self.args = arg


class DataOccurFQException(RuntimeError):
    def __init__(self, arg):
        self.args = arg