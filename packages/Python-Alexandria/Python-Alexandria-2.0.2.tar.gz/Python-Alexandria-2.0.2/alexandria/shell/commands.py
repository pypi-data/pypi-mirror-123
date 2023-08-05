# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Shell command utilities
-----------------------
"""


import os
import sys
import subprocess
from contextlib import contextmanager


def shell(command):
    """
    Executes command in shell.

    :param command: command string
    """
    return subprocess.run(command, shell=True, capture_output=True)


def raise_error(command):
    """
    Executes command in shell and raises an error if the command outputs non-zero exit code.

    :param command: command string
    """
    return subprocess.check_output(command, shell=True)


def bckgr(command):
    """
    Run shell command as background process.

    :param command: command string
    """
    return subprocess.Popen(command, shell=True)


def error():
    """
    :return: subprocess.CalledProcessError
    """
    return subprocess.CalledProcessError
