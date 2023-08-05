# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Plain text file utilities
-------------------------
"""


def save_txt(filename, string):
    with open(filename, 'a') as f:
        f.write('	'.join(map(str, string))+'\n')
