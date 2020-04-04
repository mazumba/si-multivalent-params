from __future__ import annotations

import numpy as np
import src.service.QService as QService
from src.Exceptions import NegativeValueError, NormValueTooLargeError
from src.entity.ExtractCollection import ExtractCollection
from src.entity.ResultCollection import QcResultCollection
from src.service.Wiseman import Wiseman
from scipy.optimize import minimize
from scipy.stats import norm


class Processor:
    def __init__(self, extract: ExtractCollection, gauss_pos: float):
        self.extract_collection = extract
        self.scale = np.abs(
            gauss_pos - np.max(self.extract_collection.molar_ratio) + np.min(self.extract_collection.molar_ratio)) / 4
        # self.gaussian = norm.pdf(self.extract_collection.molar_ratio, gauss_pos, self.scale)
        # OR
        self.gaussian = np.ones(len(self.extract_collection.molar_ratio))

    def calculate_norm(self, array_a: np.ndarray, array_b: np.ndarray) -> float:
        # self.gaussian = np.ones(len(self.extract_collection.molar_ratio))
        # return self.calculate_norm_omit(array_a, array_b)
        return np.linalg.norm(self.gaussian * (array_a - array_b))

    def calculate_norm_omit(self, array_a: np.ndarray, array_b: np.ndarray) -> float:
        return np.linalg.norm(self.gaussian[1:] * (array_a[1:] - array_b[1:]))

    def calculate_error(self, array_a: np.ndarray, array_b: np.ndarray) -> np.ndarray:
        return np.abs(self.gaussian * (array_a - array_b))

    def calculate_error_omit(self, array_a: np.ndarray, array_b: np.ndarray) -> np.ndarray:
        return np.abs(self.gaussian * (array_a - array_b))

    @staticmethod
    def calculate_lb(kd: np.ndarray, n: float, m_t: np.ndarray, l_t: np.ndarray, m_x_l: np.ndarray) -> np.ndarray:
        mlkd_sum = n * m_t + l_t + kd
        return 0.5 * (mlkd_sum - np.sqrt(mlkd_sum * mlkd_sum - 4 * n * m_x_l))

    @staticmethod
    def calculate_qtrans(k: np.ndarray, n: float, delta_h: float, m_t: np.ndarray, lt_mt: np.ndarray):
        tmp = lt_mt + 1 / (m_t * k)
        return 0.5 * (1 + (n - tmp) / np.sqrt((n + tmp) * (n + tmp) - 4 * n * lt_mt)) * delta_h


class QcProcessor(Processor):
    def __init__(self, extract: ExtractCollection, gauss_pos: float, matrix_key: str, result: QcResultCollection,
                 norm_to_beat: float):
        super().__init__(extract, gauss_pos)
        self.matrix_key = matrix_key
        self.extract_collection = extract
        self.result_collection = result
        self.norm_to_beat = norm_to_beat
        # self.norm_threshold = 10 * norm_to_beat / 3
        self.norm_threshold = 30

    def calculate_kds_new(self, k: np.ndarray, n: float):
        # Calculate the first kd, where [L] = (L_t)_1.
        m_t = self.extract_collection.m_t
        l_t = self.extract_collection.l_t
        m_x_l = self.extract_collection.lt_x_mt
        con = l_t[0]
        k_on, k_off = QService.calc_kon_and_koff(k, con, self.matrix_key)
        self.result_collection.set_kd(k_on, k_off, pos=0)
        for inj in range(1, len(l_t)):
            con = l_t[inj] - self.calculate_lb(self.result_collection.k_d[inj - 1], n, m_t[inj - 1], l_t[inj - 1],
                                               m_x_l[inj - 1])
            k_on, k_off = QService.calc_kon_and_koff(k, con, self.matrix_key)
            self.result_collection.set_kd(k_on, k_off, pos=inj)
        return self

    def optimize_n_and_deltah(self, n: float, delta_h: float, k: np.ndarray) -> float:
        self.calculate_kds_new(k, n)
        wiseman_graph = self.calculate_qtrans(self.result_collection.k_a, n, delta_h, self.extract_collection.m_t,
                                              self.extract_collection.molar_ratio)
        calc_norm = self.calculate_norm(self.extract_collection.heat_per_injection, wiseman_graph)
        if calc_norm > self.norm_threshold:
            raise NormValueTooLargeError
        f_min = minimize(self.__fitting_func__,
                         x0=np.array([n, delta_h]),
                         args=list([k]),
                         method='Nelder-Mead',
                         options={'disp': False, 'maxiter': 1e+3, 'maxfev': 1e+4, 'return_all': True, 'adaptive': True}
                         )
        if not f_min.success:
            print('Optimizing of delta_h failed.')
            print(f'         Current function value: {f_min["fun"]}')
            print(f'         Iterations: {f_min["nit"]}')
            print(f'         Function evaluations: {f_min["nfev"]}')
        if calc_norm <= self.norm_to_beat:
            print(f'Initial norm: {calc_norm} | Resulting norm: {f_min["fun"]}')
        return f_min.x

    def __fitting_func__(self, x0: np.ndarray, args: list):
        n = x0[0]
        delta_h = x0[1]
        k = args[0]
        self.calculate_kds_new(k, n)
        wiseman_graph = self.calculate_qtrans(self.result_collection.k_a, n, delta_h, self.extract_collection.m_t,
                                              self.extract_collection.molar_ratio)
        heat_graph = self.extract_collection.heat_per_injection
        return self.calculate_norm(heat_graph, wiseman_graph)

    def calculate_kds(self, k: np.ndarray, optimal_kas: np.ndarray, n: float) -> QcProcessor:
        m_t = self.extract_collection.m_t
        l_t = self.extract_collection.l_t
        m_x_l = self.extract_collection.lt_x_mt
        con = l_t - self.calculate_lb(1 / optimal_kas, n, m_t, l_t, m_x_l)
        # if np.min(con) < 0:
        #     raise NegativeValueError('Concentration value has to be positive.')
        for inj in range(0, len(l_t)):
            k_on, k_off = QService.calc_kon_and_koff(k, con[inj], self.matrix_key)
            self.result_collection.set_kd(k_on, k_off, inj)
        return self

    def get_result(self):
        return self.result_collection


class WisemanProcessor(Processor):
    def __init__(self, extract: ExtractCollection, gauss_pos: float, wiseman: Wiseman):
        super().__init__(extract, gauss_pos)
        self.wiseman = wiseman

    def fit_to_heat_per_inj(self):
        f_min = minimize(self.__fitting_func__,
                         x0=self.__get_x0__(),
                         args=self.__get_args__(),
                         method='Nelder-Mead',
                         options={'disp': True, 'maxfev': 1e+6, 'maxiter': 1e+6, 'return_all': True, 'adaptive': True}
                         )
        if not f_min.success:
            print('         Current function value: ' + str(f_min['fun']))
            print('         Iterations: ' + str(f_min['nit']))
            print('         Function evaluations: ' + str(f_min['nfev']))
        self.wiseman.update_data(f_min.x[0], f_min.x[1], f_min.x[2])

    def __fitting_func__(self, x0: np.ndarray, args: list):
        k = x0[0]
        n = x0[1]
        delta_h = x0[2]
        m_t = args[0]
        lt_mt = args[1]
        wiseman_graph = self.calculate_qtrans(k, n, delta_h, m_t, lt_mt)
        heat_graph = args[2]
        return self.calculate_norm(heat_graph, wiseman_graph)

    def __get_x0__(self) -> np.ndarray:
        return np.array([self.wiseman.k, self.wiseman.n, self.wiseman.delta_h])

    def __get_args__(self) -> list:
        return list([self.wiseman.m_t, self.wiseman.molar_ratio, self.wiseman.heat_per_inj])
