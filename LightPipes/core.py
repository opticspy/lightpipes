# -*- coding: utf-8 -*-

import numpy as _np
from scipy.special import hermite, genlaguerre
from scipy.interpolate import RectBivariateSpline


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
    Fout = BeamMix(F1, F2)

    :ref:`Addition of the fields F1 and F2. <BeamMix>`

    Args::
    
        F1, F2: input fields
        
    Returns::
      
        Fout: output field (N x N square array of complex numbers).
        
    Example:
    
    :ref:`Two holes interferometer <Young>`
    
    """
    if Fin1.field.shape != Fin2.field.shape:
        raise ValueError('Field sizes do not match')
    Fout = Field.copy(Fin1)
    Fout.field += Fin2.field
    return Fout

def CircAperture(R, x_shift, y_shift, Fin):
    """
    Fout = CircAperture(R, x_shift, y_shift, Fin)
    
    :ref:`Propagates the field through a circular aperture. <CircAperture>`

    Args::
    
        R: radius of the aperture
        x_shift, y_shift: shift from the center
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).
            
    Example:
    
    :ref:`Diffraction from a circular aperture <circ_aperture>`
    
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
    return Fout

def CircScreen(R, x_shift, y_shift, Fin):
    """
    Fout = CircScreen(R, x_shift, y_shift, Fin)
                
    :ref:`Diffracts the field by a circular screen. <CircScreen>`

    Args::
    
        R: radius of the screen
        x_shift, y_shift: shift from the center
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).
            
    Example:
    
    :ref:`Spot of Poisson <Poisson>`
    
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
    return Fout

def GaussAperture(w, x_shift, y_shift, T, Fin):
    """
    Fout = GaussAperture(w, x_shift, y_shift, T, Fin)
    
    :ref:`Inserts an aperture with a Gaussian shape in the field. <GaussAperture>`
    
        :math:`F_{out}(x,y)= \\sqrt{T}e^{ -\\frac{ x^{2}+y^{2} }{2w^{2}} } F_{in}(x,y)`

    Args::
    
        w: 1/e intensity width
        x_shift, y_shift: shift from center
        T: center intensity transmission
        Fin: input field
    
    Returns::
    
        Fout: output field (N x N square array of complex numbers).

    """ 

    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w*2
    SqrtT=_np.sqrt(T)
    Fout.field*=SqrtT*_np.exp(-(X*X+Y*Y)/w2)
    return Fout

def SuperGaussAperture(w, x_shift, y_shift, T, n, Fin):
    """
    Fout = SuperGaussAperture(w, x_shift, y_shift, T, n, Fin)
    
    :ref:`Inserts an aperture with a Gaussian shape in the field. <GaussAperture>`
    
        :math:`F_{out}(x,y)= \\sqrt{T}e^{ -\\frac{ x^{2}+y^{2} }{2w^{2}} } F_{in}(x,y)`

    Args::
    
        w: 1/e intensity width
        x_shift, y_shift: shift from center
        T: center intensity transmission
        n: power of the super Gaussian
        Fin: input field
    
    Returns::
    
        Fout: output field (N x N square array of complex numbers).

    """ 

    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w*2
    SqrtT=_np.sqrt(T)
    Fout.field*=SqrtT*_np.exp(-((X*X+Y*Y)/w2)**n)
    return Fout

def GaussScreen(w, x_shift, y_shift, T, Fin):
    """
    Fout = GaussScreen(w, x_shift, y_shift, T, Fin)
    
    :ref:`Inserts a screen with a Gaussian shape in the field. <GaussScreen>`

        :math:`F_{out}(x,y)= \\sqrt{1-(1-T)e^{ -\\frac{ x^{2}+y^{2} }{w^{2}} }} F_{in}(x,y)`

   Args::
    
        w: 1/e intensity width
        x_shift, y_shift: shift from center
        T: center intensity transmission
        Fin: input field
    
    Returns::
    
        Fout: output field (N x N square array of complex numbers).

    """  
    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    Y = Y - y_shift
    X = X - x_shift

    w2=w*w
    Fout.field*=_np.sqrt(1-(1-T)*_np.exp(-(X*X+Y*Y)/w2))
    return Fout
    
def GaussHermite( n, m, A, w0, Fin):
    """
    Fout = GaussHermite(m, n, A, w0, Fin)
    
    :ref:`Substitutes a Hermite-Gauss mode (beam waist) in the field. <GaussHermite>`

        :math:`F_{m,n}(x,y,z=0) = A H_m\\left(\\dfrac{\\sqrt{2}x}{w_0}\\right)H_n\\left(\\dfrac{\\sqrt{2}y}{w_0}\\right)e^{-\\frac{x^2+y^2}{w_0^2}}`

    Args::
        
        m, n: mode indices
        A: Amplitude
        w0: Guaussian spot size parameter in the beam waist (1/e amplitude point)
        Fin: input field
        
    Returns::
    
        Fout: output field (N x N square array of complex numbers).            
        
    Reference::
    
        A. Siegman, "Lasers", p. 642

    """

    Fout = Field.copy(Fin)
    
    Y, X = Fout.mgrid_cartesian
    #Y = Y - y_shift
    #X = X - x_shift

    sqrt2w0=_np.sqrt(2.0)/w0
    w02=w0*w0

    Fout.field  = A * hermite(m)(sqrt2w0*X)*hermite(n)(sqrt2w0*Y)*_np.exp(-(X*X+Y*Y)/w02)
    return Fout
    
def GaussLaguerre(p, l, A, w0, Fin):
    """
    Fout = GaussLaguerre(p, l, A, w0, Fin)

    :ref:`Substitutes a Laguerre-Gauss mode (beam waist) in the field. <GaussLaguerre>`

        :math:`F_{p,l}(x,y,z=0) = A \\left(\\frac{\\rho}{2}\\right)^{\\frac{|l|}{2} }L^p_l\\left(\\rho\\right)e^{-\\frac{\\rho}{2}}\\cos(l\\theta)`,
        
        with :math:`\\rho=\\frac{2(x^2+y^2)}{w_0^2}`

    Args::
        
        p, l: mode indices
        A: Amplitude
        w0: Guaussian spot size parameter in the beam waist (1/e amplitude point)
        Fin: input field
        
    Returns::
    
        Fout: output field (N x N square array of complex numbers).            
        
    Reference::
    
        A. Siegman, "Lasers", p. 642

    """

    Fout = Field.copy(Fin)
    R, Phi = Fout.mgrid_polar
    w02=w0*w0
    la=abs(l)
    rho = 2*R*R/w02
    Fout.field = A * rho**(la/2) * genlaguerre(p,la)(rho) * _np.exp(-rho/2) * _np.cos(l*Phi)
    return Fout


def IntAttenuator(att, Fin):
    """
    Fout = IntAttenuator(att, Fin)
    
    :ref:`Attenuates the intensity of the field. <IntAttenuator>`
        
        :math:`F_{out}(x,y)=\\sqrt{att}F_{in}(x,y)`
        
    Args::
    
        att: intensity attenuation factor
        Fin: input field
        
    Returns::
    
        Fout: output field (N x N square array of complex numbers).
   
    """
    Efactor = _np.sqrt(att) #att. given as intensity
    Fout = Field.copy(Fin)
    Fout.field *= Efactor
    return Fout

def Intensity(flag, Fin):
    """
    I=Intensity(flag,Fin)
    
    :ref:`Calculates the intensity of the field. <Intensity>`
    
    :math:`I(x,y)=F_{in}(x,y).F_{in}(x,y)^*`
    
    Args::
    
        flag: 0= no normalization, 1=normalized to 1, 2=normalized to 255 (for bitmaps)
        Fin: input field
        
    Returns::
    
        I: intensity distribution (N x N square array of doubles)

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

def Interpol(new_size, new_N, x_shift, y_shift, angle, magnif, Fin):
    """
    Fout = Interpol(NewSize, NewN, x_shift, y_shift, angle, magnif, Fin)
    
    :ref:`Interpolates the field to a new grid size, grid dimension. <Interpol>`
    
    Args::
    
        NewSize: the new grid size
        NewN: the new grid dimension
        x_shift, y_shift: shift of the field
        angle: rotation of the field in degrees
        magnif: magnification of the field amplitude
        Fin: input field
        
    Returns::
        
        Fout: output field (Nnew x Nnew square array of complex numbers).
  
    """

    Fout = Field.begin(new_size, Fin.lam, new_N)
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
    return Fout

def MultIntensity(Intens, Fin):
    """
    Fout = MultIntensity(Intens, Fin)

    :ref:`Multiplies the field with a given intensity distribution. <MultIntensity>`
        
    Args::
        
        Intens: N x N square array of real numbers or scalar
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    if not _np.isscalar(Intens):
        if Intens.shape != Fin.field.shape:
            raise ValueError('Intensity pattern shape does not match field size')
    Fout = Field.copy(Fin)
    Efield = _np.sqrt(Intens)
    Fout.field *= Efield
    return Fout


def MultPhase(Phi, Fin):
    """
    Fout = MultPhase(Phase, Fin)

    :ref:`Multiplies the field with a given phase distribution. <MultPhase>`
        
    Args::
        
        Phase: N x N square array of real numbers or scalar
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    if not _np.isscalar(Phi):
        if Phi.shape != Fin.field.shape:
            raise ValueError('Phase pattern shape does not match field size')
    Fout = Field.copy(Fin)
    Fout.field *= _np.exp(1j*Phi)
    return Fout


def Normal(Fin):
    """
    Fout = Normal(Fin)

    :ref:`Normalizes the field using beam power. <Normal>`
    
        :math:`F_{out}(x,y)= \\frac{F_{in}(x,y)}{\\sqrt{P}}`
        
        with
        
        :math:`P=\\int\\int\\abs{F_{in}(x,y)\\right}^2 dx dy`
    
    Args::
        
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
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
    Phi=Phase(Fin)
    
    :ref:`Calculates the phase of the field. <Phase>`
    
    
    Args::
    
        Fin: input field
        unwrap: Call PhaseUnwarp on the extracted Phase, Default is False
        units: 'opd': returned in [meters] of optical path length
                'lam': returned in multiples of lambda
                'rad': returned in multiples of 2pi phase jumps (default)
        blank_eps: [fraction] of max. Intensity at which to blank the phase
            and replace the value with numpy.nan (e.g. 1e-3==0.1%)
            Set to 0 or None to disable
        
    Returns::
    
        Phi: phase distribution (N x N square array of doubles)

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

def PhaseSpiral(Fin, **kwargs):
    """ 
    Fout = PhaseSpiral(Fin, m=1)
    Multiplies Fin with a spiral phase distribution.
    
    Args::
    
        required:
        Fin: input field

        optional:
        m = 1: order of the spiral.
    """
    Fout = Field.copy(Fin)
    m = kwargs.get('m',1)   
    R, Phi = Fout.mgrid_polar  
    Fout.field *= _np.exp(1j * m * Phi)
    return Fout

def PhaseUnwrap(Phi):
    """
    PhiOut=PhaseUnwrap(PhiIn)
    
    :ref:`Unwraps (removes jumps of pi radians) the phase. <PhaseUnwrap>`
    
    
    Args::
    
        PhiIn: input phase distribution
        
    Returns::
    
        PhiOut: unwrapped phase distribution (N x N square array of doubles)

    """
    PhiU = _unwrap_phase(Phi)
    return PhiU


def Power(Fin):
    """
    P = Power(Fin)

    :ref:`Calculates the total power. <Power>`
        
    Args::
        
        Fin: input field
        
    Returns::
        
        P: output power (real number).
  
    """
    #TODO why does Normal() also sum dx**2 (==integral) while this does not??
    I = _np.abs(Fin.field)**2
    return I.sum()


def RandomIntensity(seed, noise, Fin):
    """
    Fout = RandomIntensity(seed, noise, Fin)

    :ref:`Adds random intensity to the field <RandomIntensity>`
        
    Args::
        
        seed: seed number for the random noise generator
        noise: level of the noise
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    #TODO implementation error in original LP: field error, not I error!
    # need to sqrt for that
    Fout = Field.copy(Fin)
    _np.random.seed(int(seed))
    N = Fout.N
    ranint = _np.random.rand(N, N)*noise
    Fout.field += ranint
    return Fout

def RandomPhase(seed, maxPhase, Fin):
    """
    Fout = RandomPhase(seed, maxPhase, Fin)

    :ref:`Adds random phase to the field <RandomPhase>`
        
    Args::
        
        seed: seed number for the random noise generator
        maxPhase: maximum phase in radians
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    #2020023 - ldo - tested similar result as Cpp version, although not 
    # 1:1 since seed is different in numpy
    Fout = Field.copy(Fin)
    _np.random.seed(int(seed))
    N = Fout.N
    ranphase = (_np.random.rand(N, N)-0.5)*maxPhase
    Fout.field *= _np.exp(1j * ranphase)
    return Fout


def RectAperture(sx, sy, x_shift, y_shift, angle, Fin):
    """
    Fout = RectAperture(w, h, x_shift, y_shift, angle, Fin)
    
    :ref:`Propagates the field through a rectangular aperture. <RectAperture>`

    Args::
    
        w: width of the aperture
        h: height of the aperture
        x_shift, y_shift: shift from the center
        angle: rotation angle in degrees 
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).

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
    return Fout


def RectScreen(sx, sy, x_shift, y_shift, angle, Fin):
    """
    Fout = RectScreen(w, h, x_shift, y_shift, angle, Fin)
    
    :ref:`Diffracts the field by a rectangular screen. <RectScreen>`

    Args::
    
        w: width of the screen
        h: height of the screen
        x_shift, y_shift: shift from the center
        angle: rotation angle in degrees 
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).

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
    return Fout


def Strehl(Fin):
    """
    S = Strehl( Fin)

    :ref:`Calculates the Strehl value of the field <Strehl>`
        
    Args::
        
        Fin: input field
        
    Returns::
        
        S: Strehl value (real number).
  
    """
    normsq = _np.abs(Fin.field).sum()**2
    if normsq == 0.0:
        raise ValueError('Error in Strehl: Zero beam power')
    strehl = _np.real(Fin.field).sum()**2 + _np.imag(Fin.field).sum()**2
    strehl = strehl/normsq
    return strehl

def SubIntensity(Intens, Fin):
    """
    Fout = SubIntensity(Intens, Fin)

    :ref:`Substitutes  a given intensity distribution in the field with. <SubIntensity>`
        
    Args::
        
        Intens: N x N square array of real numbers >= 0
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    Fout = Field.copy(Fin)
    Intens = _np.asarray(Intens)
    if Intens.shape != Fout.field.shape:
        raise ValueError('Intensity map has wrong shape')
    phi = _np.angle(Fout.field)
    Efield = _np.sqrt(Intens)
    Fout.field = Efield * _np.exp(1j * phi)
    return Fout

def SubPhase(Phi, Fin):
    """
    Fout = SubPhase(Phi, Fin)

    :ref:`Substitutes  a given phase distribution in the field with. <SubPhase>`
        
    Args::
        
        Phase: N x N square array of real numbers
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    Fout = Field.copy(Fin)
    Phi = _np.asarray(Phi)
    if Phi.shape != Fin.field.shape:
        raise ValueError('Phase map has wrong shape')
    oldabs = _np.abs(Fout.field)
    Fout.field = oldabs * _np.exp(1j * Phi)
    return Fout


