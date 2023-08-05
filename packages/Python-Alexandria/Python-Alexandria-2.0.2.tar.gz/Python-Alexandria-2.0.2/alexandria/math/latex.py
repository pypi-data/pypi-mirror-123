# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
LaTeX utilities
---------------
"""


from alexandria.shell import print_color


def latex_eq(var, formula):
    """
    LaTeX equation wrap.
    """
    print_color(r"\begin{equation}", "blue")
    print_color(f"   {var} = {formula}", "blue")
    print_color(r"\end{equation}", "blue")


