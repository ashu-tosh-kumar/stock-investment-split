from enum import Enum


class ScipyOptimizeMinimizeMethods(Enum):
    """Methods to minimize the function for `scipy.optimize.minimize` function

    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

    Note: We are allowing only following out of above because only these methods allow
    adding bound AND constraints on variables
    """

    SLSQP = "SLSQP"
    TRUST_CONSTR = "trust-constr"
    COBYLA = "COBYLA"
