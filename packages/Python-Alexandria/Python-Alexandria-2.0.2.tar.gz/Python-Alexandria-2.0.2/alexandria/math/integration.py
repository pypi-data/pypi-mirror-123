# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Numerical integration methods
-----------------------------
"""


import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d

from alexandria.data_structs.array import dx_v


class one_d:
    @classmethod
    def trapezoidal(cls, x, y):
        """
        Trapezoidal integration.

        :param x: Domain over which _f_ is integrated.
        :param y: Function to be integrated.

        :type x:  np.ndarray
        :type y:  np.ndarray

        :return:
        - [float] Integral value
        - [np.ndarray] Primitive of _f_
        """
        f_prime = np.zeros(len(y))
        dt_y = dx_v(x)
        for i in range(y.size - 1):
            f_prime[i] = dt_y[i] * (y[i] + (y[i + 1] - y[i]) / 2)
        np.append(f_prime, dt_y[-2] * (y[-1] + (y[-2] - y[-1]) / 2))
        return f_prime.sum(), f_prime


class two_d:
    @classmethod
    def Q_interp1d(cls, x1, x2, y, log=False):
        """
        2 step 2D integration:
        1. Interpolation and integration of the function along x2
        2. Interpolation and integration of the result over x1

        Methods:
        - Integration: _scipy.integrate.quad_
        - Interpolation: _scipy.interpolate.interp1D_

        :param x1:  Domain 1.
        :param x2:  Domain 2.
        :param y:   2D array to be integrated.
        :param log: Print maximum value of input array, average value
                    of integral over x2, and integrals over x1 and x2

        :param x1:  np.ndarray
        :param x2:  np.ndarray
        :param y:   np.ndarray

        :return:
        - [float]    Integral
        - [np.ndarray] Primitive over x1
        """

        # Integral about x_p axis
        int_z = np.empty(y.shape[1])

        for i in range(x1.size):
            spl_x2 = interp1d(x2, y[:, i])
            int_z[i] = quad(spl_x2, x2.min(), x2.max())[0]*1000

        # Integral about z_p axis
        spl_x1 = interp1d(x1, int_z)
        int_x1 = quad(spl_x1, x1[1], x1[-2])[0]

        if log:
            print(f"Maximum value of target distribution:    {y.max():.5f}")
            print(f"Average value over x2 axis:              {np.mean(y):.5f}")
            print(f"Integral over x1, x2 axes:               {int_z:.5f}")

        return int_x1, spl_x1
