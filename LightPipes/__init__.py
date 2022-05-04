__all__ = [
    'ABCD',
    'AiryBeam1D',
    'AiryBeam2D',
    'Axicon',
    'BeamMix',
    'Begin',
    'Centroid',
    'CircAperture',
    'CircScreen',
    'Convert',
    'D4sigma', 
    'Forward',
    'Forvard',
    'Fresnel',
    'Gain',
    'GaussAperture',
    'GaussBeam',
    'GForvard',
    'GaussScreen',
    'GaussHermite',
    'GaussLaguerre',
    'GLens',
    'IntAttenuator',
    'Intensity',
    'Interpol',
    'Lens',
    'LensForvard',
    'LensFresnel',
    'MultIntensity',
    'MultPhase',
    'Normal',
    'Phase',
    'PhaseSpiral',
    'PhaseUnwrap',
    'PipFFT',
    'PlaneWave',
    'PointSource',
    'Power',
    'Propagate',
    'RandomIntensity',
    'RandomPhase',
    'RectAperture',
    'RectScreen',
    'Steps',
    'Strehl',
    'SubIntensity',
    'SubPhase',
    'SuperGaussAperture',
    'Tilt',
    'Zernike',
    'noll_to_zern',
    'ZernikeName',
    'ZernikeFit',
    'ZernikeFilter',
    'LPtest',
    'LPhelp',
    'LPdemo',
    
]

#User defined functions from userfunc.py:
__all__.extend([
    'FieldArray2D',
    'RowOfFields',
    'CylindricalLens',
    'ZonePlate',
    ])

__all__.sort()

#physical units like m, mm, rad, deg, ...
from .units import * 

from ._version import __version__
LPversion=__version__

__all__.extend([
    'm', 'cm', 'mm', 'um', 'nm',
    'rad', 'mrad', 'urad', 'deg', 'W', 'mW', 'LPversion', 
    'PI'
])

# avoid modified
__all__ = tuple(__all__)

import functools
import numpy as np
import webbrowser

from .field import Field
from .propagators import ABCD, Fresnel, Forward, Forvard, GForvard, Propagate, Steps
from .lenses import Axicon, Lens, GLens, LensFarfield, LensForvard, LensFresnel, \
    Convert
from .zernike import ZernikeName, ZernikeNolltoMN, noll_to_zern, \
    ZernikeFilter, ZernikeFit, Zernike
from .core import CircAperture, CircScreen, RectAperture, RectScreen
from .core import GaussAperture, GaussScreen, GaussHermite, GaussLaguerre, SuperGaussAperture
from .core import Intensity, Phase, PhaseUnwrap, PhaseSpiral
from .core import RandomIntensity, RandomPhase
from .core import Strehl, Centroid, D4sigma
from .core import SubIntensity, SubPhase
from .core import BeamMix
from .core import MultIntensity, MultPhase
from .core import Normal, Power
from .core import IntAttenuator
from .misc import Tilt, Gain, PipFFT
from .core import Interpol
from .sources import AiryBeam1D, AiryBeam2D, PointSource, GaussBeam, PlaneWave
from .userfunc import ZonePlate, CylindricalLens, RowOfFields, FieldArray2D

def Begin(size,labda,N,dtype=None):
    """
    *Initiates a field with a grid size, a wavelength and a grid dimension.
    By setting dtype to numpy.complex64 memory can be saved.
    If dtype is not set (default = None), complex (equivalent to numpy.complex128) will be used for the field array.*
    
    :param size: size of the square grid
    :type size: int, float
    :param labda: the wavelength of the output field
    :type labda: int, float
    :param N: the grid dimension
    :type N: int
    :param dtype: type of the field array
    :type dtype: complex, numpy.complex64, numpy.complex128 (default = None)
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> from LightPipes import *
    >>> size = 20*mm
    >>> wavelength = 500*nm
    >>> N = 5
    >>> F = Begin(size, wavelength, N)
    >>> F
    <LightPipes.field.Field object at 0x0000027AAF6E5908>
    >>> F.field
    array([[1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j],
           [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j],
           [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j],
           [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j],
           [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j]])
    >>> F.siz
    0.02
    >>> F.lam
    5.000000000000001e-07
    >>> F.N
    5
    
    .. seealso::
    
        * :ref:`Manual: Starting the calculations. <Starting the calculations.>`
        
        * :ref:`Examples: Diffraction from a circular aperture <Diffraction from a circular aperture.>`
    """

    Fout = Field.begin(size, labda, N, dtype) #returns Field class with all params
    return Fout

def LPtest():
    """
    *Performs a test to check if the installation of the LightPipes package was successful.*
    
    :return: "LightPipes for Python: test passed." if successful, "Test failed" if not.
    :rtype: string
    
    """
    import math
    F=Begin(1.8,2.5,55)
    F=Fresnel(10,F)
    I=Intensity(0,F)
    S=np.sum(I)
    Sa=16.893173606654138
    if math.isclose(S, Sa):
        print('LightPipes for Python: test passed.')
        print("LightPipes version:",LPversion)
    else:
        print('Test failed')

def LPhelp():
    """
    *Go to the LightPipes documentation website on:* `https://opticspy.github.io/lightpipes/ <https://opticspy.github.io/lightpipes/>`_

    """
    webbrowser.open_new("https://opticspy.github.io/lightpipes/")

def LPdemo():
    """
    *Demonstrates the simulation of a two-holes interferometer.*
    
    :return: A plot of the interference pattern and a listing of the Python script.
    :rtype: `matplotlib.image.AxesImage`
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

