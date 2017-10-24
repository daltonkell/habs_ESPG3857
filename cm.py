#!/usr/bin/env python

import matplotlib.colors
import matplotlib.pyplot as plt

percentages = [
    (0.0,    [  0,  0,139]),
    (0.0942, [  0,  0,255]),
    (0.1945, [125,158,192]),
    (0.31,   [ 98,221,221]), # light blue
    (0.4164, [  0,210,  0]), # green
    (0.5137, [255,255,  0]), # yellow
    (0.6079, [255,215,  0]), # dark yellow
    (0.7052, [255,104, 32]), # orange
    (0.7872, [251, 57, 30]), # red-orange
    (0.8541, [232,  0,  0]), # red
    (0.9119, [179,  0,  0]), # red
    (0.96,   [221,  0,221]), # purple
    (1.0,    [221,  0,221])  # purple
]

percentages = list(map(lambda l: (l[0], [x/255.0 for x in l[1]]), percentages))
R = []
G = []
B = []

for p in percentages:
    R.append((p[0], p[1][0], p[1][0]))
    G.append((p[0], p[1][1], p[1][1]))
    B.append((p[0], p[1][2], p[1][2]))

RGB=zip(R,G,B)
rgb=zip(*RGB)
k=['red', 'green', 'blue']
LinearL=dict(zip(k,rgb))

wave = matplotlib.colors.LinearSegmentedColormap('prin_wave_colormap', LinearL)
plt.show()