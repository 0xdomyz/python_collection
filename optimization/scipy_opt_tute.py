# example of sccipy minimization
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


# define the function to be minimized
def f(x):
    return x**2 + 10 * np.sin(x)


# define the derivative of the function to be minimized
def df(x):
    return 2 * x + 10 * np.cos(x)


# define the second derivative of the function to be minimized
def ddf(x):
    return 2 - 10 * np.sin(x)


# minimize the function using the BFGS algorithm
res = minimize(f, 0, method="BFGS", jac=df, hess=ddf, options={"disp": True})


def plot_function(f, x_min, x_max, ax=None):
    x = np.linspace(x_min, x_max, 1000)
    if ax is None:
        plt.plot(x, f(x))
    else:
        ax.plot(x, f(x))


def plot_minima(res, ax=None):
    if ax is None:
        plt.plot(res.x, res.fun, "ro")
    else:
        ax.plot(res.x, res.fun, "ro")


def plot(x_min, x_max, f, res):
    fig, ax = plt.subplots()
    plot_function(f, x_min, x_max, ax=ax)
    plot_minima(res, ax=ax)
    plt.show()


plot(-10, 10, f, res)
plt.show()

# minimize the function using the Nelder-Mead algorithm
res = minimize(f, 0, method="Nelder-Mead", options={"disp": True})
plot(-10, 10, f, res)
plt.show()

# minimize the function using the Powell algorithm
res = minimize(f, 0, method="Powell", options={"disp": True})
plot(-10, 10, f, res)
plt.show()

# minimize the function using the CG algorithm
res = minimize(f, 0, method="CG", jac=df, options={"disp": True})
plot(-10, 10, f, res)
plt.show()

# minimize the function using the Newton-CG algorithm
res = minimize(f, 0, method="Newton-CG", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)
plt.show()

# minimize the function using the L-BFGS-B algorithm
res = minimize(f, 0, method="L-BFGS-B", jac=df, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the TNC algorithm
res = minimize(f, 0, method="TNC", jac=df, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the COBYLA algorithm
res = minimize(f, 0, method="COBYLA", options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the SLSQP algorithm
res = minimize(f, 0, method="SLSQP", jac=df, options={"disp": True})
res = minimize(f, 0, method="SLSQP", options={"disp": True})
plot(-10, 10, f, res)

# has constraints
constriants = {"type": "ineq", "fun": lambda x: x - 2}
res = minimize(f, 0, method="SLSQP", constraints=constriants, options={"disp": True})
plot(-10, 10, f, res)

# has bounds
bounds = [(-9, -5)]
res = minimize(f, 0, method="SLSQP", bounds=bounds, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the trust-constr algorithm
res = minimize(f, 0, method="trust-constr", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the dogleg algorithm
res = minimize(f, 0, method="dogleg", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the trust-ncg algorithm
res = minimize(f, 0, method="trust-ncg", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the trust-exact algorithm
res = minimize(f, 0, method="trust-exact", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)

# minimize the function using the trust-krylov algorithm
res = minimize(f, 0, method="trust-krylov", jac=df, hess=ddf, options={"disp": True})
plot(-10, 10, f, res)


# minimize the function using the custom algorithm
def custom_minimize(f, x0, jac, hess, options):
    print("Running custom minimization algorithm")
    return minimize(f, x0, method="BFGS", jac=jac, hess=hess, options=options)


# minimize the function using the custom algorithm
res = custom_minimize(f, 0, df, ddf, {"disp": True})
plot(-10, 10, f, res)
