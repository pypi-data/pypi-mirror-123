import numpy as np

from scipy.special import erfinv


def estimate_t_p(val):
    return erfinv(2 * val - 1) * np.sqrt(2)


def estimate_ro_p(val):
    return erfinv(1 - val) * np.sqrt(2)


def boot(entity, x, alp, beta, num, k):
    ms = np.infty
    res1 = -1
    res2 = np.ones(num)

    for k_ in range(k[0], k[1]):
        real = entity.estimate(x, k_)
        if not entity.check(real):
            continue
        k1 = int((k_-1) / (x.size ** ((1 - beta) * alp)))+1
        n1 = int(x.size ** beta)

        ga = np.empty(num)
        count = 0
        count_0 = 0
        while count < num:
            if count_0 > 10*num and count == 0:
                break

            rsi = entity.estimate(np.sort(
                [x[i] for i in np.random.choice(x.size, n1, replace=True)]
            ), k1)
            if entity.check(rsi):
                ga[count] = rsi
                count += 1
            else:
                count_0 += 1

        bias = (np.mean(ga) - real) ** 2
        vr = np.var(ga)
        if ms > vr + bias:
            res1, res2 = real, ga
            ms = vr + bias

    return res1, res2


# alp = 2/3, beta = 1/2 for Hill's estimator
def boot_estimate(entity, x, alp, beta, num, pers=(0.95, 0.025), qt=0.05, back=True):
    if x.size < 2:
        return (
            -1,
            (0, 0),
            (0, 0)
        )

    k = entity.get_k(x, boot=True)
    x_ = entity.prepare(x)

    if k[1] - k[0] < 2:
        return (
            -1,
            (0, 0),
            (0, 0)
        )

    t_p = estimate_t_p(pers[0])
    ro_p = estimate_ro_p(pers[1])
    ro = ro_p * (1 + (t_p / np.sqrt(2 * num) + ((5 * (t_p ** 2) + 10) / (12 * num))))
    alp, dls = boot(entity, x_, alp, beta, num, k)

    if back:
        mn = np.mean(dls)
        ds = np.var(dls)
        try:
            return (
            1 / alp,
                (
                1/mn - ro * np.sqrt(ds / (mn**2)),
                1/mn + ro * np.sqrt(ds / (mn**2)),
                ),
                (
                np.quantile(1 / dls[dls > 0], qt),
                np.quantile(1 / dls[dls > 0], 1 - qt)
                )
            )
        except:
            return (
                1 / alp,
                (
                    1 / mn - ro * np.sqrt(ds / (mn ** 2)),
                    1 / mn + ro * np.sqrt(ds / (mn ** 2)),
                ),
                (
                    1/np.quantile(dls, 1-qt),
                    1/np.quantile(dls, qt)
                )
            )
    else:
        return (
            alp,
            (
                np.mean(dls) - ro * np.std(dls),
                np.mean(dls) + ro * np.std(dls),
            ),
            (
                np.quantile(dls, qt),
                np.quantile(dls, 1 - qt)
            )
        )
