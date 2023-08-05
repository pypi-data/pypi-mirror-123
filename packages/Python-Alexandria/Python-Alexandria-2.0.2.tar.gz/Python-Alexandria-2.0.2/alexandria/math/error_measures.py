# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Error measurement utilities
---------------------------
"""


import numpy as np


def AEMAO(forecast, observation):
    """
    Absolute Error over the Mean of the Absolute Observation
    --------------------------------------------------------

    :type forecast:     np.ndarray
    :type observation:  np.ndarray
    """
    return abs(forecast - observation) / abs(observation).mean()
