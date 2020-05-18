__all__ = [
    'Axicon',
    'BeamMix',
    'Begin',
    'CircAperture',
    'CircScreen',
    'Convert',
    'Forward',
    'Forvard',
    'Fresnel',
    'Gain',
    'GaussAperture',
    'GaussBeam',
    'GaussScreen',
    'GaussHermite',
    'GaussLaguerre',
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
    # 'getGridSize',
    # 'setGridSize',
    # 'getWavelength',
    # 'setWavelength',
    # 'getGridDimension',
    'LPtest',
    'LPhelp',
    'LPdemo',
]

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
from .propagators import Fresnel, Forward, Forvard, Steps
from .lenses import Axicon, Lens, LensFarfield, LensForvard, LensFresnel, \
    Convert
from .zernike import ZernikeName, ZernikeNolltoMN, noll_to_zern, \
    ZernikeFilter, ZernikeFit, Zernike
from .core import CircAperture, CircScreen, RectAperture, RectScreen
from .core import GaussAperture, GaussScreen, GaussHermite, GaussLaguerre, SuperGaussAperture
from .core import Intensity, Phase, PhaseUnwrap, PhaseSpiral
from .core import RandomIntensity, RandomPhase
from .core import Strehl
from .core import SubIntensity, SubPhase
from .core import BeamMix
from .core import MultIntensity, MultPhase
from .core import Normal, Power
from .core import IntAttenuator
from .misc import Tilt, Gain, PipFFT
from .core import Interpol
from .sources import PointSource, GaussBeam, PlaneWave


# def _apply_vals_to_LP(Fin):
    # """Apply the values stored in Field to LP instance.
    # Use this before calling any LP function."""
    # _LP.internal_setN(Fin.N)
    # _LP.setGridSize(Fin.siz)
    # _LP.setWavelength(Fin.lam)
    # _LP.internal_setInt1(Fin._int1)
    # _LP.internal_setDoub1(Fin._curvature)

# def _field_vals_from_LP(Fout):
    # """Apply (in-place!) the global values stored in
    # LP to the field Fout."""
    # if Fout.N != _LP.getGridDimension():
        # raise ValueError('Field size does not match LP global params')
    # Fout.siz = _LP.getGridSize()
    # Fout.lam = _LP.getWavelength()
    # Fout._int1 = _LP.internal_getInt1()
    # Fout._curvature = _LP.internal_getDoub1()
    

# def accept_new_field(fn):
    # """Decorator to wrap existint LP functions to accept new style
    # Field object with numpy field.
    # """
    # @functools.wraps(fn)
    # def fn_wrapper(*args, **kwargs):
        # if 'Fin' in kwargs:
            # raise NotImplementedError(
                # 'accept_new_field decorator: Fin must not be keyword arg')
        # Fin = args[-1] #all LP functions have Fin as last arg
        # args = args[:-1] #strip last arg
        # Fout = Field.copy(Fin)
        # ll_in = Fout.field.T.tolist() #transpose since numpy convention
        # # is [y,x] and LP functions mostly assume [x,y] with some exceptions
        # args = list(args) #make mutable
        # args.append(ll_in)
        # # args = tuple(args) #back to standard
        
        # _apply_vals_to_LP(Fout)
        
        # ll_out = fn(*args, **kwargs)
        
        # Fout.field = np.asarray(ll_out).T #undo transpose, see above
        # _field_vals_from_LP(Fout)
        
        # return Fout
    
    # return fn_wrapper
        

def Begin(size,labda,N):
    """
    F = Begin(GridSize, Wavelength, N)
    
    :ref:`Creates a plane wave (phase = 0.0, amplitude = 1.0). <Begin>`

    Args::
    
        GridSize: size of the grid
        Wavelength: wavelength of the field
        N: N x N grid points (N must be even)
        
    Returns::
     
        F: N x N square array of complex numbers (1+0j).
            
    Example:
    
    :ref:`Diffraction from a circular aperture <Diffraction>`
    
    """
    # return _LP.Begin(size, labda, N) #returns list of list
    Fout = Field.begin(size, labda, N) #returns Field class with all params
    #_apply_vals_to_LP(Fout) #apply global params to keep consistency
    return Fout


# @accept_new_field
# def StepsOLD(z, nstep, refr, Fin):
    # """
    # Fout = Steps(z, nstep, refr, Fin)
                 
    # :ref:`Propagates the field a distance, nstep x z, in nstep steps in a
    # medium with a complex refractive index stored in the
    # square array refr. <Steps>`

    # Args::
    
        # z: propagation distance per step
        # nstep: number of steps
        # refr: refractive index (N x N array of complex numbers)
        # Fin: input field
        
    # Returns::
      
        # Fout: ouput field (N x N square array of complex numbers).
        
    # Example:
    
    # :ref:`Propagation through a lens like medium <lenslikemedium>`
    
    # """
    # return _LP.Steps(z, nstep, refr, Fin)


def LPtest():
    """
    Performs a test to check if the installation of the LightPipes package was successful.
    
    Args::
    
        -
        
    Returns::
    
        "LightPipes for Python: test passed." if successful,
        "Test failed" if not.

    """
    Fa=[]
    F=Begin(1,2,4)
    F=Fresnel(10,F)
    f_ll = F.field.T.tolist() #transpose to make f_ll[x,y] not [y,x]
    for i in range(0, 4):
        for j in range(0, 4):
            Fa.append('({0.real:2.7f} + {0.imag:2.7f}i)'.format(f_ll[i][j]))
    Faa=[
    '(0.0004345 + -0.0195239i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0004345 + -0.0195239i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0008946 + -0.0382658i)',
    '(0.0008946 + -0.0382658i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0008946 + -0.0382658i)',
    '(0.0008946 + -0.0382658i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0004345 + -0.0195239i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0006237 + -0.0273331i)',
    '(0.0004345 + -0.0195239i)'
    ]
    if Fa==Faa:
        ret = _LP.test()
        if ret==1:
            print('Test OK')
    else:
        print('Test failed')

def LPhelp():
    """
    Go to the LightPipes documentation website on:
    
    https://opticspy.github.io/lightpipes/

    """
    webbrowser.open_new("https://opticspy.github.io/lightpipes/")

# def getGridSize():
    # """
    # size_grid = getGridSize()
    
    # Returns the value of the size of the grid in meters.
    
    # Args::
        
        # -
        
    # Returns::
    
        # size_grid: Size of the grid (real number).

    # """
    # return _LP.getGridSize()

# def setGridSize(newSize):
    # """
    # setGridSize(newGridSize)
    
    # Changes the value of the grid size.
    
    # Args::
    
        # newGridSize: New size of the grid.
        
    # Returns::
    
        # -

    # """
    # # _LP.setGridSize(newSize)
    # raise NotImplementedError('Deprecated! use Field.size on object, not lib.')

# def getWavelength():
    # """
    # wavelength = getWavelength()
    
    # Returns the value of the wavelength in meters.
    
    # Args::
    
        # -
        
    # Returns::
    
        # wavelength: Value of the wavelength (real number).

    # """
    # return _LP.getWavelength()

# def setWavelength(newWavelength):
    # """
    # setWavelength(newWavelength)
    
    # Changes the value of the wavelength.
    
    # Args::
    
        # newWavelength: New value of the wavelength.
        
    # Returns::
    
        # -

    # """ 
    # # _LP.setWavelength(newWavelength)
    # raise NotImplementedError('Deprecated! use Field.lam on object, not lib.')

# def getGridDimension():
    # """
    # grid-dimension = getGridDimension()
    
    # Returns the value of the grid dimension.
    # The grid dimension cannot be set. Use: :ref:`Interpol. <Interpol>`
    
    # Args::
    
        # -
        
    # Returns::
    
        # grid-dimension: Value of the dimension of the grid (integer).

    # """
    # return _LP.getGridDimension()


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

