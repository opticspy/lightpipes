# -*- coding: utf-8 -*-

import numpy as _np

from .field import Field

PI=_np.pi

def Gain(Isat, alpha0, Lgain, Fin):
    """
    Fout = Gain(Isat, alpha0, Lgain, Fin)

    :ref:`Propagates the field through a thin saturable gain sheet. <Gain>`
        
        :math:`F_{out}(x,y) = F_{in}(x,y) e^{\\alpha L_{gain}}`, with
        :math:`\\alpha = \\dfrac{\\alpha_0}{1 + {2 I(x,y)}/{I_{sat}}}`.
         
        :math:`2\\alpha L_{gain}` is the net round-trip intensity gain. 
        :math:`\\alpha_0` is the small-signal intensity gain and 
        :math:`I_{sat}` is the saturation intensity of the gain medium 
        with a length :math:`L_{gain}`.
        
        The intensity must be doubled because of the left- and right 
        propagating fields in a normal resonator. (If only one field is propagating in one direction (ring 
        laser) you should double :math:`I_{sat}` as well to remove the factor 2 in the denominator).

        The gain sheet should be at one of the mirrors of a (un)stable laser resonator.
        
        See: Rensch and Chester (1973).
        
    Args::
    
        Isat: saturation intensity
        alpha0: small signal gain
        Lgain: length of the gain sheet
        Fin: input field
        
    Returns::
     
        Fout: output field (N x N square array of complex numbers).

    Example:
    
    :ref:`Unstable resonator <Unstab>`

    """
    Fout = Field.copy(Fin)
    Ii = _np.abs(Fout.field)**2
    """direct port from Cpp:
    if Isat == 0.0:
        Io = Ii
    else:
        Io = Ii * _np.exp(alpha0*Lgain/(1+2*Ii/Isat))
    ampl = _np.sqrt(Io/Ii)
    ampl[Ii==0.0] = 0.0 #replace nan from 0-division
    Fout.field *= ampl
    
    However this can be simplified since multiplying and dividing by Ii
    is redundant and once removed the div by zero is gone, too.
    And if Isat==0.0, Io/Ii=1 everywhere -> gain=1, just skip.
    Finally, sqrt can be put in exp() as 1/2
    """
    if Isat == 0.0:
        ampl = 1
    else:
        ampl = _np.exp(1/2*alpha0*Lgain/(1+2*Ii/Isat))
    Fout.field *= ampl
    return Fout


def PipFFT(index, Fin):
    """
    Fout = PipFFT(index, Fin)

    :ref:`Performs a 2D Fourier transform of the field. <PipFFT>`
        
    Args::
        
        index: +1 = forward transform, -1 = back transform
        Fin: input field
        
    Returns::
        
        Fout: output field (N x N square array of complex numbers).
  
    """
    Fout = Field.copy(Fin)
    legacy = False
    if legacy:
        """Tested to give same results as Cpp version.
        However, viewing the Phase and Intensity in the FFT-plane,
        it seems the phase is wrong (high-frequency jumps).
        The output with ifftshift() correctly applied (see below) seems
        like a flatter phase and probably physically more accurate.
        The multiplication might just be a little faster than the shift/roll
        of the entire array in large-array cases, so keep this code for
        reference:
        """
        ii = _np.ones(Fout.N, dtype=float)
        ii[1::2] = -1
        iiij = _np.outer(ii, ii)
        Fout._int1 += index
        if Fout._int1 != 0:
            Fout.field *= iiij #effectively doing fftshift
        if index==1:
            Fout.field = _np.fft.fft2(Fout.field)
        elif index==-1:
            Fout.field = _np.fft.ifft2(Fout.field)
        else:
            raise ValueError(
                'FFT direction index must be 1 or -1, got {}'.format(index))
        if Fout._int1 == 0:
            Fout.field *= iiij
    else:
        """Very useful comment on fftshift and ifftshift found in 
        https://github.com/numpy/numpy/issues/13442
        with x=real and X=fourier space:
            x = ifft(fft(x))
            X = fft(ifft(X))
        and both 0-centered in middle of array:
        ->
        X = fftshift(fft(ifftshift(x)))  # correct magnitude and phase
        x = fftshift(ifft(ifftshift(X)))  # correct magnitude and phase
        X = fftshift(fft(x))  # correct magnitude but wrong phase !
        x = fftshift(ifft(X))  # correct magnitude but wrong phase !
        """
        if index==1:
            Fout.field = _np.fft.fftshift(
                _np.fft.fft2(_np.fft.ifftshift(Fout.field)))
        elif index==-1:
            Fout.field = _np.fft.fftshift(
                _np.fft.ifft2(_np.fft.ifftshift(Fout.field)))
        else:
            raise ValueError(
                'FFT direction index must be 1 or -1, got {}'.format(index))
    return Fout


def Tilt(tx, ty, Fin):
    """
    Fout = Tilt(tx, ty, Fin)

    :ref:`Tilts the field. <Tilt>`

    Args::
    
        tx, ty: tilt in radians
        Fin: input field
        
    Returns::
    
        Fout: output field (N x N square array of complex numbers).

    """

    Fout = Field.copy(Fin)
    yy, xx = Fout.mgrid_cartesian
    k = 2*_np.pi/Fout.lam
    fi = -k*(tx*xx + ty*yy)
    Fout.field *= _np.exp(1j * fi)
    return Fout

def LPdemo():
    """
    LPdemo()
    Demonstrates the simulation of a two-holes interferometer.
    
    Args::
    
         -
    
    Returns::
    
        A plot of the interference pattern and a listing of the Python script.
    
    """
    import matplotlib.pyplot as plt
    import sys
    import platform
    m=1
    mm=1e-3*m
    cm=1e-2*m
    um=1e-6*m
    wavelength=20*um
    size=30.0*mm
    N=500
    F=Begin(size,wavelength,N)
    F1=CircAperture(0.15*mm, -0.6*mm,0, F)
    F2=CircAperture(0.15*mm, 0.6*mm,0, F)    
    F=BeamMix(F1,F2)
    F=Fresnel(10*cm,F)
    I=Intensity(0,F)
    #plt.contourf(I,50); plt.axis('equal')
    fig=plt.figure()
    fig.canvas.set_window_title('Interference pattern of a two holes interferometer') 
    plt.imshow(I,cmap='rainbow');plt.axis('off')
    print(
        '\n\nLightPipes for Python demo\n\n'
        'Python script of a two-holes interferometer:\n\n'
        '   import matplotlib.pyplot as plt\n'
        '   from LightPipes import *\n'
        '   wavelength=20*um\n'
        '   size=30.0*mm\n'
        '   N=500\n'
        '   F=Begin(size,wavelength,N)\n'
        '   F1=CircAperture(0.15*mm, -0.6*mm,0, F)\n'
        '   F2=CircAperture(0.15*mm, 0.6*mm,0, F)\n'
        '   F=BeamMix(F1,F2)\n'
        '   F=Fresnel(10*cm,F)\n'
        '   I=Intensity(0,F)\n'
        '   fig=plt.figure()\n'
        '   fig.canvas.set_window_title(\'Interference pattern of a two holes interferometer\')\n'
        '   plt.imshow(I,cmap=\'rainbow\');plt.axis(\'off\')\n'
        '   plt.show()\n\n'
    )
    print('Executed with python version: ' + sys.version)
    print('on a ' + platform.system() + ' ' + platform.release() + ' ' + platform.machine() +' machine')
    plt.show()
