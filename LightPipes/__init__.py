# fix: https://github.com/matthew-brett/delocate/issues/15
from ._LightPipes import *  # noqa

__all__ = [
    'Axicon',
    'BeamMix',
    'Begin',
    'CircAperture',
    'CircScreen',
    'Convert',
    'Forvard',
    'Fresnel',
    'Gain',
    'GaussAperture',
    'GaussScreen',
    'GaussHermite',
    'GaussLaguerre',
    'IntAttenuator',
    'Lens',
    'LensForvard',
    'LensFresnel',
    'MultIntensity',
    'MultPhase',
    'Normal',
    'Intensity',
    'Interpol',
    'Phase',
    'PhaseUnwrap',
    'PipFFT',
    'Power',
    'RandomIntensity',
    'RandomPhase',
    'RectAperture',
    'RectScreen',
    'Steps',
    'Strehl',
    'SubIntensity',
    'SubPhase',
    'Tilt',
    'Zernike',
    'getGridSize',
    'setGridSize',
    'getWavelength',
    'setWavelength',
    'getGridDimension',
]

LP = Init() # noqa
for name in __all__:
    locals[name] = getattr(LP, name)


# define some units
m = 1.0
cm = 1e-2*m
mm = 1e-3*m
um = 1e-6*m
nm = 1e-9*m
rad = 1.0
mrad = 1e-3*rad
W = 1.0
mW = 1e-3*W

__all__.extend([
    'm', 'cm', 'mm', 'um', 'nm',
    'rad', 'mrad', 'W', 'mW',
])

# avoid modified
__all__ = tuple(__all__)
