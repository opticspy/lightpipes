# -*- coding: utf-8 -*-
"""
User defined functions for LightPipes for Python

"""
import numpy as _np
import LightPipes
    
def CylindricalLens(Fin,f,x_shift=0.0,y_shift=0.0,angle=0.0):
    """
    *Inserts a cylindrical lens in the field*
    
    :param Fin: input field
    :type Fin: Field  
    :param f: focal length
    :type f: int, float
    :param x_shift: shift in the x-direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in the y-direction (default = 0.0)
    :type y_shift: int, float
    :param angle: rotation angle (default = 0.0, horizontal)
    :type angle: int, float    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F=Begin(size,wavelength,N)
    >>> F=CylindricalLens(F,f) #Cylindrical lens in the center
    >>> F=CylindricalLens(F,f, x_shift=2*mm) #idem, shifted 2 mm in x direction
    >>> F=CylindricalLens(F,f, x_shift=2*mm, angle=30.0*deg) #idem, rotated 30 degrees
    """
    Fout = LightPipes.Field.copy(Fin)
    k = 2*_np.pi/Fout.lam
    yy, xx = Fout.mgrid_cartesian
    xx -= x_shift
    yy -= y_shift
    if angle!=0.0:
        cc = _np.cos(angle)
        ss = _np.sin(angle)
        xx = cc * xx + ss * yy
    fi = -k*(xx**2)/(2*f)
    Fout.field *= _np.exp(1j * fi)
    return Fout
