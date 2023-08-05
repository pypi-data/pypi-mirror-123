# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Units
-----
"""


import numpy as np
from math import ceil


# Angles
def deg(a):
    return a/np.pi*180


def rad(a):
    return a/180*np.pi


# Mass
def lbs_to_kg(m):
    return m*0.453592


# Conversion
def s_to_hms(n):
    """
    Decimal seconds to
        hh :: m :: ss
    """
    hours, remainder = divmod(n, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), seconds


def d_to_dms(n):
    """
    Decimal degrees to
        dd :: mm :: ss.ss
    """
    mnt, sec = divmod(n*3600, 60)
    deg, mnt = divmod(mnt, 60)
    return int(deg), int(mnt), sec
