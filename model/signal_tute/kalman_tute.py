"""
An example using a kalman filter to model a car's position and velocity.
plots predictions to illustrate how the kalman filter works.
"""
import matplotlib.pyplot as plt
import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter

dt = 1.0  # time step
# create a kalman filter
kf = KalmanFilter(dim_x=2, dim_z=1)
kf.x = np.array([[0.0], [0.0]])  # position  # velocity
kf.F = np.array([[1.0, dt], [0.0, 1.0]])
kf.H = np.array([[1.0, 0.0]])
kf.P *= 1000.0  # covariance matrix
kf.R = 5  # state uncertainty
kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=0.13)

zs = np.random.randn(20) * 10
xs, cov = [], []
for z in zs:
    kf.predict()
    kf.update(z)
    xs.append(kf.x)
    cov.append(kf.P[0, 0])

xs, cov = np.array(xs).squeeze(), np.array(cov).squeeze()
plt.plot(np.arange(len(zs)), zs, "o", label="noisy measurements")
plt.plot(np.arange(len(zs)), xs[:, 0], label="a posteri estimate")
plt.plot(np.arange(len(zs)), xs[:, 0] + np.sqrt(cov), label="upper bound")
plt.plot(np.arange(len(zs)), xs[:, 0] - np.sqrt(cov), label="lower bound")
plt.legend()
plt.show()


"""
An example using a kalman filter to model a car's position and velocity, and acceleration.
plots predictions to illustrate how the kalman filter works.
"""
import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter

dt = 1.0  # time step
# create a kalman filter
kf = KalmanFilter(dim_x=3, dim_z=1)
kf.x = np.array([[0.0], [0.0], [0.0]])  # position  # velocity  # acceleration
kf.F = np.array([[1.0, dt, dt**2 / 2], [0.0, 1.0, dt], [0.0, 0.0, 1.0]])
kf.H = np.array([[1.0, 0.0, 0.0]])
kf.P *= 1000.0  # covariance matrix
kf.R = 5  # state uncertainty
kf.Q = Q_discrete_white_noise(dim=3, dt=dt, var=0.13)

zs = np.random.randn(20) * 10
xs, cov = [], []
for z in zs:
    kf.predict()
    kf.update(z)
    xs.append(kf.x)
    cov.append(kf.P[0, 0])

xs, cov = np.array(xs).squeeze(), np.array(cov).squeeze()
plt.plot(np.arange(len(zs)), zs, "o", label="noisy measurements")
plt.plot(np.arange(len(zs)), xs[:, 0], label="a posteri estimate")
plt.plot(np.arange(len(zs)), xs[:, 0] + np.sqrt(cov), label="upper bound")
plt.plot(np.arange(len(zs)), xs[:, 0] - np.sqrt(cov), label="lower bound")
plt.legend()
plt.show()

# plot the position, velocity, and acceleration
plt.plot(np.arange(len(zs)), xs[:, 0], label="position")
plt.plot(np.arange(len(zs)), xs[:, 1], label="velocity")
plt.plot(np.arange(len(zs)), xs[:, 2], label="acceleration")
plt.legend()
plt.show()
