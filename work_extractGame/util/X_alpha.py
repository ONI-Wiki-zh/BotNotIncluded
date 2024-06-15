import numpy as np
from scipy.integrate import quad, dblquad
from scipy.optimize import brentq


def f(x):
    # 取值范围自参考游戏反编译代码中Resample()函数。
    if x > -6 and x < 6:
        return np.exp(x) / (1 + np.exp(x))**2
    return 0


def create_dict(alpha, arr_multi, arr_div):
    if alpha.shape == arr_multi.shape == arr_div.shape:
        dict1 = {a: b for a, b in zip(alpha, arr_multi)}
        dict2 = {a: b for a, b in zip(alpha, arr_div)}
        return dict1, dict2
    else:
        raise ValueError("Input arrays must have the same shape.")


def get_percentile(minVal: float, maxVal: float, alpha=np.array([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])):
    def F_resample(x):
        return minVal+(f(x) + 6) / 12 * (maxVal - minVal)
    F_alpha_resample = np.array([F_resample(a) for a in alpha])
    if alpha.shape == F_alpha_resample.shape:
        return {a: b for a, b in zip(alpha, F_alpha_resample)}
    return None


def get_percentile_dbl(m1: float, m2: float, alpha=np.array([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])):
    # f1 is the probability density function of X
    f10, _ = quad(lambda a: f(12 / (m1 - 1) * (a - 1) - 6), 1, m1, limit=100)
    f1 = lambda a: f(12 / (m1 - 1) * (a - 1) - 6) / f10

    # f2 is the probability density function of Y
    f20, _ = quad(lambda a: f(12 / (m2 - 1) * (a - 1) - 6), 1, m2, limit=100)
    f2 = lambda a: f(12 / (m2 - 1) * (a - 1) - 6) / f20

    # X*Y cumulative distribution function: integrate the product of densities
    # over x from 1 to m1 and y from 1 to a/x
    F_mult = lambda a: dblquad(lambda s, t: f1(t) * f2(s), 1, m1, lambda s: 1, lambda s: a / s)[0]
    # X/Y cumulative distribution function: integrate the product of densities
    # over x from 1 to m1 and y from x/a to m2
    F_div = lambda a: dblquad(lambda s, t: f1(t) * f2(s), 1, m1, lambda s: s / a, lambda s: m2)[0]

    # Compute quantiles
    F_alpha_mult = np.array([brentq(lambda u: F_mult(u) - a, 1, m1 * m2) for a in alpha])
    F_alpha_div = np.array([brentq(lambda u: F_div(u) - a, 1/m2, m1) for a in alpha])

    return create_dict(alpha, F_alpha_mult, F_alpha_div)


if __name__ == '__main__':
    dict_resample = get_percentile(6000, 12000)
    print(dict_resample)
    dict_multi, dict_div = get_percentile_dbl(2, 9)
    print(dict_multi)
    print(dict_div)
