"""
example of compute the discrete wavelet transform (DWT) of a signal using PyWavelets
"""

import matplotlib.pyplot as plt
import numpy as np
import pywt
import seaborn as sns

sns.set()
x = np.linspace(0, 1, 200)
y = np.sin(12 * np.pi * x) + 0.5 * np.sin(25 * np.pi * x)
plt.plot(x, y)
plt.show()

# perform DWT
coeffs = pywt.wavedec(y, "db4", level=4)

# plot the approximation
plt.plot(coeffs[0], label="A5", linewidth=5)
plt.show()

# plot detail coefficients together with original signal
plt.plot(y, label="original")
for i, d in enumerate(coeffs[1:]):
    plt.plot(d, label="D{}".format(i + 1))
plt.legend(loc="best")
plt.show()


# reconstruct the signal
y_recon = pywt.waverec(coeffs, "db4")
plt.plot(x, y, label="original")
plt.plot(x, y_recon, label="reconstructed")
plt.legend(loc="best")
plt.show()
