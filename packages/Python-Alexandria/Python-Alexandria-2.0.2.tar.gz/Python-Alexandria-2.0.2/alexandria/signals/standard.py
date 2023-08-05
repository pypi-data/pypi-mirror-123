# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Standard signals
----------------
"""


import numpy as np

from alexandria.math.differentiation import forward_euler

from alexandria.data_structs.array import find_nearest_entry


def step(t):
    """
    Step signal.

    :param t: Time vector.
    :return: Step signal.
    """
    return np.array([1 if i > 0 else 0 for i in t]).flatten()


def ramp(t):
    """
    Ramp signal.

    :param t: Time vector.
    :return: Ramp signal.
    """
    return np.array([max(0, i) for i in t]).flatten()


def square(f, t):
    """
    Square signal.

    :param f: Square signal "formula".
    :param t: Time vector.
    :return: Square signal vector.

    Example:

        t = np.linspace(0, 10, 100)
        f = (-t+5)/3

        s = square(f, t)

    """
    base           = abs(1/forward_euler(t, f))
    center_idx     = find_nearest_entry(f, 0)[0]
    center         = t[center_idx]
    l_idx          = find_nearest_entry(t, center - base/2)[0]
    u_idx          = find_nearest_entry(t, center + base/2)[0]
    s              = np.zeros(t.shape)
    s[l_idx:u_idx] = 1
    return s


def triangular(f, t):
    """
    Triangular signal. Convolution of two square waves.

    :param f: Triangular signal "formula".
    :param t: Time vector.
    :return: Triangular signal vector.

    Example:

        t = np.linspace(0, 10, 100)
        f = (-t+5)/3

        s = triangular(f, t)

    """
    s = np.convolve(square(f, t), square(f, t), 'same')
    s = s/s.max()
    return s

