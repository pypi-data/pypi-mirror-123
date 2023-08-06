# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
International Standard Atmosphere
---------------------------------
"""


import numpy as np
from alexandria.data_structs.array import ensure_ndarray, find_nearest_entry

import matmos.constants as c
from matmos.atmosphere import atmosphere


class ISA(atmosphere):

    bounds = {'troposphere':    11,
              'tropopause':     20,
              'stratosphere':   32,
              'stratosphere2':  47,
              'stratopause':    51,
              'mesosphere':     71,
              'mesosphere2':    86}

    def _run(self, h):
        """
        :type h: float or np.ndarray
        """
        h = ensure_ndarray(h)

        if h.size == 1:

            region = find_nearest_entry(list(self.bounds.values()), h)[0]

            region = region + 1 if h - list(self.bounds.values())[region] > 0 else region

            self.t, self.p, self.d = getattr(self, list(self.bounds.keys())[region])(h)

        else:

            self.t, self.p, self.d = np.zeros(h.shape), np.zeros(h.shape), np.zeros(h.shape)

            bounds = list(self.bounds.values())

            for i in range(len(bounds)):
                ub = bounds[i]
                lb = bounds[i-1] if i-1 >= 0 else 0

                region = (lb <= h) & (h < ub)

                self.t[region], self.p[region], self.d[region] = getattr(self, list(self.bounds.keys())[i])(h[region])

    def troposphere(self, h):
        """
        Troposphere
        """

        a = -6.5

        t0 = 288.15
        p0 = 101325
        d0 = 1.225

        t = t0 + a * h
        p = p0 * (1 + (a * h) / t0) ** 5.2561
        d = d0 * (1 + (a * h) / t0) ** 4.2561

        return t, p, d

    def tropopause(self, h):
        """
        Tropopause
        """

        t0 = 216.65
        p0 = 22632.1
        d0 = 0.363918

        t = t0
        p = p0 * np.exp(-c.g / (c.R * t) * ((h - 11) * 1000))
        d = d0 * np.exp(-c.g / (c.R * t) * ((h - 11) * 1000))

        return t, p, d

    def stratosphere(self, h):
        """
        Stratosphere
        """

        a = 1

        t0 = 216.65
        p0 = 5474.89
        d0 = 0.00880349

        t = t0 + a * (h - 20)
        p = p0 * (1 + (a * (h - 20)) / t) ** (-34.181185)
        d = d0 * (1 + (a * (h - 20)) / t) ** (-33.181185)

        return t, p, d

    def stratosphere2(self, h):
        """
        Stratosphere - 2
        """

        a = 2.8

        t0 = 228.65
        p0 = 868.019
        d0 = 0.013225

        t = t0 + a * (h - 32)
        p = p0 * (1 + (a * (h - 32)) / t) ** (-12.20756)
        d = d0 * (1 + (a * (h - 32)) / t) ** (-11.20756)

        return t, p, d

    def stratopause(self, h):
        """
        Stratopause
        """

        t0 = 270.65
        p0 = 110.906
        d0 = 0.00142753

        t = t0
        p = p0 * np.exp(-c.g / (c.R * t) * ((h - 47) * 1000))
        d = d0 * np.exp(-c.g / (c.R * t) * ((h - 47) * 1000))

        return t, p, d

    def mesosphere(self, h):
        """
        Mesosphere
        """

        a = -2.8

        t0 = 270.65
        p0 = 66.9389
        d0 = 0.000861606

        t = t0 + a * (h - 51)
        p = p0 * (1 + (a * (h - 51)) / t) ** 12.20756
        d = d0 * (1 + (a * (h - 51)) / t) ** 11.20756

        return t, p, d

    def mesosphere2(self, h):
        """
        Mesosphere - 2
        """

        a = -2

        t0 = 214.65
        p0 = 3.95642
        d0 = 0.000064211

        t = t0 + a * (h - 71)
        p = p0 * (1 + (a * (h - 71)) / t) ** 17.09059
        d = d0 * (1 + (a * (h - 71)) / t) ** 16.09059

        return t, p, d

    def thermosphere(self, h):
        """
        Thermosphere
        """
        raise ValueError(
            'thermosphere reached. Calculations at such and higher hitudes are out of the scope of this program.')