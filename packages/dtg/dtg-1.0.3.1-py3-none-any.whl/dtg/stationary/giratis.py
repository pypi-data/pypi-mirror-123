import numpy as np
#import numba as nb


#@nb.njit(fastmath=True)
def stat(data, q=None):
    ns = data.size
    mn = np.mean(data)

    if q is None:
        q = int(np.sqrt(ns))
    if q < 1 or ns < 10:
        return 0

    dels = data - mn
    s = np.array([np.sum(dels[: i + 1]) for i in np.arange(dels.size)])
    gamma = [np.sum(np.multiply(dels[: ns - j], dels[j:])) / ns for j in np.arange(q)]

    v = (np.sum(s ** 2) - (np.sum(s) ** 2 / ns)) / (ns ** 2)
    s = np.array([gamma[i - j] for i in np.arange(q) for j in np.arange(q) if i - j >= 0])
    s = np.sum(s)/q

    if s == 0:
        return 0
    return v / s


def undir_stat(data, q=None, mins=True, subs=100):
    ns = data.size
    mn = np.mean(data)

    if q is None:
        q = int(np.sqrt(ns))

    if q == ns:
        return (1, 1, 1)

    dels = data - mn
    res = []
    for _ in np.arange(subs):
        np.random.shuffle(dels)

        res.append(stat(dels, q))
    if mins:
        return np.quantile(res, 0.5)
    else:
        return (np.min(res), np.mean(res), np.quantile(res, 0.5), np.max(res))
