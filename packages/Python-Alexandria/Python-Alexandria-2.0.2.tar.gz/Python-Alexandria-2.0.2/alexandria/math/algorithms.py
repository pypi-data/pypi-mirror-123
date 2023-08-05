# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Algorithms
----------
"""


import itertools


def prime_factors(n):
    """
    Prime factor finding algorithm using _itertools_.

    :param n: Number.
    :return:  Generator of prime factors of _n_.
    """
    for i in itertools.chain([2], itertools.count(3, 2)):
        if n <= 1:
            break
        while n % i == 0:
            n //= i
            yield i


def largest_prime_factor(n):
    """
    Finds largest prime factor using Alexandria _prime_factor_.

    :param n: Number.
    :return:  Alexandria largest prime factor.
    """
    return list(prime_factors(n))[-1]
