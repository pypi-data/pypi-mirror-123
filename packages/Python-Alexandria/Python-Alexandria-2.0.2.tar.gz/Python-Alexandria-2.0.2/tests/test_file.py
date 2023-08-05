# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest

from alexandria.file import search


class Tests(unittest.TestCase):

    def test_file_management(self):
        print(search.find_file("txt", "resources"))

    def test_file_methods(self):
        pass

    def test_parsers(self):
        pass
