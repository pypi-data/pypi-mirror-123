# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Special functions
-----------------
"""


def macauley(x, k):
    """
    Macauley step function for exponents > 0.

        macauley(t - 5)**n     for all n > 0

    :param x: Domain.
    :param k: Constant.

    :type x:  np.ndarray
    :type k:  float

    :return: [np.ndarray] Macauley step function array.
    """
    return x - k if x - k >= 0 else 0


def macauley0(x, k):
    """
    Macauley step function for exponent = 0.
    Necessary as 0**1 is defined as 1, while

        macauley(a-b)**0 = 0

    for all a, b such that b > a.

    :param x: Domain.
    :param k: Constant.

    :type x:  np.ndarray
    :type k:  float

    :return:  [np.ndarray] Macauley step function array.
    """
    return 1 if x - k >= 0 else 0
