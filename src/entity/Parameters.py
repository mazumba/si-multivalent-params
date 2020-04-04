import numpy as np


class QcParameters:
    prefix = '/qc'

    def __init__(self, k: np.ndarray, n: float, delta_h: float, dirname: str):
        self.k = k
        self.n = n
        self.delta_h = delta_h
        self.dirname = dirname + self.prefix

    def print(self):
        print(f'Qc parameters:\nk: {self.k}, n: {self.n}, delta_h: {self.delta_h}')


class WisemanParameters:
    prefix = '/wiseman'

    def __init__(self, k: float, n: float, delta_h: float, dirname: str):
        self.k = k
        self.n = n
        self.delta_h = delta_h
        self.dirname = dirname + self.prefix

    def print(self):
        print(f'Wiseman parameters:\nk: {self.k}, n: {self.n}, delta_h: {self.delta_h}')
