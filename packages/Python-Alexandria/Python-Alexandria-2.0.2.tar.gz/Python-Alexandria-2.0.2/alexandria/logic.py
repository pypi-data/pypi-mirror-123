# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Simple logical clauses
----------------------
"""


def if_none(a, b):
    """
    :param a: Variable 1
    :param b: Variable 2
    :return: a if it's not None, else b
    """
    return b if isinstance(a, type(None)) else a
