from src.service.initializer.AbstractInitialize import AbstractInitialize
from src.entity.Parameters import QcParameters, WisemanParameters


class Initialize(AbstractInitialize):
    @staticmethod
    def init_wiseman_man1355llbb25(dirname: str) -> WisemanParameters:
        k_ini = 2000
        n_ini = 0.3
        deltah_ini = -80
        return WisemanParameters(k_ini, n_ini, deltah_ini, dirname)

    @staticmethod
    def init_qc_man1355llbb25(dirname: str) -> QcParameters:
        k_ini = AbstractInitialize.__new_random_k__(6, 1000)
        n_ini = AbstractInitialize.__new_random_single__(0.3, 0.5)
        deltah_ini = AbstractInitialize.__new_random_single__(-120, 0.4)
        return QcParameters(k_ini, n_ini, deltah_ini, dirname)

    @staticmethod
    def init_wiseman_man1010lacetate2(dirname: str) -> WisemanParameters:
        k_ini = 1000
        n_ini = 0.2
        deltah_ini = -120
        return WisemanParameters(k_ini, n_ini, deltah_ini, dirname)

    @staticmethod
    def init_qc_man1010lacetate2(dirname: str) -> QcParameters:
        k_ini = AbstractInitialize.__new_random_k__(4, 100)
        n_ini = AbstractInitialize.__new_random_single__(0.2, 0.5)
        deltah_ini = AbstractInitialize.__new_random_single__(-120, 0.4)
        return QcParameters(k_ini, n_ini, deltah_ini, dirname)
