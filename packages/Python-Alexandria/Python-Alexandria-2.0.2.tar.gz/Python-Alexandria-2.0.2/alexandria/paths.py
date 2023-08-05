# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Path string utilities
---------------------
"""


import os
import sys


def root():
    """
    :return: Project root directory

    Alternative method
    os.path.dirname(sys.modules['__main__'].__file__)
    """
    return "/".join(sys.argv[0].split("/")[:-1])


def home():
    """
    :return: User home directory.
    """
    return os.environ['HOME']


class path:
    """
    Class to ease the manipulation of paths
    """
    def __init__(self, path):
        self.path = os.path.abspath(path).replace("\\", "/")

    def __getitem__(self, item):
        """
        Slice the path string.

        :param item: Slice (NumPy style).
        :return: Sliced path string.
        """
        print(self.path.split("/"))
        return "/".join(self.path.split("/")[item])

    def __repr__(self):
        """
        Represent object by printing the path string.
        """
        return self.path
