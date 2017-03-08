# fix: https://github.com/matthew-brett/delocate/issues/15
from ._LightPipes import * # noqa
from ._version import __version__

LPversion=_version.__version__

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

LP = _LightPipes.Init()
Axicon = LP.Axicon
BeamMix = LP.BeamMix
Begin = LP.Begin
CircAperture = LP.CircAperture
CircScreen = LP.CircScreen
Convert = LP.Convert
Forvard = LP.Forvard
Fresnel = LP.Fresnel
Gain = LP.Gain
GaussAperture = LP.GaussAperture
GaussScreen = LP.GaussScreen
GaussHermite = LP.GaussHermite
GaussLaguerre = LP.GaussLaguerre
IntAttenuator = LP.IntAttenuator
Lens = LP.Lens
LensForvard = LP.LensForvard
LensFresnel = LP.LensFresnel
MultIntensity = LP.MultIntensity
MultPhase = LP.MultPhase
Normal = LP.Normal
Intensity = LP.Intensity
Interpol = LP.Interpol
Phase = LP.Phase
PhaseUnwrap = LP.PhaseUnwrap
PipFFT = LP.PipFFT
Power = LP.Power
RandomIntensity = LP.RandomIntensity
RandomPhase = LP.RandomPhase
RectAperture = LP.RectAperture
RectScreen = LP.RectScreen
Steps = LP.Steps
Strehl = LP.Strehl
SubIntensity = LP.SubIntensity
SubPhase = LP.SubPhase
Tilt = LP.Tilt
Zernike = LP.Zernike
noll_to_zern=LP.noll_to_zern
ZernikeName=LP.ZernikeName
ZernikeNolltoMN=LP.ZernikeNolltoMN
LPtest = LP.LPtest
LPhelp = LP.LPhelp
LPDoc = LP.LPhelp
LPweb = LP.LPhelp
getGridSize = LP.getGridSize
setGridSize = LP.setGridSize
getWavelength = LP.getWavelength
setWavelength = LP.setWavelength
getGridDimension = LP.getGridDimension


