import numpy as np
from src.entity.ExtractCollection import ExtractCollection
from typing import Union


class Wiseman:
    def __init__(self, extract: ExtractCollection, k: Union[float, np.ndarray], n: float, delta_h: float):
        self.k = k
        self.delta_h = delta_h
        self.n = n
        self.l_t = extract.l_t
        self.m_t = extract.m_t
        self.molar_ratio = extract.molar_ratio
        self.heat_per_inj = extract.heat_per_injection

    def update_data(self, k: Union[float, np.ndarray], n: float, delta_h: float):
        self.k = k
        self.delta_h = delta_h
        self.n = n

    def get_graph(self) -> np.ndarray:
        lt_mt = self.molar_ratio
        tmp = lt_mt + 1 / (self.m_t * self.k)
        return 0.5 * (1 + (self.n - tmp) / np.sqrt(np.power(self.n + tmp, 2) - 4 * self.n * lt_mt)) * self.delta_h
