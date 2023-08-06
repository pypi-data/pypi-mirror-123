import numpy as np


def e(x, u):
    x = np.array(x)
    return np.sum(np.multiply(x - u, x > u)) / np.sum(x > u)


def e_s(x, u):
    return np.array([e(x, u_) for u_ in u])
