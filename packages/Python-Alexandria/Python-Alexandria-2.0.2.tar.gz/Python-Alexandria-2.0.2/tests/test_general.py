# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest

from alexandria.shell import print_color, print_result, print_numbered_list
from alexandria import logic
from alexandria import paths


class Tests(unittest.TestCase):

    def test_console(self):
        print_color("Color", "blue")
        print_result("A", 2, "Kg", 3)
        print_numbered_list(["a", "b", "c"], 5)

    def test_logic(self):
        assert logic.if_none("a", "b") == "a"
        assert logic.if_none(None, "b") == "b"

    def test_project(self):
        print(paths.root())

    def test_runtime(self):
        pass

