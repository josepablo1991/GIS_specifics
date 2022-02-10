#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 11:05:10 2022

@author: josepabloceballos
"""

#!/usr/bin/env python
import pylab as pl
import numpy as np

from rdp import rdp

M = np.array([13.593445400000064,
                50.832758100000035,
                13.592554700000052,
                50.833953800000074,
                13.592228200000024,
                50.83419450000007,
                13.591829700000062,
                50.83442560000003,
                13.591704500000048,
                50.83452150000005,
                13.591549300000056,
                50.83463660000007,
                13.59064230000007,
                50.83584840000003,
                13.59048830000006,
                50.83605410000007,
                13.590372600000027,
                50.836211700000035,
                13.590245300000047,
                50.836333600000046]).reshape(10, 2)


def visualize(e_min, e_max, e_0):
    pl.subplots_adjust(left=0.15, bottom=0.25)

    line, = pl.plot(M[:, 0], M[:, 1], 'b-')
    line2, = pl.plot(0, 0, 'ro--')

    pl.grid(True)
    pl.title("Ramer-Douglas-Peucker Algorithm Visualization")

    axslider = pl.axes([0.15, 0.1, 0.65, 0.03])
    slider = pl.Slider(axslider, 'Epsilon', e_min, e_max, valinit=e_0)

    def update(val):
        M2 = rdp(M, slider.val)
        line2.set_xdata(M2[:, 0])
        line2.set_ydata(M2[:, 1])

        pl.legend([line, line2], ["Original (# {0})".format(M.shape[0]),
                                  "Simplified (# {0})".format(M2.shape[0])],
                  bbox_to_anchor=(1.05, 4))

        pl.draw()

    slider.on_changed(update)
    update(e_0)

    return pl

if __name__ == "__main__":
    visualize(0, 5, 0).show()