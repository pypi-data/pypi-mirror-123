# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np

from alexandria.signals.standard import step, ramp, square, triangular
from alexandria.signals.control import ControlDomain


class Tests(unittest.TestCase):

    def test_step(self):
        from mpl_plotter.presets.publication import two_d
        t = np.linspace(-10, 10, 100)
        s = 3 * step((t - 5) / 2)

        two_d.line(t, s, show=True)

    def test_ramp(self):
        from mpl_plotter.presets.publication import two_d
        t = np.linspace(-10, 10, 100)
        s = 3 * ramp((t - 5) / 2)

        two_d.line(t, s, show=True)

    def test_square(self):
        from mpl_plotter.presets.publication import two_d

        t = np.linspace(0, 4, 1000)
        s = square((t-2)/2, t)

        two_d.line(t, s, show=True)

    def test_triangular(self):
        from mpl_plotter.presets.publication import two_d

        t = np.linspace(0, 4, 1000)
        s_c = 2*triangular((t-2)/2, t)

        two_d.line(t, s_c, show=True)

    def test_control_t(self):
        a = ControlDomain(10, 1)
        assert a.t().size == 10

    def test_control_seconds_to_n(self):
        a = ControlDomain(10, 1)
        b = ControlDomain(10, 0.01)
        assert a.time_vector_length(0, 2) == 2
        assert b.time_vector_length(0, 2) == 200

    def test_control_step_forcing(self):
        b = ControlDomain(10, 0.01)
        assert b.step(5, 0, 10).mean() == 5

    def test_control_ramp_forcing(self):
        b = ControlDomain(10, 0.01)
        assert round(b.ramp(0, 5, 0, 10).mean(), 12) == 2.5
