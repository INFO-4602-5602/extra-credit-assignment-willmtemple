#!/usr/bin/env python3
"""
Generate plots for my extra-credit report
"""

import sys

import numpy as np

from matplotlib import pyplot as plt

from scipy.stats import norm, multivariate_normal

# Random seed value for consistency
np.random.seed(839472938)

_N = 1000

_MU = [
    np.random.uniform(0.3, 0.7),
    np.random.uniform(0.3, 0.7)
]

_V = [
    [np.random.uniform(0.05, 0.15), 0],
    [0, np.random.uniform(0.05, 0.15)]
]

_G = multivariate_normal(_MU, _V)


#pylint: disable=invalid-name
if __name__ == '__main__':
    T = len(sys.argv) < 2
    T = T or (sys.argv[1] != 'coordinate' and sys.argv[1] != 'overlay')
    if T:
        raise ValueError("Provide either 'coordinate' or 'overlay'")

    if sys.argv[1] == 'overlay':
        @np.vectorize
        def pdfunc(x, y):
            """ Vectorized bivariate pdf """
            return _G.pdf([x, y])

        XR, YR = np.linspace(0, 1, _N), np.linspace(0, 1, _N)
        X, Y = np.meshgrid(XR, YR)
        IR = plt.imshow(pdfunc(X, Y), cmap='binary', extent=[0, 1, 1, 0])
        plt.axis([0, 1, 0, 1])
        plt.xlabel("X Distribution")
        plt.ylabel("Y Distribution")
        plt.title("Bivariate Gaussian Distribution")
        #plt.colorbar(IR) # Don't really want to show actual Density
    else:
        X = np.linspace(0, 1, 100)
        _, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
        ax1.margins(x=0)
        ax2.margins(x=0)
        ax1.plot(X, norm.pdf(X, loc=_MU[0], scale=_V[0][0]), color='black')
        ax2.plot(X, norm.pdf(X, loc=_MU[1], scale=_V[1][1]), color='black')
        ax1.set_title("X Distribution")
        ax2.set_title("Y Distribution")
        # Don't really want to show actual density
        ax1.axes.get_yaxis().set_ticks([])
        ax2.axes.get_yaxis().set_ticks([])
        plt.suptitle("Bivariate Gaussian Distribution")

    print("X: N({0}, {1})".format(_MU[0], _V[0][0]))
    print("Y: N({0}, {1})".format(_MU[1], _V[1][1]))
    plt.show()
