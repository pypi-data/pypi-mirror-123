# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
String utilities
----------------
"""


import re

from alexandria.math.symbols import greek_letters


def capletter(s, n):
    """
    Capitalize _n_th letter of string
    """
    aux_list = list(s)
    try:
        aux_list[n] = aux_list[n].upper()
        return "".join(aux_list)
    except IndexError:
        return s


def find_between_quotations(s, q='"'):
    """
    Find substrings between quotations.

    :param s: Input string.
    :param q: Quotation mark type. Default: "
    :return: Substrings found between quotation marks _q_
    """
    try:
        if q == '"':
            return re.findall('"([^"]*)"', str(s))[0]
        elif q == "'":
            return re.findall("'([^']*)'", str(s))[0]
    except IndexError:
        return print('No match')


def join_set_distance(s, u, n=20, sep=' '):
    """
    :param s: String 1
    :param u: String 2
    :param n: Length from the beginning of String 1 to the start of String 2
    :return: Joint strings _s_ and _u_, separated by the necessary whitespace so
             the length from the first character of String 1 to the first of
             String 2 equals _n_.
    """
    if not isinstance(s, type(str)):
        s = str(s)
    m = max(n - len(s.replace("\n", "")), 1)
    return s + sep * m + u.rstrip()


def tuple_to_equal(a, n=20):
    """
    :param a: Tuple.
    :param n: Separation between first and second value of the tuple.

    :return: String of the form "tuple[0] = tuple[1]"
    """
    chars = r"()"
    for c in chars:
        if c in a:
            a = a.replace(c, "")
    k, v = a.split(',')
    return join_set_distance(k, '= ' + v, n)


def sort_based_on_other(l_subject, l_sort):
    """
    Return both input lists, sorted based on the values of the second.

    :param l_subject: List to be sorted.
    :param l_sort:    List based on the values of which both lists will be sorted.
    :return:          Both lists
    """
    sorted_tuples = [(y, x) for y, x in sorted(zip(l_sort, l_subject), reverse=True)]
    list_tuples = zip(*sorted_tuples)
    # Sorted lists (inverted as the pairs were defined as (y, x) above
    l_sort, l_subject = list(map(list, list_tuples))
    return l_subject, l_sort


def to_latex_vars(s):
    terms = s.split('_')
    for i in range(len(terms)):
        if i == 0:
            pass
        elif i > 0:
            terms[i] = '{' + terms[i] + '}$'

        if terms[i][0].isupper():
            terms[i] = terms[i].title()
        if terms[i].lower() in greek_letters():
            terms[i] = f'$\{terms[i]}$'
    return '$_'.join(terms)