# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
File search utilities
---------------------
"""


import os
import re
from itertools import chain


def find_by_ext(ext, dir):
    """
    :param ext: File extension
    :param dir: Absolute path to directory where file is to be found
    :return: Files with given extension in target directory
    """
    r = re.compile(f'.*{ext}?')
    tgt = os.path.abspath(dir)
    matches = list((filter(r.match, list(chain.from_iterable(chain.from_iterable(os.walk(tgt)))))))
    paths = list(map(lambda x: os.path.join(tgt, x).replace("\\", "/"), matches))
    return paths
