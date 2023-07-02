# -*- coding: utf-8 -*-

import numpy as _np
from scipy.special import hermite, genlaguerre
from scipy.interpolate import RectBivariateSpline
from .misc import backward_compatible

USE_CV2 = False

if USE_CV2:
    import cv2

USE_SKIMAGE = False
if USE_SKIMAGE:
    from skimage.restoration import unwrap_phase as _unwrap_phase
else:
    #used in PhaseUnwrap
    # own implementation currently slower, but seems a little more stable
    # with jumpy phases and of course removes dependency on the extra package
    from .unwrap import unwrap_phase as _unwrap_phase

from .units import deg
from .field import Field
from .subs import Inv_Squares


def BeamMix(Fin1, Fin2):
    """
    *Addition of the fields Fin1 and Fin2.*
    
    :param Fin1: First field.
    :type Fin1: Field
    :param Fin2: Second field
    :param Fin2: Field
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = BeamMix(F1 , F2)

    .. seealso::
    
        * :ref:`Manual: Splitting and mixing beams. <Splitting and mixing beams.>`

        * :ref:`Examples: Young's experiment. <Young's experiment.>`
    """
    if Fin1.field.shape != Fin2.field.shape:
        raise ValueError('Field sizes do not match')
    Fout = Field.copy(Fin1)
    Fout.field += Fin2.field
    Fout._IsGauss=False
    return Fout

def Centroid(Fin):
    """
    *Returns the centroid of the intensity distribution.*
    
    :param Fin: input field.
    :type Fin: Field
    :return: the coordinates and the closests array indices of the centroid: Xc, Yc, NXc, NYc
    :rtype: Tuple[float, float, int, int]
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        wavelength = 500*nm
        size = 25*mm
        N = 500
        F = Begin(size, wavelength, N)
        F = CircAperture(F, 2*mm, x_shift = 5*mm, y_shift = 3*mm)
        F = Fresnel(F, 10*m)
        Xc,Yc, NXc, NYc = Centroid(F)
        print("Xc = {:4.2f} mm, Yc = {:4.2f} mm".format(Xc/mm, Yc/mm))
    
    :Answer:
    
    .. code-block::
        
        Xc = 4.96 mm, Yc = 2.97 mm
        NXc =  349, NYc =  309

    .. seealso::
        
        * :ref:`Manual: Diagnostics: Centroid.<Centroid.>`
    """
    Y,X=Fin.mgrid_cartesian
    I=Intensity(Fin)
    Xc=_np.average(X,weights = I)
    Yc=_np.average(Y,weights = I)
    # Find the array indices close to Xc and Yc:
    NXc =(_np.abs(Fin.xvalues - Xc)).argmin()
    NYc =(_np.abs(Fin.yvalues - Yc)).argmin()
    return Xc, Yc, NXc, NYc

def D4sigma(Fin):
    """
    *Returns the width (* :math:`D4\\sigma` *) of the intensity distribution.*
    
    :param Fin: input field.
    :type Fin: Field
    :return: widths in X and Y direction.
    :rtype: Tuple[float, float]
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        wavelength = 500*nm
        size = 25*mm
        N = 500
        F = Begin(size, wavelength, N)
        F = CircAperture(F, 2*mm, x_shift = 5*mm, y_shift = 3*mm)
        F = Fresnel(F, 10*m)
        sx, sy = Centroid(F)
        print("sx = {:4.2f} mm, sy = {:4.2f} mm".format(sx/mm, sy/mm))
    
    :Answer:
    
    .. code-block::
        
        sx = 6.19 mm, sy = 6.30 mm
        
    .. seealso::
        
        * :ref:`Manual => Diagnostics => Beam width => D4sigma<d4-sigma>`
    """
    
    Y,X=Fin.mgrid_cartesian
    I=Intensity(Fin)
    Xc,Yc, NXc, NYc = Centroid(Fin)
    return 4*_np.sqrt(_np.average((X-Xc)*(X-Xc), weights = I)), 4*_np.sqrt(_np.average((Y-Yc)*(Y-Yc), weights = I))

@backward_compatible
def CircAperture(Fin, R, x_shift = 0.0, y_shift = 0.0):
    """
    *Inserts a circular aperture in the field.*
    
    :param R: radius of the aperture
    :type R: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param Fin: input field
    :type Fin: Field
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = CircAperture(F, 3*mm) # A 3 mm radius circular aperture in the center of the grid.
    >>> # alternative notations:
    >>> F = CircAperture(F, 3*mm, 0, -3*mm) # Shifted -3 mm in the y-direction.
    >>> F = CircAperture(F, R = 3*mm, y_shift = -3*mm) # Idem
    >>> F = CircAperture(3*mm, 0.0, -3*mm, F) # Idem, old order of arguments for backward compatibility.
    
    .. seealso::
    
        * :ref:`Manual: Apertures and screens<Apertures and screens.>`
        
        * :ref:`Examples: Diffraction from a circular aperture.<Diffraction from a circular aperture.>`
    """
    #from
    #https://stackoverflow.com/questions/44865023/
    # circular-masking-an-image-in-python-using-numpy-arrays
    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift
    
    dist_sq = X**2 + Y**2 #squared, no need for sqrt
    
    Fout.field[dist_sq > R**2] = 0.0
    Fout._IsGauss=False
    return Fout

@backward_compatible
def CircScreen(Fin, R, x_shift=0.0, y_shift=0.0):
    """
    *Inserts a circular screen in the field.*
    
    :param Fin: input field
    :type Fin: Field    
    :param R: radius of the screen
    :type R: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = CircScreen(F, 3*mm) # A 3 mm radius circular screen in the center of the grid.
    >>> # alternative notations:
    >>> F = CircScreen(F, 3*mm, 0, -3*mm) # Shifted -3 mm in the y-direction.
    >>> F = CircScreen(F, R = 3*mm, y_shift = -3*mm) # Idem
    >>> F = CircScreen(3*mm, 0.0, -3*mm, F) # Idem, old order of arguments for backward compatibility.
    
    .. seealso::
    
        * :ref:`Manual: Apertures and screens<Apertures and screens.>`
        
        * :ref:`Examples: Spot of Poisson <Spot of Poisson.>`
    """
    #from
    #https://stackoverflow.com/questions/44865023/
    # circular-masking-an-image-in-python-using-numpy-arrays
    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift
    dist_sq = X**2 + Y**2 #squared, no need for sqrt
    
    Fout.field[dist_sq <= R**2] = 0.0
    Fout._IsGauss=False
    return Fout



@backward_compatible
def GaussAperture(Fin, w, x_shift = 0.0, y_shift = 0.0, T = 1.0, ):
    """
    *Inserts an aperture with a Gaussian shape in the field.*
    
        :math:`F_{out}(x,y)= \\sqrt{T}e^{ -\\frac{ x^{2}+y^{2} }{2w^{2}} } F_{in}(x,y)`

    :param Fin: input field
    :type Fin: Field
    :param w: 1/e intensity width
    :type w: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param T: center intensity transmission (default = 1.0)
    :type T: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = GaussAperture(Fin, w) # centered, T=1.0, width = w
    >>> F = GaussAperture(Fin, w, T = 0.5) # idem, transmission = 0.5
    >>> F = GaussAperture(Fin, w, T = 0.5, y_shift = -3 *mm) # idem, shifted in y direction
    >>> F = GaussAperture(Fin, w, 0.0, -3.0*mm, 0.5) # idem

    .. seealso::
    
        * :ref:`Manual: Apertures and screens.<Apertures and screens.>`
    """ 

    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w*2
    SqrtT=_np.sqrt(T)
    Fout.field*=SqrtT*_np.exp(-(X*X+Y*Y)/w2)
    Fout._IsGauss=False
    return Fout

def SuperGaussAperture(Fin, w, n = 2.0, x_shift = 0.0, y_shift = 0.0, T = 1.0  ):
    """
    *Inserts an aperture with a super-Gaussian shape in the field.*
    
        :math:`F_{out}(x,y)= \\sqrt{T}e^{ -\\left [ \\frac{ x^{2}+y^{2} }{2w^{2}} \\right ]^n } F_{in}(x,y)`

    :param Fin: input field
    :type Fin: Field
    :param w: 1/e intensity width
    :type w: int, float
    :param n: power of the super Gauss (default = 2.0)
    :type n: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param T: center intensity transmission (default = 1.0)
    :type T: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = SuperGaussAperture(Fin, w) # centered, T=1.0, width = w, power = 2.0
    >>> F = SuperGaussAperture(Fin, w, n = 21) # idem, power = 21
    >>> F = SuperGaussAperture(Fin, w, n = 21, y_shift = -3 *mm) # idem, shifted in y direction
    >>> F = SuperGaussAperture(Fin, w, 21, 0.0, -3.0*mm, 0.5) # idem

    .. seealso::
    
        * :ref:`Manual: Apertures and screens.<Apertures and screens.>`
    """ 

    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w*2
    SqrtT=_np.sqrt(T)
    Fout.field*=SqrtT*_np.exp(-((X*X+Y*Y)/w2)**n)
    Fout._IsGauss=False
    return Fout

@backward_compatible
def GaussScreen(Fin, w, x_shift = 0.0, y_shift = 0.0, T = 0.0 ):
    """    
    *Inserts a screen with a Gaussian shape in the field.*

        :math:`F_{out}(x,y)= \\sqrt{1-(1-T)e^{ -\\frac{ x^{2}+y^{2} }{w^{2}} }} F_{in}(x,y)`

    :param Fin: input field
    :type Fin: Field
    :param w: 1/e intensity width
    :type w: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param T: center intensity transmission (default = 0.0)
    :type T: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = GaussAperture(Fin, w) # centered, T=1.0, width = w
    >>> F = GaussAperture(Fin, w, T = 0.5) # idem, transmission = 0.5
    >>> F = GaussAperture(Fin, w, T = 0.5, y_shift = -3 *mm) # idem, shifted in y direction
    >>> F = GaussAperture(Fin, w, 0.0, -3.0*mm, 0.5) # idem

    .. seealso::
    
        * :ref:`Manual: Apertures and screens.<Apertures and screens.>`
    """  
    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w
    Fout.field*=_np.sqrt(1-(1-T)*_np.exp(-(X*X+Y*Y)/w2))
    Fout._IsGauss=False
    return Fout
    
def GaussHermite(Fin, w0, m = 0, n = 0, A = 1.0):
    """
    *Substitutes a Hermite-Gauss mode (beam waist) in the field.*

        :math:`F_{m,n}(x,y,z=0) = A H_m\\left(\\dfrac{\\sqrt{2}x}{w_0}\\right)H_n\\left(\\dfrac{\\sqrt{2}y}{w_0}\\right)e^{-\\frac{x^2+y^2}{w_0^2}}`

    :param Fin: input field
    :type Fin: Field
    :param w0: Gaussian spot size parameter in the beam waist (1/e amplitude point)
    :type w0: int, float
    :param m: mode index (default = 0.0)
    :param n: mode index (default = 0.0)
    :type m: int, float
    :type n: int, float
    :param A: amplitude (default = 1.0)
    :type A: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = GaussHermite(F, 3*mm) # Fundamental Gauss mode, HG0,0 with a beam radius of 3 mm
    >>> F = GaussHermite(F, 3*mm, m=3) # Idem, HG3,0
    >>> F = GaussHermite(F, 3*mm, m=3, n=1, A=2.0) # Idem, HG3,1, amplitude 2.0
    >>> F = GaussHermite(F, 3*mm, 3, 1, 2.0) # Idem
    
    .. seealso::
    
        * :ref:`Examples: Hermite Gauss modes.<Hermite Gauss modes.>`
        
    Reference::
    
        A. Siegman, "Lasers", p. 642
    """
    # ************* Backward compatibility section ****************
    #The general backward_compatible decorator does not work for this command,
    #because of the positional argument w0.
    _using_oldstyle = False
    if not isinstance(Fin, Field):
        #first arg is not a field, either backward compat syntax or
        # complete usage error -> find out if Field is last, else error
        if isinstance(A, Field):
            #found field in last arg
            _using_oldstyle = True #just in case code wants to know this later
            # in function
            Fin, w0, m, n, A = A, n, Fin, w0, m
            #caution: python can swap the values only if written on single
            # line, if split up a temporary assignment is necessary
            # (since a=b, b=a would not work, only temp=a, a=b, b=temp)
            #-> now all the variables contain what is expected in new style
        else:
            raise ValueError('GaussHermite: Field is neither first nor '
                             + 'last parameter (backward compatibility check)'
                             + ', please check syntax/usage.')
    # ************* end of Backward compatibility section *********
    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    #Y = Y - y_shift
    #X = X - x_shift

    sqrt2w0=_np.sqrt(2.0)/w0
    w02=w0*w0

    Fout.field  = A * hermite(m)(sqrt2w0*X)*hermite(n)(sqrt2w0*Y)*_np.exp(-(X*X+Y*Y)/w02)
    Fout._IsGauss=True
    return Fout

def GaussLaguerre(Fin, w0, p = 0, l = 0, A = 1.0 ):
    """
    *Substitutes a Laguerre-Gauss mode (beam waist) in the field.*

        :math:`F_{p,l}(x,y,z=0) = A \\left(\\frac{\\rho}{2}\\right)^{\\frac{|l|}{2} }L^p_l\\left(\\rho\\right)e^{-\\frac{\\rho}{2}}\\cos(l\\theta)`,
        
        with: :math:`\\rho=\\frac{2(x^2+y^2)}{w_0^2}`

    :param Fin: input field
    :type Fin: Field
    :param w0: Gaussian spot size parameter in the beam waist (1/e amplitude point)
    :type w0: int, float
    :param p: mode index (default = 0.0)
    :param l: mode index (default = 0.0)
    :type p: int, float
    :type l: int, float
    :param A: amplitude (default = 1.0)
    :type A: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = GaussLaguerre(F, 3*mm) # Fundamental Gauss mode, LG0,0 with a beam radius of 3 mm
    >>> F = GaussLaguerre(F, 3*mm, m=3) # Idem, LG3,0
    >>> F = GaussLaguerre(F, 3*mm, m=3, n=1, A=2.0) # Idem, LG3,1, amplitude 2.0
    >>> F = GaussLaguerre(F, 3*mm, 3, 1, 2.0) # Idem
    
    .. seealso::
    
        * :ref:`Examples: Laguerre Gauss modes.<Laguerre Gauss modes.>`
        
    Reference::
    
        A. Siegman, "Lasers", p. 642
    """
    # ************* Backward compatibility section ****************
    #The general backward_compatible decorator does not work for this command,
    #because of the positional argument w0.
    #Old style: GaussLaguerre(p, l, A, w0,Fin)
    #New style: GaussLaguerre(Fin, w0, p=0, l=0, A=1.0)
    _using_oldstyle = False
    if not isinstance(Fin, Field):
        #first arg is not a field, either backward compat syntax or
        # complete usage error -> find out if Field is last, else error
        if isinstance(A, Field):
            #found field in last arg
            _using_oldstyle = True #just in case code wants to know this later
            # in function
            Fin, w0, p, l, A = A, l, Fin, w0, p
            #caution: python can swap the values only if written on single
            # line, if split up a temporary assignment is necessary
            # (since a=b, b=a would not work, only temp=a, a=b, b=temp)
            #-> now all the variables contain what is expected in new style
        else:
            raise ValueError('GaussLaguerre: Field is neither first nor '
                             + 'last parameter (backward compatibility check)'
                             + ', please check syntax/usage.')
    # ************* end of Backward compatibility section *********
    Fout = Field.copy(Fin)
    R, Phi = Fout.mgrid_polar
    w02=w0*w0
    la=abs(l)
    rho = 2*R*R/w02
    Fout.field = A * rho**(la/2) * genlaguerre(p,la)(rho) * _np.exp(-rho/2) * _np.cos(l*Phi)
    Fout._IsGauss=False
    return Fout



@backward_compatible
def IntAttenuator(Fin, att = 0.5 ):
    """
    *Attenuates the intensity of the field.*
        
        :math:`F_{out}(x,y)=\\sqrt{att}F_{in}(x,y)`

    :param Fin: input field
    :type Fin: Field
    :param att: intensity attenuation factor (default = 0.5)
    :type att: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = IntAttenuator(F) # attenuates the intensity of the field with a factor 0.5
    >>> F = IntAttenuator(F, att = 0.2) # Idem, with a factor 0.2
    >>> F = IntAttenuator(F, 0.2) # Idem
    
    .. seealso::
    
        * :ref:`Manual: Splitting and mixing beams.<Splitting and mixing beams.>`
    
        * :ref:`Examples: Michelson interferometer.<Michelson interferometer.>`
    """
    Efactor = _np.sqrt(att) #att. given as intensity
    Fout = Field.copy(Fin)
    Fout.field *= Efactor
    return Fout

@backward_compatible
def Intensity(Fin, flag = 0):
    """
    *Calculates the intensity of the field.*
    
        :math:`I(x,y)=F_{in}(x,y).F_{in}(x,y)^*`
    
    :param Fin: input field
    :type Fin: Field
    :param flag: 0: no normalisation, 1: normalisation to 1, 2: normalized to 255 (for bitmaps) (default = 0)
    :type flag: int, float
    :return: output intensity distribution (N x N square array of real numbers).
    :rtype: `numpy.ndarray`
    :Example:
    
    >>> I = Intensity(F) # intensity of the field, no normalisation
    >>> I = Intensity(F, flag=1) # Idem, normalized to 1
    >>> I = Intensity(F, 2) # Idem, normalized to 255
    
    .. seealso::
    
        * :ref:`Manual: Graphing and visualisation.<Graphing and visualisation.>`
    """
    I = _np.abs(Fin.field)**2
    if flag > 0:
        Imax = I.max()
        if Imax == 0.0:
            raise ValueError('Cannot normalize because of 0 beam power.')
        I = I/Imax
        if flag == 2:
            I = I*255
    return I

@backward_compatible
def Interpol(Fin, new_size, new_N, x_shift = 0.0, y_shift = 0.0, angle = 0.0, magnif = 1.0 ):
    """
    *Interpolates the field to a new grid size, grid dimension.*
    
    :param Fin: input field
    :type Fin: Field
    :param new_size: new grid size
    :type new_size: int, float
    :param new_N: new grid dimension
    :type new_N: int, float
    :param x_shift: shift of the field in x direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift of the field in y direction (default = 0.0)
    :type y_shift: int, float
    :param angle: rotation of the field in degrees (default = 0.0)
    :type angle: int, float
    :param magnif: magnification of the field amplitude (default = 1.0)
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = Interpol(F, 50*mm, 200) # interpolates the field to a grid size of 50 mm and a grid dimension of 200
    >>> F = Interpol(F, 50*mm, 200, y_shift = 2*mm) # Idem, shifted 2 mm in the y direction
    >>> F = Interpol(F, 50*mm, 200, y_shift = 2*mm, magnif = 2.0) # Idem, magnifizes the field a factor 2.0
    >>> F = Interpol(F, 50*mm, 200, 0.0, 2*mm, 0.0, 2.0) # Idem
    
    .. seealso::
    
        * :ref:`Manual: Interpolation.<Interpolation.>`
        
    """

    Fout = Field.begin(new_size, Fin.lam, new_N, Fin._dtype)
    Fout.field[:,:] = 0.0
    
    legacy = True
    if legacy:
        Pi = 3.141592654 #compare Cpp results numerically
    else:
        Pi = _np.pi #more accurate, but slightly different results
    angle *= Pi/180.
    cc=_np.cos(angle)
    ss=_np.sin(angle)
    
    if legacy:
        #dx defined differently
        size_old = Fin.siz
        old_number = Fin.N
        dx_old = size_old/(old_number-1)
        on21 = int(old_number/2)
        Xold = dx_old * _np.arange(-on21, old_number-on21)
        Yold = dx_old * _np.arange(-on21, old_number-on21)
    else:
        Xold = Fin.xvalues
        Yold = Fin.yvalues
    
    if legacy:
        dx_new = new_size/(new_N-1) #TODO legacy, once again without -1 seems correct
        nn21 = int(new_N/2)
        X0 = dx_new * _np.arange(-nn21, new_N-nn21)
        Y0 = dx_new * _np.arange(-nn21, new_N-nn21)
        X0, Y0 = _np.meshgrid(X0, Y0)
    else:
        dx_new = Fout.dx
        Y0, X0 = Fout.mgrid_cartesian #note swapped order!
    X0 -= x_shift
    Y0 -= y_shift
    Xnew = (X0*cc + Y0*ss)/magnif
    Ynew = (X0*(-ss) + Y0* cc)/magnif
    
    xmin, xmax = Xold[0], Xold[-1]
    ymin, ymax = Yold[0], Yold[-1]
    #filter strictly inside (not <=) since edge pixels seem wrong in interp
    filtmask = ((Xnew > xmin) & (Xnew < xmax) &
                (Ynew > ymin) & (Ynew < ymax))
    # same goes for Cpp lightpipes, interpolating a 20x20 grid to a 20x20 grid
    # of same size will have 0s along the edges and only 18x18 useful pixels
    
    #instead of calling interp for all pixels, only call for those new pixels
    # who's coordinates (transformed to old) are inside old grid box
    Xmask = Xnew[filtmask] #flat list of X-values, not meshgrid anymore
    Ymask = Ynew[filtmask]
    
    use_scipy_interp = False
    if use_scipy_interp:
        ks = 1 #spline order: linear or higher
        interp_real = RectBivariateSpline(Xold, Yold, Fin.field.real,
                                          kx=ks, ky=ks)
        interp_imag = RectBivariateSpline(Xold, Yold, Fin.field.imag,
                                          kx=ks, ky=ks)
        
        out_real = interp_real(Xmask, Ymask, grid=False)
        out_imag = interp_imag(Xmask, Ymask, grid=False)
        out_comp = out_real + 1j* out_imag
        Fout.field[filtmask] = out_comp
    else:
        out_z = Inv_Squares(Xmask, Ymask, Fin.field, dx_old)
        Fout.field[filtmask] = out_z
    Fout.field /= magnif
    Fout._IsGauss=False
    return Fout

@backward_compatible
def MultIntensity( Fin, Intens):
    """
    *Multiplies the field with a given intensity distribution.*
    
    :param Fin: input field
    :type Fin: Field
    :param Intens: N x N square array of real numbers or scalar
    :type Intens: numpy.ndarray, float, int
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> import numpy as np
    >>> Int=np.empty([N,N])
    >>> for i in range(1,N):
    >>>     for j in range(1,N):
    >>>         Int[i][j]=math.fabs(math.sin(i/10.0)*math.cos(j/5.0))
    >>> F = MultIntensity(F, Int)

    .. seealso::
    
        * :ref:`Manual: User defined phase and intensity filters.<User defined phase and intensity filters.>`
    """
    if not _np.isscalar(Intens):
        if Intens.shape != Fin.field.shape:
            raise ValueError('Intensity pattern shape does not match field size')
    Fout = Field.copy(Fin)
    Efield = _np.sqrt(Intens)
    Fout.field *= Efield
    Fout._IsGauss=False
    return Fout

@backward_compatible
def MultPhase( Fin, Phi):
    """
    *Multiplies the field with a given phase distribution.*
    
    :param Fin: input field
    :type Fin: Field
    :param Phi: N x N square array of real numbers or scalar
    :type Phi: numpy.ndarray, int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> # multiply with a phase distribution:
    >>> #
    >>> import numpy as np
    >>> Phi=np.empty([N,N])
    >>> for i in range(1,N):
    >>>     for j in range(1,N):
    >>>         Phi[i][j]=math.fabs(math.sin(i/10.0)*math.cos(j/5.0))
    >>> F = MultPhase(F, Phi)
    >>> #
    >>> # multiply with a scalar:
    >>> F = MultPhase(F, 0.12345*rad) # multiplies the field with a constant phase factor of 0.12345 rad

    .. seealso::
    
        * :ref:`Manual: User defined phase and intensity filters.<User defined phase and intensity filters.>`
    """
    if not _np.isscalar(Phi):
        if Phi.shape != Fin.field.shape:
            raise ValueError('Phase pattern shape does not match field size')
    Fout = Field.copy(Fin)
    Fout.field *= _np.exp(1j*Phi)
    Fout._IsGauss=False
    return Fout


def Normal(Fin):
    """
    *Normalizes the field using beam power.*
    
        :math:`F_{out}(x,y)= \\frac{F_{in}(x,y)}{\\sqrt{P}}`

        with: :math:`P=\\int \\int F_{in}(x,y)^2 dx dy`
    
    :param Fin: input field
    :type Fin: Field
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = Normal(F)
    
    .. seealso::
    
        * :ref:`Manual: Diagnostics: Field normalization.<Field normalization.>`
    """
    Fabs = _np.abs(Fin.field)**2
    Fabs *= Fin.dx**2
    Ptot = Fabs.sum()
    if Ptot == 0.0:
        raise ValueError('Error in Normal(Fin): Zero beam power!')
    Fout = Field.copy(Fin)
    Fout.field *= _np.sqrt(1/Ptot)
    return Fout


def Phase(Fin, unwrap = False, units='rad', blank_eps=0):
    """
    *Calculates the phase of the field.*
    
    :param Fin: input field
    :type Fin: Field
    :param unwrap: Call PhaseUnwrap on the extracted Phase (default = False)
    :type unwrap: bool
    :param units:   'opd': returned in [meters] of optical path length
                    'lam': returned in multiples of lambda
                    'rad': returned in multiples of 2pi phase jumps (default)
    :type units: string
    :param blank_eps:  [fraction] of max. Intensity at which to blank the phase
                        and replace the value with numpy.nan (e.g. 1e-3==0.1%)
                        Set to 0 or None to disable
    :type blank_eps: int, None
    :return: output phase distribution (N x N square array of real numbers).
    :rtype: `numpy.ndarray`
    :Example:
    
    >>> Phi = Phase(F) # returns phase distribution
    >>> Phi = Phase(F, unwrap = True) # Idem, phase unwrapped
    >>> Phi = Phase(F, units = 'lam') # phase in multiples of wavelength
    
    .. seealso::
        
        * :ref:`Manual: Graphing and visualisation.<Graphing and visualisation.>`
    """
    _2pi = 2*_np.pi
    Phi = _np.angle(Fin.field)
    if unwrap:
        Phi = PhaseUnwrap(Phi)
    
    if units=='opd':
        Phi = Phi/_2pi*Fin.lam #a PtV of 2pi will yield e.g. 1*lam=1e-6=1um
    elif units=='lam':
        Phi = Phi/_2pi #a PtV of 2pi=6.28 will yield 1 (as in 1 lambda)
    elif units=='rad':
        pass #a PtV of 2pi will yield 6.28 as requested
    else:
        raise ValueError('Unknown value for option units={}'.format(units))
        
    if blank_eps:
        I = Intensity(0,Fin)
        Phi[I<blank_eps*I.max()] = _np.nan
        
    return Phi

def PhaseSpiral(Fin, m = 1):
    """
    *Multiplies Fin with a spiral phase distribution.*
    
    :param Fin: input field
    :type Fin: Field
    :param m: Order of the spiral (default = 1)
    :type m: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> order = 2
    >>> F=PhaseSpiral(F,m=order) # multiplies the field with a spiral phase distribution of order 2
    
    """
    Fout = Field.copy(Fin) 
    R, Phi = Fout.mgrid_polar  
    Fout.field *= _np.exp(1j * m * Phi)
    Fout._IsGauss=False
    return Fout

def PhaseUnwrap(Phi):
    """
    *Unwraps (removes jumps of pi radians) the phase.*
    
    :param Phi: input phase distribution
    :type Phi: numpy
    :param Phi: Order of the spiral (default = 1)
    :type m: int, float
    :return: output phase distribution (N x N square array of real numbers).
    :rtype: `numpy.ndarray`
    :Example:
    
    >>> Phi = PhaseUnwrap(Phi) # unwraps the phase distribution Phi
    """
    PhiU = _unwrap_phase(Phi)
    return PhiU


def Power(Fin):
    """
    *Calculates the total power.*
    
    .. math:: P=\\int \\int(|F_{in}(x,y)|)^2dxdy
    
    :param Fin: input field
    :type Fin: Field
    :return: output power
    :rtype: float
    :Example:
    
    >>> P = Power(F) # returns the power of the field F
      
    """
    I = _np.abs(Fin.field)**2
    return I.sum() * Fin.dx**2

@backward_compatible
def RandomIntensity(Fin, seed = 123, noise = 1.0, ):
    """
    *Adds random intensity to the field*
    
    :param Fin: input field
    :type Fin: Field
    :param seed: seed number for the random noise generator (default = 123)
    :type seed: int, float
    :param noise: level of the noise (default = 1.0)
    :type noise: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = RandomIntensity(F) # adds noise to the field
    >>> F = RandomIntensity(F, seed = 49) # Idem, with seed 49
    >>> F = RandomIntensity(F, noise = 0.1) # adds noise to the field with amplitude 0.1

    .. seealso::
    
        * :ref:`Manual: Random filters.<Random filters.>`
    """
    #TODO implementation error in original LP: field error, not I error!
    # need to sqrt for that
    Fout = Field.copy(Fin)
    _np.random.seed(int(seed))
    N = Fout.N
    ranint = _np.random.rand(N, N)*noise
    Fout.field += ranint
    Fout._IsGauss=False
    return Fout

@backward_compatible
def RandomPhase(Fin, seed =456, maxPhase = _np.pi ):
    """
    *Adds random phase to the field*
    
    :param Fin: input field
    :type Fin: Field
    :param seed: seed number for the random noise generator (default = 456)
    :type seed: int, float
    :param maxPhase: max value of the phase (default = 3.1415 (pi))
    :type maxPhase: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = RandomPhase(F) # adds noise to the phase of the field
    >>> F = RandomPhase(F, seed = 49) # Idem, with seed 49
    >>> F = RandomPhase(F, maxPhase = 0.1) # adds phase-noise to the field with maximum value 0.1

    .. seealso::
    
        * :ref:`Manual: Random filters.<Random filters.>`
    """
    #2020023 - ldo - tested similar result as Cpp version, although not 
    # 1:1 since seed is different in numpy
    Fout = Field.copy(Fin)
    _np.random.seed(int(seed))
    N = Fout.N
    ranphase = (_np.random.rand(N, N)-0.5)*maxPhase
    Fout.field *= _np.exp(1j * ranphase)
    Fout._IsGauss=False
    return Fout

@backward_compatible
def RectAperture(Fin, sx, sy, x_shift = 0.0, y_shift = 0.0, angle = 0.0 ):
    """
    *Inserts a rectangular aperture in the field.*
    
    :param Fin: input field
    :type Fin: Field    
    :param sx: width of the aperture
    :type sx: int, float
    :param sy: height of the aperture
    :type sy: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param angle: rotation angle in degrees (default = 0.0)
    :type angle: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = RectAperture(F, 3*mm, 4*mm) # A 3 x 4 mm rectangular aperture in the center of the grid.
    >>> F = RectAperture(F, 3*mm, 4*mm, 0, -3*mm) # Idem, shifted -3 mm in the y-direction.
    >>> F = RectAperture(F, 3*mm, 4*mm, y_shift = -3*mm) # Idem
    
    .. seealso::
    
        * :ref:`Manual: Apertures and screens<Apertures and screens.>`
    """
    Fout = Field.copy(Fin)
    yy, xx = Fout.mgrid_cartesian
    yy = yy - y_shift
    xx = xx - x_shift
    if angle!=0.0:
        ang_rad = -1*angle*deg #-1 copied from Cpp convention
        cc = _np.cos(ang_rad)
        ss = _np.sin(ang_rad)
        xxr = cc * xx + ss * yy
        yyr = -ss * xx + cc * yy
        yy, xx = yyr, xxr
    matchx = _np.abs(xx) > sx/2
    matchy = _np.abs(yy) > sy/2
    Fout.field[matchx | matchy] = 0.0
    Fout._IsGauss=False
    return Fout

@backward_compatible
def RectScreen(Fin, sx, sy, x_shift = 0.0, y_shift = 0.0, angle = 0.0 ):
    """
    *Inserts a rectangular screen in the field.*
    
    :param Fin: input field
    :type Fin: Field    
    :param sx: width of the screen
    :type sx: int, float
    :param sy: height of the screen
    :type sy: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :param y_shift: shift in y direction (default = 0.0)
    :type x_shift: int, float
    :type y_shift: int, float
    :param angle: rotation angle in degrees (default = 0.0)
    :type angle: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = RectScreen(F, 3*mm, 4*mm) # A 3 x 4 mm rectangular screen in the center of the grid.
    >>> F = RectScreen(F, 3*mm, 4*mm, 0, -3*mm) # Idem, shifted -3 mm in the y-direction.
    >>> F = RectScreen(F, 3*mm, 4*mm, y_shift = -3*mm) # Idem
    
    .. seealso::
    
        * :ref:`Manual: Apertures and screens<Apertures and screens.>`
    """
    Fout = Field.copy(Fin)
    yy, xx = Fout.mgrid_cartesian
    yy = yy - y_shift
    xx = xx - x_shift
    if angle!=0.0:
        ang_rad = -1*angle*deg #-1 copied from Cpp convention
        cc = _np.cos(ang_rad)
        ss = _np.sin(ang_rad)
        xxr = cc * xx + ss * yy
        yyr = -ss * xx + cc * yy
        yy, xx = yyr, xxr
    matchx = _np.abs(xx) <= sx/2
    matchy = _np.abs(yy) <= sy/2
    Fout.field[matchx & matchy] = 0.0
    Fout._IsGauss=False
    return Fout


def Strehl(Fin):
    """
    *Calculates the Strehl value of the field*
    
    :param Fin: input field
    :type Fin: Field    
    :return: Strehl value of the field
    :rtype: float
    :Example:
    
    >>> S = Strehl(F) # returns the Strehl value of the field
    
    .. seealso::
        
        * :ref:`Manual: Diagnostics: Strehl ratio.<Strehl ratio.>`
    """
    normsq = _np.abs(Fin.field).sum()**2
    if normsq == 0.0:
        raise ValueError('Error in Strehl: Zero beam power')
    strehl = _np.real(Fin.field).sum()**2 + _np.imag(Fin.field).sum()**2
    strehl = strehl/normsq
    return strehl

@backward_compatible
def SubIntensity(Fin, Intens ):
    """
    *Substitutes  a given intensity distribution in the field with.*
    
    :param Fin: input field
    :type Fin: Field
    :param Intens: N x N square array of real numbers or scalar
    :type Intens: numpy.ndarray, int, float    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. seealso::
    
        * :ref:`Matlab: User defined phase and intensity filters.<User defined phase and intensity filters.>`
    """
    Fout = Field.copy(Fin)
    Intens = _np.asarray(Intens)
    if Intens.shape != Fout.field.shape:
        raise ValueError('Intensity map has wrong shape')
    phi = _np.angle(Fout.field)
    Efield = _np.sqrt(Intens)
    Fout.field = Efield * _np.exp(1j * phi)
    Fout._IsGauss=False
    return Fout

@backward_compatible
def SubPhase( Fin, Phi):
    """
    *Substitutes  a given phase distribution in the field with.*
    
    :param Phi: N x N square array of real numbers or scalar
    :type Phi: numpy.ndarray, int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. seealso::
    
        * :ref:`Manual: User defined phase and intensity filters.<User defined phase and intensity filters.>`
    """
    Fout = Field.copy(Fin)
    if not _np.isscalar(Phi):
        Phi = _np.asarray(Phi)
        if Phi.shape != Fin.field.shape:
            raise ValueError('Phase map has wrong shape')
    oldabs = _np.abs(Fout.field)
    Fout.field = oldabs * _np.exp(1j * Phi)
    Fout._IsGauss=False
    return Fout


