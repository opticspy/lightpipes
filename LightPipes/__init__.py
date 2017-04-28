# fix: https://github.com/matthew-brett/delocate/issues/15

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
    'noll_to_zern',
    'ZernikeName',
    'getGridSize',
    'setGridSize',
    'getWavelength',
    'setWavelength',
    'getGridDimension',
    'LPtest',
    'LPhelp',
]

from ._LightPipes import * # noqa
from ._version import __version__

LPversion=_version.__version__

LP = Init() # noqa
for name in __all__:
    locals()[name] = getattr(LP, name)

# define some units
m = 1.0;mm=1e-3*m; cm=1e-2*m;um=1e-6*m;nm=1e-9*m
rad=1.0;mrad=1e-3*rad
W = 1.0;mW = 1e-3*W

__all__.extend([
    'm', 'cm', 'mm', 'um', 'nm',
    'rad', 'mrad', 'W', 'mW', 'LPversion',
])

# avoid modified
__all__ = tuple(__all__)
