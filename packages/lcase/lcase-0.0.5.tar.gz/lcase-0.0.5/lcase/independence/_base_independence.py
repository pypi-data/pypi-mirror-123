import copy
from abc import ABCMeta, abstractmethod


class _Base_Independence(metaclass=ABCMeta):
    def __init__(self, data):
        self.data = copy.deepcopy(data)

    @abstractmethod
    def compute_pvalue(self, x, y, condition_set):
        raise NotImplementedError

    @abstractmethod
    def compute_stats(self, x, y, condition_set):
        raise NotImplementedError
