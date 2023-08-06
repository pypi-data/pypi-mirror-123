import numpy as np


class TailEstimator:
    @staticmethod
    def prepare(x):
        return np.sort(x)

    @staticmethod
    def get_k(x, boot=False):
        if boot:
            return (1, #np.sum(x >= np.quantile(x, 0.975)),
                    np.sum(x >= np.quantile(x, 0.5)))
        return np.arange(2, x.size-2)

    @staticmethod
    def estimate(x, k):
        return None

    @staticmethod
    def check(ex):
        return ex is not None

    @staticmethod
    def get_opt_k(x):
        return None
