# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Operating system utilities
--------------------------
"""

import platform


def operating_system():
    """
    :return: Operating system of host machine.
    """
    return platform.system().lower()
