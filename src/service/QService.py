import numpy as np
from src.Exceptions import QMatrixNotFoundError, ComplexError
import src.service.ClusterByIsa as Cluster

const_trival_jacek = 'trival_jacek'
const_monval = 'monval'
const_bval = 'bval'
const_trival = 'trival'


def get_matrix_key(dirname: str) -> str:
    if 'tri_tetra' == dirname:
        return const_trival
    if 'deca_bi' == dirname:
        return const_bval


# Factory to determine which binding matrix q should be used.
#
# @param np.array k   - the given k_ons and k_offs in that order.
# @param float    con - the given receptor concentration.
def get_q_matrix(k, con: float, matrix_key: str):
    if matrix_key is const_trival_jacek:
        return __q_trival_jacek_large(k, con)
    if matrix_key is const_monval:
        return __q_monval(k, con)
    if matrix_key is const_bval:
        return __q_bval(k, con)
    if matrix_key is const_trival:
        return __q_trival(k, con)
    raise QMatrixNotFoundError('Q-Matrix not found.')


# Returns q for monovalent bindings.
#
# @param np.array k   - the given k_ons and k_offs in that order.
# @param float    con - the given receptor concentration.
def __q_monval(k: np.array, con: float):
    q = np.array([[-k[0] * con, k[1]],
                  [k[0] * con, -k[1]]])
    return q  # .astype(float)


# Returns q for bivalent bindings.
#
# @param np.array k   - the given k_ons and k_offs in that order.
# @param float    con - the given receptor concentration.
def __q_bval(k: np.array, con: float):
    q = np.array([[-4 * k[0] * con, k[1], k[1], k[1], k[1], 0, 0],
                  [k[0] * con, -k[1] - k[2], 0, 0, 0, k[3], 0],
                  [k[0] * con, 0, -k[1] - k[2], 0, 0, 0, k[3]],
                  [k[0] * con, 0, 0, -k[1] - k[2], 0, k[3], 0],
                  [k[0] * con, 0, 0, 0, -k[1] - k[2], 0, k[3]],
                  [0, k[2], 0, k[2], 0, -2 * k[3], 0],
                  [0, 0, k[2], 0, k[2], 0, -2 * k[3]]])
    return q.astype(float)


def __q_trival(k: np.array, con: float):
    q = np.array(
        [[-9 * k[0] * con, k[1], k[1], k[1], k[1], k[1], k[1], k[1], k[1], k[1], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [k[0] * con, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, 0, 0, 0, k[3], 0, 0, 0, k[3], 0, 0, 0, 0, 0, 0, 0],
         [k[0] * con, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, 0, 0, 0, 0, k[3], k[3], 0, 0, 0, 0, 0, 0, 0, 0],
         [k[0] * con, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, 0, 0, k[3], 0, 0, 0, k[3], 0, 0, 0, 0, 0, 0],
         [k[0] * con, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, 0, k[3], 0, 0, 0, 0, k[3], 0, 0, 0, 0, 0],
         [k[0] * con, 0, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, k[3], 0, 0, 0, 0, 0, 0, 0, k[3], 0, 0, 0],
         [k[0] * con, 0, 0, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, k[3], 0, 0, 0, 0, k[3], 0, 0, 0, 0],
         [k[0] * con, 0, 0, 0, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, k[3], 0, 0, 0, k[3], 0, 0, 0, 0],
         [k[0] * con, 0, 0, 0, 0, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, k[3], 0, 0, 0, k[3], 0, 0, 0],
         [k[0] * con, 0, 0, 0, 0, 0, 0, 0, 0, -k[1] - 2 * k[2], 0, 0, 0, 0, 0, k[3], k[3], 0, 0, 0, 0, 0],
         [0, k[2], 0, 0, 0, k[2], 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, 0, 0, 0, 0, k[5], 0, 0],
         [0, 0, 0, k[2], k[2], 0, 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, 0, 0, 0, 0, 0, k[5]],
         [0, 0, k[2], 0, 0, 0, k[2], 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, 0, 0, 0, k[5], 0],
         [0, 0, k[2], 0, 0, 0, 0, k[2], 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, 0, 0, k[5], 0],
         [0, k[2], 0, 0, 0, 0, 0, 0, 0, k[2], 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, k[5], 0, 0],
         [0, 0, 0, k[2], 0, 0, 0, 0, k[2], 0, 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, 0, k[5]],
         [0, 0, 0, 0, k[2], 0, 0, 0, k[2], 0, 0, 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, 0, 0, 0, k[5]],
         [0, 0, 0, 0, 0, k[2], 0, 0, 0, k[2], 0, 0, 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, k[5], 0, 0],
         [0, 0, 0, 0, 0, 0, k[2], k[2], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -k[4] - 2 * k[3], 0, k[5], 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, k[4], 0, 0, 0, k[4], 0, 0, k[4], 0, -3 * k[5], 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, k[4], k[4], 0, 0, 0, 0, k[4], 0, -3 * k[5], 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, k[4], 0, 0, 0, k[4], k[4], 0, 0, 0, 0, -3 * k[5]]])
    return q.astype(float)


def __q_trival_jacek(k: np.array, con: float):
    q = np.array(
        [[-con * k[0], k[1], 0, 0],
         [con * k[0], -k[1] - con * k[2], k[3], 0],
         [0, con * k[2], -k[3] - con * k[4], k[5]],
         [0, 0, con * k[4], -k[5]]])
    return q.astype(float)


def __q_trival_jacek_large(k: np.array, con: float):
    q = np.array(
        [[-3 * con * k[0], k[1], k[1], k[1], 0, 0, 0, 0],
         [con * k[0], -k[1] - con * k[2], 0, 0, k[3], 0, 0, 0],
         [con * k[0], 0, -k[1] - con * k[2], 0, 0, k[3], 0, 0],
         [con * k[0], 0, 0, -k[1] - con * k[2], 0, 0, k[3], 0],
         [0, con * k[2], 0, 0, -k[3] - con * k[4], 0, 0, k[5]],
         [0, 0, con * k[2], 0, 0, -k[3] - con * k[4], 0, k[5]],
         [0, 0, 0, con * k[2], 0, 0, -k[3] - con * k[4], k[5]],
         [0, 0, 0, 0, con * k[4], con * k[4], con * k[4], -3 * k[5]]])
    return q.astype(float)


# Function to determine the macroscopic k_on and k_off from given microscopic k_ons and k_offs and
# the macromolecules concentration.
#
# Depends on matrix q that determines the possible binding states and the cluster algorithm by isa.
#
# @param np.array k   - the given k_ons and k_offs in that order.
# @param float    con - the given macromolecules concentration.
def calc_kon_and_koff(k: np.array, con: float, matrix_key: str) -> tuple:
    # k = [1, 1, 1, 1, 1, 1]
    q = get_q_matrix(k, con, matrix_key)
    e = np.linalg.eig(q)
    chi = Cluster.get_chi(q)  # [Chi, ~] = cluster_by_isa(Q,2);
    # zero_ind = np.nonzero(chi < 1e-15)
    # chi[zero_ind] = 0

    # ChiT = Chi.';
    # e = np.linalg.eig(q.T)  # e = eig(Q);
    eig_0_ind = np.argmin(np.abs(e[0]))
    pi = e[1][:, eig_0_ind]
    pi = pi / np.sum(pi)
    pi = np.eye(q.shape[1]) * pi  # Pi = eye(length(Q(:,1)))*e(1);

    # Qc = inv(ChiT * Pi * Chi) * (ChiT * Pi * Q.T * Chi)
    temp_l = chi.T @ pi @ chi
    temp_r = chi.T @ pi @ q.T @ chi
    q_c = np.linalg.inv(temp_l) @ temp_r
    q_c = q_c.T
    k_on = q_c[1, 0] / con  # k_on_new(t) = Qc(2,1)/con(t);
    k_off = q_c[0, 1]
    # if con > 1e-10 and (k_on < 0 or k_off < 0):
    #     raise NegativeValueError('k_on or k_off are below zero')
    if k_on.imag != 0 or k_off.imag != 0:
        raise ComplexError('k_on or k_off have an imaginary part')
    return k_on.real, k_off.real
