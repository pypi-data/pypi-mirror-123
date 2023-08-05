# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Shell color utilities
---------------------
"""


import os
import sys


class colors:
    """
    ANSI color codes for color printing to shell.
    """

    reset           = "\033[0m"

    # Black
    fgBlack         = "\033[30m"
    fgBrightBlack   = "\033[30;1m"
    bgBlack         = "\033[40m"
    bgBrightBlack   = "\033[40;1m"

    # Red
    fgRed           = "\033[31m"
    fgBrightRed     = "\033[31;1m"
    bgRed           = "\033[41m"
    bgBrightRed     = "\033[41;1m"

    # Orange (may not be supported)
    fgOrange = "\033[38:2:252:127:0m"
    fgBrightOrange = "\033[38:2:255:165:0m"
    bgOrange = "\033[48:2:252:127:0m"
    bgBrightOrange = "\033[48:2:255:165:0m"

    # Green
    fgGreen         = "\033[32m"
    fgBrightGreen   = "\033[32;1m"
    bgGreen         = "\033[42m"
    bgBrightGreen   = "\033[42;1m"

    # Yellow
    fgYellow        = "\033[33m"
    fgBrightYellow  = "\033[33;1m"
    bgYellow        = "\033[43m"
    bgBrightYellow  = "\033[43;1m"

    # Blue
    fgBlue          = "\033[34m"
    fgBrightBlue    = "\033[34;1m"
    bgBlue          = "\033[44m"
    bgBrightBlue    = "\033[44;1m"

    # Magenta
    fgMagenta       = "\033[35m"
    fgBrightMagenta = "\033[35;1m"
    bgMagenta       = "\033[45m"
    bgBrightMagenta = "\033[45;1m"

    # Cyan
    fgCyan          = "\033[36m"
    fgBrightCyan    = "\033[36;1m"
    bgCyan          = "\033[46m"
    bgBrightCyan    = "\033[46;1m"

    # White
    fgWhite         = "\033[37m"
    fgBrightWhite   = "\033[37;1m"
    bgWhite         = "\033[47m"
    bgBrightWhite   = "\033[47;1m"

    # ANSI escape sequences https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
    fmt_str         = '\033[%m'
    bold            = fmt_str.format(1)
    faint           = fmt_str.format(2)
    italic          = fmt_str.format(3)
    underline       = fmt_str.format(4)
    crossed         = fmt_str.format(9)
    framed          = fmt_str.format(51)
    encircled       = fmt_str.format(52)
    overlined       = fmt_str.format(53)


def shell_supports_color():
    """
    Returns True if the running terminal supports color, and False otherwise.

    Modified from the Django codebase - https://github.com/django/django/blob/main/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ or
                                                  os.getenv('ANSI_COLORS_DISABLED') is None)
    return supported_platform
