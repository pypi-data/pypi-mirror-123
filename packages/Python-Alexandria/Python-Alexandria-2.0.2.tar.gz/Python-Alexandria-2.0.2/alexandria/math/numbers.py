# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Number utilities
----------------
"""


import numpy as np
from math import ceil


def get_representative_decimals(n, precision=1/100):
    """
    :param n: Number
    :param precision: Fractional precision required. Default: 1%
    :return: Required decimals to represent _n_ with the required
             fractional precision.
    """
    d = -np.log10(abs(n)*precision)
    return ceil(d) if d > 0 else 0


def min_multiple_under(x, base):
    """
    Returns the minimum multiple of the base
    that is larger than x.

    :param x: Maximum value
    :param base: Base
    :return: Minimum multiple of Base larger than x
    """
    return base*ceil(x/base)
