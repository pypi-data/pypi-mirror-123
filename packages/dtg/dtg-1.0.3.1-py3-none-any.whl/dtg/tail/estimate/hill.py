import numpy as np

from dtg.tail.estimate.estimator import TailEstimator
from dtg.tail.estimate.jackknife import JackknifeEstimator
from dtg.tail.estimate.vries import DeVriesEstimator


class HillEstimator(TailEstimator):
    @staticmethod
    # @nb.njit(fastmath=True)
    def estimate(x, k):
        try:
            return np.mean(np.log(x[-k - 1:])) - np.log(x[-k - 2])
        except:
            return 0

    @staticmethod
    def check(ex):
        if np.sum(np.isnan(ex)) + np.sum(np.isinf(ex)) > 0:
            return False
        if ex <= 0:
            return False
        return True

    @staticmethod
    def AMSEE(x, tau=None, back=True, qt=0.01, bt=(10000, 0.95)):
        if x.size < 10:
            return -1, (-1, -1)
        ks, smpl = np.arange(0, x.size - 1), []

        if tau is None:
            ro = -1
        else:
            ro = -1  # todo
        alls = [HillEstimator.estimate(x, k) for k in ks]
        bi = {str(k + 1) + "-" + str(K + 1): np.mean(alls[k: K + 1]) - np.mean(alls[:K + 1]) for K in ks for k in
              np.arange(K + 1)}
        des = [DeVriesEstimator.estimate(x, k) for k in ks]

        ads = [np.mean([(des[k] - alls[k] + (bi[str(k + 1) + "-" + str(K + 1)] / dls((k + 1) / (K + 1), ro))) ** 2
                        for k in np.arange(K + 1)]) for K in ks]
        K = ks[2 + np.argmin([np.sum(
            [np.abs(((ads[K] - ads[K + i]) / i)) for i in [-2, -1, 1, 2]]) for K in np.arange(2, len(ads) - 2)]
        )]

        for i in ks[1:]:
            if ks[i] > K:
                break

            smpl.append((JackknifeEstimator.estimate(x, ks[i]) ** 2 / ks[i]) +
                        (
                                (1 - ro) * ((((K + 1) / (ks[i] + 1)) - 1) / ((((ks[i] + 1) / (K + 1)) ** ro) - 1)) * bi[
                            str(ks[i] + 1)

                            + "-" + str(K + 1)]) ** 2)
        smpl = np.array(smpl[:len(smpl) - 1])
        alls = np.array(alls)
        mn = np.nanargmin(smpl)



        if back:
            alls = 1 / alls
            alls[np.isnan(alls)] = 0

        tst = (alls[1 + mn] - np.sqrt(smpl[mn]), alls[1 + mn] + np.sqrt(smpl[mn]))
        return alls[1 + mn], tst, (
            np.quantile(alls, qt), np.quantile(alls, 1 - qt))


def dls(x, ro):
    if x == 1:
        return 1

    return - (x ** ro - 1) / (ro * (x ** (-1) - 1))
