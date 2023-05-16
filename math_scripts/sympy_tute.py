# example of python package that does math symbolic differentiation

import re


def diff(expr, var):
    """Return the symbolic derivative of expr with respect to var."""
    if expr == var:
        return 1
    elif not re.search("[a-z]", expr):
        return 0
    elif expr[0] == "+":
        return diff(expr[1:], var)
    elif expr[0] == "-":
        return -diff(expr[1:], var)
    elif expr[0] == "*":
        return diff(expr[1:3], var) + expr[1] + "*" + diff(expr[3:], var)
    elif expr[0] == "/":
        return (
            "("
            + diff(expr[1:3], var)
            + "*"
            + expr[3:]
            + "-"
            + expr[1]
            + "*"
            + diff(expr[3:], var)
            + ")/"
            + expr[3:]
            + "**2"
        )
    elif expr[0] == "^":
        return (
            expr[1]
            + "**"
            + expr[3:]
            + "*"
            + diff(expr[1:3], var)
            + "*"
            + expr[3:]
            + "/"
            + expr[1]
        )
    else:
        raise ValueError("invalid expression")


# test cases
diff("x", "x")
diff("x**2", "x")
diff("x**2 + 2*x + 1", "x")

# example of using sympy
import sympy as sp

x = sp.Symbol("x")
sp.diff(x**2 + 2 * x + 1, x)
