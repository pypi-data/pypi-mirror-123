# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Differential equation integration schemes
-----------------------------------------
"""

import numpy as np


def newton_euler(f, h, F0, *args, **kwargs):
    """
    Newton-Euler integration scheme
    -------------------------------

    :type f:        function
    :type h:        float
    :type F0:       float
    :type args:     list of any
    :type kwargs:   dict of any
    """
    F1 = F0 + h*f(F0, *args, **kwargs)
    return F1


def heun(f, h, F0, *args, **kwargs):
    """
    Heun's method
    -------------

    :type f:        function
    :type h:        float
    :type F0:       float
    :type args:     list of any
    :type kwargs:   dict of any
    """
    _F1 = F0 + h*f(F0, *args, **kwargs)
    F1  = F0 + 1/2*(_F1 + h*f(_F1, *args, **kwargs))
    return F1


def runge_kutta_4(f, h, F0, f0, *args, **kwargs):
    """
    4th order Runge-Kutta integration scheme
    ----------------------------------------

    For a time and state dependent differential equation.

    :param F0:      Initial value of the function
    :param f0:      Initial value of the derivative of the function

    :type f:        function
    :type h:        float
    :type F0:       float
    :type f0:       float
    :type args:     list of any
    :type kwargs:   dict of any
    """

    k1a = h * f0
    k1b = h * f(F0, *args, **kwargs)

    k2a = h * (f0 + k1b/2)
    k2b = h * f(F0 + k1a/2, *args, **kwargs)

    k3a = h * (f0 + k2b/2)
    k3b = h * f(F0 + k2a/2, *args, **kwargs)

    k4a = h * (f0 + k3b)
    k4b = h * f(F0 + k3a, *args, **kwargs)

    F1  = F0 + 1/6*(k1a + 2*k2a + 2*k3a + k4a)
    dF1 = f0 + 1/6*(k1b + 2*k2b + 2*k3b + k4b)

    return np.array([F1, dF1])
