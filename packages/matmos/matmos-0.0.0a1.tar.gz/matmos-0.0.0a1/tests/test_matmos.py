# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np
from mpl_plotter.two_d import line

from matmos import ISA


class TestCombustion(unittest.TestCase):

    def test_h(self):

        m = ISA(np.linspace(0, 85, 1000))

        line(m.p, m.h,
             demo_pad_plot=True,
             fine_tick_locations=True,
             show=True
             )

    def test_t(self):
        m = ISA(t=np.linspace(288, 216, 1000), hrange=[0, 20])

        line(m.t, m.h,
             demo_pad_plot=True,
             fine_tick_locations=True,
             show=True
             )

    def test_p(self):
        m = ISA(p=np.linspace(101325, 0.0, 1000))

        line(m.p, m.h,
             demo_pad_plot=True,
             fine_tick_locations=True,
             show=True
             )
