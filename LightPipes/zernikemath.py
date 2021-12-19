# -*- coding: utf-8 -*-

import numpy as _np


def zernike(n,m,rho,phi):
    """
    Zernike polynomial 

       +-m
      R    as in Born and Wolf, p. 465, sixth edition, Pergamon
         n
    
    The implementation have not been optimized for speed.

    Parameters
    ----------
    n : int
        DESCRIPTION.
    m : int
        DESCRIPTION.
    rho : rho
        DESCRIPTION.
    phi : phi
        DESCRIPTION.

    Returns
    -------
    double.

    """
    mabs = _np.abs(m)
    prod = 1.0
    sign = 1
    summ = 0.0
    for s in range(int((n-mabs)/2) + 1):
        if n-2*s != 0:
            prod = _np.power(rho, n-2*s)
        else:
            prod = 1.0
        prod *= _np.math.factorial(n-s)*sign
        prod /= (_np.math.factorial(s)
                * _np.math.factorial(int(((n+mabs)/2))-s)
                * _np.math.factorial(int(((n-mabs)/2))-s))
        summ += prod
        sign = -sign
    if m>=0:
        return summ*_np.cos(m*phi)
    else:
        return (-1)*summ*_np.sin(m*phi)




