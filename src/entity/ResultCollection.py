import numpy as np


class QcResultCollection:
    def __init__(self, size: int):
        self.k_on = np.zeros(size)
        self.k_off = np.zeros(size)
        self.k_d = np.zeros(size)
        self.k_a = np.zeros(size)

    def set_kon(self, value: float, pos: int):
        self.k_on[pos] = value
        self.k_d[pos] = self.k_off[pos] / value
        return self

    def set_koff(self, value: float, pos: int):
        self.k_off[pos] = value
        self.k_a[pos] = self.k_on[pos] / value
        return self

    def set_kd(self, k_on: float, k_off: float, pos: int):
        self.k_d[pos] = k_off / k_on
        self.k_a[pos] = k_on / k_off
        self.k_on[pos] = k_on
        self.k_off[pos] = k_off
        return self

    def set_kds(self, k_ons: np.ndarray, k_offs: np.ndarray):
        self.k_d = k_offs / k_ons
        self.k_a = k_ons / k_offs
        self.k_on = k_ons
        self.k_off = k_offs

    def set_ka(self, k_on: float, k_off: float, pos: int):
        self.k_a[pos] = k_on / k_off
        self.k_d[pos] = k_off / k_on
        self.k_on[pos] = k_on
        self.k_off[pos] = k_off
        return self
