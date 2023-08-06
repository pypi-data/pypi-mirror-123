import numpy as np
#import numba as nb

from dtg.tail.estimate.estimator import TailEstimator


class DeVriesEstimator(TailEstimator):
    @staticmethod
    #@nb.njit(fastmath=True)
    def estimate(x, k):
        try:
            mn = np.mean(np.log(x[-k-1:])**2) - np.log(x[-k-2]**2)
            hl = np.mean(np.log(x[-k - 1:])) - np.log(x[-k - 2])
            if hl == 0:
                return 0
            return (mn/(2*hl))
        except:
            return 0
