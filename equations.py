# equations.py>
import numpy as np

def derivatives(x, y, t):
    dir_x_1 = np.gradient(x,t)
    dir_x_2 = np.gradient(dir_x_1,t)
    dir_y_1 = np.gradient(y,t)
    dir_y_2 = np.gradient(dir_y_1,t)
    return dir_x_1, dir_x_2, dir_y_1, dir_y_2

def lemniscate(t, a, fac):
    x = a*np.cos(fac*t) * 1/(1+np.sin(fac*t)**2)
    y = a*np.sin(fac*t)*np.cos(fac*t) * 1/(1+np.sin(fac*t)**2)
    return x, y


def circle(t, a, fac):
     # -- Circle --
    x = a*np.cos(fac * t)
    y = a*np.sin(fac * t)
    return x, y


def other():
    # -- line --
    """x = t
    y = 0*t"""

    # -- Lissajous curve --
    """x = 4*np.cos(1.5*t)
    y = 4*np.sin(t)"""

    # -- Test 1 --
    """x = 2*np.cos(t)+1
    y = 5*np.sin(2*t)"""

    # -- cardioid --
    """x = 2*np.cos(t)*(1-np.cos(t))
    y = 2*np.sin(t)*(1-np.cos(t))"""
