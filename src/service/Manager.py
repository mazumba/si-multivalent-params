from src.entity.Parameters import QcParameters, WisemanParameters
import numpy as np
import os

saves_dir = 'saves/'
k_file = 'k_ini'
n_file = 'n'
deltah_file = 'delta_h'


def load_q_c_ini(dirname: str) -> QcParameters:
    new_dirname = saves_dir + dirname + QcParameters.prefix + '/'
    k, n, delta_h = __load_saves__(new_dirname)
    return QcParameters(k, float(n), float(delta_h), dirname)


def save_q_c_params(params: QcParameters):
    __save_params__(params.k, np.array([params.n]), np.array([params.delta_h]), saves_dir + params.dirname + '/')


def load_wiseman_ini(dirname: str) -> WisemanParameters:
    new_dirname = saves_dir + dirname + WisemanParameters.prefix + '/'
    k, n, delta_h = __load_saves__(new_dirname)
    return WisemanParameters(float(k), float(n), float(delta_h), dirname)


def save_wiseman_params(params: WisemanParameters):
    __save_params__(np.array([params.k]), np.array([params.n]), np.array([params.delta_h]),
                    saves_dir + params.dirname + '/')


def __load_saves__(dirname: str) -> tuple:
    k = np.load(dirname + k_file)
    n = np.load(dirname + n_file)
    delta_h = np.load(dirname + deltah_file)
    # logging.info(f'loading from {dirname}: k={k}, n={n}, delta_h={delta_h}.')
    return k, n, delta_h


def __save_params__(k: np.ndarray, n: np.ndarray, delta_h: np.ndarray, dirname: str):
    os.makedirs(dirname, exist_ok=True)
    k.dump(dirname + k_file)
    n.dump(dirname + n_file)
    delta_h.dump(dirname + deltah_file)
    # logging.info(f'saving to {dirname}: k={k}, n={n}, delta_h={delta_h}.')
