#!/usr/bin/env python3
import math

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_axes([0.13, 0.15, 0.82, 0.81])

sunotofe = 8.69 - 7.50
sunnatofe = 6.24 - 7.50

# primordial
otofe1 = 10 ** (sunotofe + 0.5)
natofe1 = 10 ** (sunnatofe - 0.3)

# extreme
otofe2 = 10 ** (sunotofe - 0.3)
natofe2 = 10 ** (sunnatofe + 0.8)

xvalues = []
yvalues = []

for f in np.arange(0, 100, 0.1):
    xvalues.append(math.log10((otofe2 + f * otofe1) / (1.0 + f)) - sunotofe)
    yvalues.append(math.log10((natofe2 + f * natofe1) / (1.0 + f)) - sunnatofe)

ax.plot(xvalues, yvalues, color='black', marker='s', markersize=5, lw=1)

# ax.set_xlim(-1.2,1)

ax.set_xlabel('[O/Fe]')
ax.set_ylabel('[Na/Fe]')

fig.savefig('dilution.pdf', format='pdf')
plt.close()
