# -*- coding: utf-8 -*-

import numpy as _np

from .field import Field
from .propagators import ABCD, Forvard, Fresnel, backward_compatible
from .core import D4sigma

@backward_compatible
def Axicon(Fin, phi, n1 = 1.5, x_shift = 0.0, y_shift = 0.0 ):
    """
    *Propagates the field through an axicon.*
    
    :param Fin: input field
    :type Fin: Field
    :param phi: top angle of the axicon in radiants
    :type phi: int, float
    :param n1: refractive index of the axicon material (default = 1.5)
    :type phi: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in y direction (default = 0.0)
    :type y_shift: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> phi=179.7/180*3.1415
    >>> F = Axicon(F, phi) # axicon with top angle phi, refractive index = 1.5, centered in grid
    >>> F = Axicon(F,phi, n1 = 1.23, y_shift = 2*mm) # Idem, refractive index = 1.23, shifted 2 mm in y direction
    >>> F = Axicon(F, phi, 1.23, 2*mm, 0.0) # Idem
     
    .. seealso::
    
        * :ref:`Example: Bessel beam with axicon <Generation of a Bessel beam with an axicon.>`
    """
    Fout = Field.copy(Fin)
    k = 2*_np.pi/Fout.lam
    theta = _np.arcsin(n1*_np.cos(phi/2)+phi/2-_np.pi/2)
    Ktheta = k * theta
    yy, xx = Fout.mgrid_cartesian
    xx -= x_shift
    yy -= y_shift
    fi = -Ktheta*_np.sqrt(xx**2+yy**2)
    Fout.field *= _np.exp(1j*fi)
    Fout._IsGauss=False
    return Fout


def Convert(Fin):
    """
    *Converts the field from a spherical variable coordinate to a normal coordinate system.*

    :param Fin: input field
    :type Fin: Field
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = Convert(F) # convert to normal coordinates
    
    .. seealso::
    
        * :ref:`Examples: Unstable resonator <Unstable laser resonator.>`
    """
    Fout = Field.copy(Fin) #copy even if no need to convert to be consistent
    doub1 = Fin._curvature
    size = Fin.siz
    lam = Fin.lam
    N =Fin.N
    if doub1 == 0.:
        return Fout
    
    f = -1./doub1
    _2pi = 2*_np.pi
    legacy = True
    if legacy:
        _2pi=3.1415926*2. #when comparing Cpp/Py code need to match numbers
    k = _2pi/lam
    kf = k/(2*f)
    
    RR = Fout.mgrid_Rsquared
    Fi = kf*RR
    Fout.field *= _np.exp(1j* Fi)
            
    Fout._curvature = 0.0
    Fout._IsGauss=False
    return Fout

def GLens(Fin, f):
    """
    *Propagates the field through an ideal thin lens using ABCD matrix theory. Only works for a pure Gaussian input field.*
    
    :param Fin: input field (must be pure Gaussian)
    :type Fin: Field
    :param f: focal length of the lens
    :type f: int, float
    :return: output field (N x N square array of complex numbers, pure Gauss).
    :rtype: LightPipes.field.Field
    
    :Example:
    
    >>> F = GLens(F,f)
    
    .. seealso::
    
        * :ref:`Manual: Phase and intensity filters.<Phase and intensity filters.>`

    """
    A=1.0
    B=0.0
    C=-1.0/f
    D=1.0
    M=[[A,B],[C,D]]
    Fout=ABCD(Fin,M) 
    return Fout

@backward_compatible
def Lens(Fin, f, x_shift = 0.0, y_shift = 0.0):
    """
    *Propagates the field through an ideal, thin lens. If the input field is pure Gaussian, the ABCD matrix theory is used.*

    The field is multiplied by a phase given by:
    :math:`F_{out}(x,y)=e^{-j\\frac{2\\pi}{\\lambda}\\left(\\frac{(x-x_{shift})^2+(y-y_{shift})^2}{2f}\\right)}F_{in}(x,y)`
    
    :param Fin: input field
    :type Fin: Field
    :param f: focal length of the lens
    :type f: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in y direction (default = 0.0)
    :type y_shift: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = Lens(F, 50*mm) # propagate through lens with focal length of 50 mm
    >>> F = Lens(F, 50*mm, x_shift = 5*mm) # Idem, shifted 5 mm in x direction
    >>> F = Lens(F, 50*mm, 5*mm, 0.0) # Idem

    .. seealso::
    
        * :ref:`Manual: Phase and intensity filters.<Phase and intensity filters.>`

    """
    # xs,ys=D4sigma(Fin)
    # NFresnel=xs*xs/_np.pi/Fin.lam
    # print(NFresnel)
    if Fin._IsGauss and x_shift == 0.0 and y_shift == 0.0:
        print('using GaussLens')
        return GLens(Fin,f)
    else:
        Fout = Field.copy(Fin)
        _2pi = 2*_np.pi
        legacy=True
        if legacy:
            _2pi = 3.1415926*2
        k = _2pi/Fout.lam
        yy, xx = Fout.mgrid_cartesian
        xx -= x_shift
        yy -= y_shift
        fi = -k*(xx**2+yy**2)/(2*f)
        Fout.field *= _np.exp(1j * fi)
        Fout._IsGauss=False
        return Fout

def LensFarfield(Fin, f ):
    """
    *Use a direct FFT approach to calculate the far field of the input field.*
    *Given the focal length f, the correct scaling is applied and the*
    *output field will have it's values for size and dx correctly set.*

    :param Fin: input field
    :type Fin: Field
    :param f: focal length of the lens
    :type f: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`


        The focus(="far field") is related to the nearfield phase and intensity
        via the Fourier transform. Applying the correct scalings we can immediately
        calculate the focus of a measured wavefront.
        Maths relations: [e.g. Tyson Fourier Optics]
        
        lam     [m] = wavelength lambda
        f_L     [m] = focal length of lens/focusing optic
        N       [1] = grid size NxN, assume square for now
        L       [m] = size of FOV in the near field
        dx      [m] = L/N grid spacing in near field
        L'      [m] = size of FOV in focal plane
        dx'     [m] = grid spacing in focal plane
        
        lam * f_L = dx' * L
                  = dx * L'
                  = dx * dx' * N
        
        given: N, dx', lam, f_L
        lemma: L' = N * dx'
        required: L, dx
        --> L = lam * f_L / dx'
        --> dx = L / N = lam * f_L / (N * dx') = lam * f_L / L' 

    """
    Fout = Field.copy(Fin)
    dx = Fout.dx
    lam = Fout.lam
    L_prime = lam * f / dx
    focusfield = _np.fft.fftshift(_np.fft.fft2(Fout.field))
    Fout.field = focusfield
    Fout.siz = L_prime
    Fout._IsGauss=False
    return Fout

@backward_compatible
def LensForvard(Fin, f, z ):
    """
    *Propagates the field in a variable spherical coordinate system using Forvard propagator.*
    
    :param Fin: input field
    :type Fin: Field
    :param f: focal length
    :type f: int, float
    :param z: propagation distance
    :type z: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = LensForvard(F, 100*mm, 20*cm) # propagate 20 cm with spherical coordinates given by the focal length of 100 mm

    .. seealso::
    
        * :ref:`Manual: Spherical coordinates.<Spherical coordinates.>`
        
        * :ref:`Examples: Unstable laser resonator.<Unstable laser resonator.>`
    """
    LARGENUMBER = 10000000.
    doub1 = Fin._curvature
    size = Fin.siz
    lam = Fin.lam
    
    if doub1 !=0.:
        f1 = 1/doub1
    else:
        f1 = LARGENUMBER * size**2/lam
        
    if (f+f1) != 0.:
        f = (f*f1)/(f+f1)
    else:
        f = LARGENUMBER * size**2/lam
    
    if ((z-f) == 0 ):
        z1 = LARGENUMBER
    else:
        z1= -z*f/(z-f)
    
    Fout = Forvard(z1, Fin)
    
    ampl_scale = (f-z)/f
    size *= ampl_scale
    doub1 = -1./(z-f)
    Fout._curvature = doub1
    Fout.siz = size
    if z1 >= 0:
        Fout.field /= ampl_scale
    else:
        ftemp = _np.zeros_like(Fout.field, dtype=complex)
        ftemp.flat[:] = Fout.field.flat[::-1]
        Fout.field = ftemp
        Fout.field /= ampl_scale
    Fout._IsGauss=False
    return Fout

@backward_compatible
def LensFresnel(Fin, f, z ):
    """
    *Propagates the field in a variable spherical coordinate system using Fresnel propagator.*
    
    :param Fin: input field
    :type Fin: Field
    :param f: focal length
    :type f: int, float
    :param z: propagation distance
    :type z: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = LensFresnel(F, 100*mm, 20*cm) # propagate 20 cm with spherical coordinates given by the focal length of 100 mm

    .. seealso::
    
        * :ref:`Manual: Spherical coordinates.<Spherical coordinates.>`
        
        * :ref:`Examples: Unstable laser resonator.<Unstable laser resonator.>`
    """
    doub1 = Fin._curvature
    size = Fin.siz
    lam = Fin.lam
    LARGENUMBER = 10000000.
    TINY_NUMBER = 1.0e-100
    
    if f == z:
        f += TINY_NUMBER
    
    if doub1 != 0.:
        f1 = 1./doub1
    else:
        f1 = LARGENUMBER * size**2/lam
    
    if (f+f1) != 0.:
        f = (f*f1)/(f+f1)
    else:
        f = LARGENUMBER * size**2/lam
    

    z1 = -z*f/(z-f)
    if z1 < 0:
        raise ValueError('LensFresnel: Behind focus')
    """
    if (z1 < 0.0){
            cout << "error in LensFresnel: Behind focus" << endl;
            return Field;
    }
    """

    Fout = Fresnel(z1, Fin)

    ampl_scale= (f-z)/f
    size *= ampl_scale
    doub1= -1./(z-f)
    Fout.siz = size
    Fout._curvature = doub1
    Fout.field /= ampl_scale
    """
    for (int i=0;i<N; i++){
        for (int j=0;j<N; j++){	
            Field.at(i).at(j) /= ampl_scale;
        }
    }
    return Field;
    """
    # return _LP.LensFresnel(f, z, Fin)
    Fout._IsGauss=False
    return Fout
