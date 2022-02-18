#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 11:05:10 2022

@author: fhirschmann 
"""

#!/usr/bin/env python
import pylab as pl
import numpy as np

from rdp import rdp

M = np.array([44, 95, 26, 91, 22, 90, 21, 90,
              19, 89, 17, 89, 15, 87, 15, 86, 16, 85,
              20, 83, 26, 81, 28, 80, 30, 79, 32, 74,
              32, 72, 33, 71, 34, 70, 38, 68, 43, 66,
              49, 64, 52, 63, 52, 62, 53, 59, 54, 57,
              56, 56, 57, 56, 58, 56, 59, 56, 60, 56,
              61, 55, 61, 55, 63, 55, 64, 55, 65, 54,
              67, 54, 68, 54, 76, 53, 82, 52, 84, 52,
              87, 51, 91, 51, 93, 51, 95, 51, 98, 50,
              105, 50, 113, 49, 120, 48, 127, 48, 131, 47,
              134, 47, 137, 47, 139, 47, 140, 47, 142, 47,
              145, 46, 148, 46, 152, 46, 154, 46, 155, 46,
              159, 46, 160, 46, 165, 46, 168, 46, 169, 45,
              171, 45, 173, 45, 176, 45, 182, 45, 190, 44,
              204, 43, 204, 43, 207, 43, 215, 40, 215, 38,
              215, 37, 200, 37, 195, 41]).reshape(77, 2)


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