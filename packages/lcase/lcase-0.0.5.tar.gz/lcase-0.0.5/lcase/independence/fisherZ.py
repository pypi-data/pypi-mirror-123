import numpy as np

from . import _base_independence


class FisherZ(_base_independence):
    def __init__(self, data):
        super(FisherZ, self).__init__(data)
        self.corr = np