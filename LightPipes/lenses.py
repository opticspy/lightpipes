# -*- coding: utf-8 -*-

import numpy as _np

from .field import Field
from .propagators import Forvard, Fresnel

def Axicon(phi, n1, x_shift, y_shift, Fin):
    """
    Fout = Axicon(phi, n1, x_shift, y_shift, Fin)
   
    :ref:`Propagates the field through an axicon. <Axicon>`

    Args::
    
        phi: top angle of the axicon in radians
        n1: refractive index of the axicon material
        x_shift, y_shift: shift from the center
        Fin: input field
        
    Returns::
      
        Fout: output field (N x N square array of complex numbers).
            
    Example:
    
    :ref:`Bessel beam with axicon <BesselBeam>`

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
    return Fout


def Convert(Fin):
    """
    Fout = Convert(Fin)

    :ref:`Converts the field from a spherical variable coordinate to a normal coordinate system. <Convert>`

    Args::
    
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).
            
    Example:
    
    :ref:`Unstable resonator <Unstab>`
    
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
    return Fout


def Lens(f, x_shift, y_shift, Fin):
    """
    Fout = Lens(f, x_shift, y_shift, Fin)

    :ref:`Propagates the field through an ideal, thin lens. <Lens>`

    It adds a phase given by:
    :math:`F_{out}(x,y)=e^{-j\\frac{2\\pi}{\\lambda}\\left(\\frac{(x-x_{shift})^2+(y-y_{shift})^2}{2f}\\right)}F_{in}(x,y)`
        
    Args::
    
        f: focal length
        x_shift, y_shift: shift from center
        Fin: input field
        
    Returns::
    
        Fout: output field (N x N square array of complex numbers).

    """
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
    return Fout


def LensFarfield(f, Fin):
    """
    Use a direct FFT approach to calculate the far field of the input field.
    Given the focal length f, the correct scaling is applied and the
    output field will have it's values for size and dx correctly set.

    Parameters
    ----------
    f : double
        Focal length in meters/ global units
    Fin : lp.Field
        The input field.

    Returns
    -------
    The output field.

    """
    """
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
    return Fout


def LensForvard(f, z, Fin):
    """
    Fout = LensForvard(f, z, Fin)

    :ref:`Propagates the field in a variable spherical coordinate system. <LensForvard>`
        
    Args::
        
        f: focal length
        z: propagation distance
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
        
    Example:
        
    :ref:`Spherical coordinates <SphericalCoordinates>`
        
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
    return Fout


def LensFresnel(f, z, Fin):
    """
    Fout = LensFresnel(f, z, Fin)

    :ref:`Propagates the field in a variable spherical coordinate system. <LensFresnel>`
        
    Args::
        
        f: focal length
        z: propagation distance
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
        
    Example:
        
    :ref:`Spherical coordinates <SphericalCoordinates>`
        
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
    return Fout
