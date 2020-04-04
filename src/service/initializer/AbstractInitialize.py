import numpy as np


class AbstractInitialize:
    @staticmethod
    def __new_random_k__(size: int, multi: float) -> np.ndarray:
        new_k = -1 * np.log(np.random.rand(size)) * multi
        return new_k

    @staticmethod
    def __new_random_single__(center: float, random_range: float = 0.2) -> float:
        new_n = center * (1 - random_range / 2) + np.random.rand(1) * center * random_range
        return float(new_n)
