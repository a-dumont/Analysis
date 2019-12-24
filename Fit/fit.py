import numpy as np
from scipy.optimize import curve_fit as CF
import Analysis.Functions as F


def fit(function,x,y,p0,sigma=None,bounds=(-np.inf,np.inf)):
    fit, err = CF(function,x,y,p0=p0,sigma=sigma,bounds=bounds)
    err = np.sqrt(np.diag(err))
    return fit, err

def linear_fit(x, y, p0=None, sigma=None,bounds=(-np.inf,np.inf)):
    """
    A simple Linear fit with limited options
    for more functionality use curve_fit
    manually
    """
    fit, err = CF(F.linear, x, y, p0=p0, sigma=sigma,bounds=bounds)
    err = np.sqrt(np.diag(err))

    return fit, err


def exponential_fit(x, y, p0=None, sigma=None,bounds=(-np.inf,np.inf)):
    """
    A simple exponential fit with limited
    options, for more functionnality
    use curve_fit manually
    """

    fit, err = CF(F.exponential, x, y, p0=p0, sigma=sigma,bounds=bounds)
    err = np.sqrt(np.diag(err))

    return fit, err
