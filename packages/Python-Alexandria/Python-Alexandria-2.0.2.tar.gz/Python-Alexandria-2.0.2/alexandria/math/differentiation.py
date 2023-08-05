# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Numerical differentiation methods
---------------------------------
"""


import numpy as np
from scipy.interpolate import UnivariateSpline

from alexandria.math.algorithms import largest_prime_factor

from alexandria.data_structs.array import find_nearest_entry


def derivative(x, y):
    """
    Obtain derivative of function over its domain by interpolating
    the function using _scipy.interpolate.UnivariateSpline_ and
    taking the derivative of the interpolant (UnivariateSpline object)
    using its _derivative_ method.

    :param x: Domain.
    :param y: Function.

    :type x:  np.ndarray
    :type y:  np.ndarray

    :return: [np.ndarray] Derivative of y over x.
    """
    n = largest_prime_factor(len(x))
    _x = x[0::n]
    _y = y[0::n]
    return UnivariateSpline(_x, _y).derivative()(x)


def forward_euler(x, y, x0):
    """
    Forward Euler derivation scheme.

    :param x:  Domain.
    :param y:  Function.
    :param x0: Value in x at which to obtain derivative.

    :type x:   np.ndarray
    :type y:   np.ndarray
    :type x0:  float

    :return:   [float] Derivative of y at x0
    """
    point = lambda u, w=0: u[find_nearest_entry(x, x0)]
    return (point(y, 1) - point(y))/(point(x, 1) - point(x))
