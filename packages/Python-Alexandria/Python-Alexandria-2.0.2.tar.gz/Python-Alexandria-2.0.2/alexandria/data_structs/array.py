# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
NumPy array utilities
---------------------
"""


import numpy as np


from alexandria.math.numbers import get_representative_decimals


def find_nearest_entry(array, value):
    """
    Find nearest entry of array to input value.

    :param array: Array.
    :param value: Input value.

    :param array: np.ndarray
    :param value: float

    :return: [int]   Index of closest value in array
             [float] Closest value in array
    """
    array = ensure_ndarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def span(a):
    """
    Find the difference between the highest and lowest elements
    of a list or array.

    :param a: Array.

    :type a: np.ndarray | list

    :return: [float] Array span.
    """
    a = ensure_ndarray(a)
    if a.size > 1:
        a_s = a + a.min() if a.min() < 0 else a
        return a_s.max() - a_s.min()
    elif a.size == 1:
        return 0


def internal_array_shape(x):
    """
    Find shape of all internal arrays of an input array x.

    :param x: Array.

    :type x: np.ndarray | list

    :return: [np.ndarray] Array with the shapes of all internal
             arrays of _x_.
    """
    x = ensure_ndarray(x)
    if x.ndim > 1:
        return np.array([x[n].shape for n in range(len(x))])
    else:
        return np.ones(x.shape)


def dx_v(t):
    """
    :return: Return vector of base dimension increments, where the base dimension is X in
                    f(X)
             for higher precision differentiation or integration with uneven measurements.
    """
    t = ensure_ndarray(t)
    dt_v = np.array(list([t[i + 1] - t[i]] for i in range(t.size - 1)))
    dt_v = np.append(dt_v, np.array([t[-1] - t[-2]]))
    return dt_v


def pretty_array(a):
    """
    Pretty print NumPy array
    """
    return np.array2string(a, precision=get_representative_decimals(np.min(a[np.nonzero(a)])), suppress_small=True)


def lists_to_ndarrays(*args):
    """
    Transform a series of lists into NumPy arrays, and return them contained in a parent NumPy array
    :param args: Number n of lists.
    :return: Array of NumPy arrays.
    """
    import inspect
    args, _, _, values = inspect.getargvalues(inspect.currentframe())
    inputs = np.array(values["args"], dtype=object).squeeze()
    try:
        for i in range(len(inputs)):
            if isinstance(inputs[i], np.ndarray):
                inputs[i] = lists_to_ndarrays(inputs[i])
            elif isinstance(inputs[i], list):
                inputs[i] = np.array(inputs[i])
                inputs[i] = lists_to_ndarrays(inputs[i])
            else:
                pass
    except TypeError:
        # End of recursion
        pass
    return inputs


def ensure_ndarray(a):
    """
    Return _a_ if it is a NumPy array, or else return _a_
    as a NumPy array.
    """
    return np.asarray(a) if not isinstance(a, np.ndarray) else a
