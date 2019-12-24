import numpy as np


def linear(x, a=1, b=0):
    """
    A simple linear function usefull
    for fits

    Parameters:
    --------------------------------
    x:  1D array
        The x-axis values
    a:  Int or float
        The slope
    b:  Int or float
        The offset

    Usage:
        y = linear(x,1,0)
        For y=x
    """

    return a*x+b


def quadratic(x, a=1, b=0, c=0):
    """
    A simple quadratic function usefull
    for fits

    Parameters:
    --------------------------------
    x:  1D array
        The x-axis values
    a:  Int or float
        The amplitude
    b:  Int or float
        The x-offset
    c:  Int or float
        The y-offset

    Usage:
        y = linear(x,1,0)
        For y=x
    """
    return a*(x**2+b)+c


def exponential(x, a=1, b=1):
    """
    A simple exponential function
    usefull for fits

    Parameters:
    -----------------------------
    x:  1D array
        The x-axis values
    a:  Int or Float
        The amplitude
    b:  Int or Float
        The exponential factor

    Usage:
        y = exponential(x,1,1)
        For the e^x
    """

    return a*(np.exp(b*x))

def sinus(t,a=1,w=1,phi=0,b=0,rad=True):
    """
    A simple sinus function
    Usefull for fits

    Parameters:
    ---------------------------
    t:  1D array
        The x-axis values
    a:  Int or Float
        The amplitude
    w:  Int or Float
        The Angular frequency
    phi: Int or Float
        The angular offset
    b:  Int or Float
        The y offset
    rad: Bool
        To use radians or degrees
    """
    if not rad:
        w *= np.pi/180
        phi *= np.pi/180
    return a*np.sin(w*t+phi)+b

def cosinus(t,a=1,w=1,phi=0,b=0,rad=True):
    """
    A simple sinus function
    Usefull for fits

    Parameters:
    ---------------------------
    t:  1D array
        The x-axis values
    a:  Int or Float
        The amplitude
    w:  Int or Float
        The Angular frequency
    phi: Int or Float
        The angular offset
    b:  Int or Float
        The y offset
    rad: Bool
        To use radians or degrees
    """
    phi += np.pi/2
    return sinus(t,a,w,phi,b,rad)
