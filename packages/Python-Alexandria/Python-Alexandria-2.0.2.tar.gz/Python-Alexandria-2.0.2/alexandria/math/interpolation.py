# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Interpolation methods
---------------------
"""


import numpy as np


def polyfit(x, y, z, kx=3, ky=3):
    """
    Polyfit-function, adapted from answers provided by
    https://stackoverflow.com/questions/33964913/equivalent-of-polyfit-for-a-2d-polynomial-in-python

    :param x:  Domain 1.
    :param y:  Domain 2.
    :param z:  Function.
    :param kx: Polynomial order in x.
    :param ky: Polynomial order in y.

    :type x:   np.ndarray
    :type y:   np.ndarray
    :type z:   np.ndarray
    :type kx:  float
    :type ky:  float

    :return:
    """

    def transform_x(_x):
        return -1 + 2 * (_x - xmin)/(xmax - xmin)

    def transform_y(_y):
        return -1 + 2 * (_y - ymin)/(ymax - ymin)

    xmax = np.amax(x)
    xmin = np.amin(x)
    ymax = np.amax(y)
    ymin = np.amin(y)

    x = transform_x(x)
    y = transform_y(y)

    xx, yy = np.meshgrid(x,y,copy=False)

    coef = np.ones((kx+1,ky+1))

    A = np.zeros((coef.size,xx.size))

    for index, (i, j) in enumerate(np.ndindex(coef.shape)):
        arr = coef[i,j] * xx**i * yy**j
        A[index] = arr.ravel()

    coef, r, rank, s = np.linalg.lstsq(A.T,np.ravel(z),rcond=None)

    res = lambda x,y: np.polynomial.polynomial.polyval2d(transform_x(x),
                                                         transform_y(y),
                                                         coef.reshape((kx+1,
                                                                       ky+1)))

    return res, r
