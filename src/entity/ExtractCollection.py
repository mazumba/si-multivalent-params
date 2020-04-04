import numpy as np


class ExtractCollection:
    def __init__(self, l_t: np.ndarray, m_t: np.ndarray, heat_per_injection: np.ndarray, time: np.ndarray,
                 itc: np.ndarray):
        self.l_t = l_t
        self.m_t = m_t
        self.molar_ratio = self.l_t / self.m_t
        self.lt_x_mt = self.l_t * self.m_t
        self.heat_per_injection = heat_per_injection
        self.time = time
        self.itc = itc
