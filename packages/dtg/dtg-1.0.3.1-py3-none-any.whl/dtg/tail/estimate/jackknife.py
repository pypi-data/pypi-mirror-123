import numpy as np
#import numba as nb

from dtg.tail.estimate.estimator import TailEstimator


class JackknifeEstimator(TailEstimator):
    @staticmethod
    #@nb.njit(fastmath=True)
    def estimate(x, k):
        try:
            mn = np.mean(np.log(x[-k-1:])**2) - np.log(x[-k-2]**2)
            hl = np.mean(np.log(x[-k - 1:])) - np.log(x[-k - 2])
            return (mn/hl) - hl
        except:
            return np.infty
