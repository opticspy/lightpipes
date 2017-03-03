# fix: https://github.com/matthew-brett/delocate/issues/15
from ._LightPipes import *  # noqa

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

LP=_LightPipes.Init()
def Axicon(phi, n1, x_shift, y_shift, F):
    return LP.Axicon(phi, n1, x_shift, y_shift, F)
def BeamMix(F1,F2):
    return LP.BeamMix(F1,F2)
def Begin(size, wavelength, N):
    return LP.Begin(size, wavelength ,N)
def CircAperture(R, x_shift, y_shift, F):
    return LP.CircAperture(R, x_shift, y_shift, F)
def CircScreen(R, x_shift, y_shift, F):
    return LP.CircScreen(R, x_shift, y_shift, F)
def Convert(F):
    return LP.Convert(F)
def Forvard(z, F):
    return LP.Forvard(z, F)
def Fresnel(z, F):
    return LP.Fresnel(z, F)
def Gain(Isat, alpha0, Lgain, F):
    return LP.Gain(Isat, alpha0, Lgain, F)
def GaussAperture(w, x_shift, y_shift, T, F):
    return LP.GaussAperture(w, x_shift, y_shift, T, F)
def GaussScreen(w, x_shift, y_shift, T, F):
    return LP.GaussScreen(w, x_shift, y_shift, T, F)
def GaussHermite(m, n, A, w0, F):
    return LP.GaussHermite(m, n, A, w0, F)
def GaussLaguerre(p, m, A, w0, F):
    return LP.GaussLaguerre(p, m, A, w0, F)
def IntAttenuator(att, F):
    return LP.IntAttenuator(att, F)
def Lens(f, x_shift, y_shift, F):
    return LP.Lens(f, x_shift, y_shift, F)
def LensForvard(f, z, F):
    return LP.LensForvard(f, z, F)
def LensFresnel(f, z, F):
    return LP.LensFresnel(f, z, F)
def MultIntensity(Intens, F):
    return LP.MultIntensity(Intens, F)
def MultPhase(Phase, F):
    return LP.MultPhase(Phase, F)
def Normal(F):
    return LP.Normal(F)
def Intensity(flag,F):
    return LP.Intensity(flag,F)
def Interpol(new_size, new_number, x_shift, y_shift, angle, magnif, F):
    return LP.Interpol(new_size, new_number, x_shift, y_shift, angle, magnif, F)
def Phase(F):
    return LP.Phase(F)
def PhaseUnwrap(Phi):
    return LP.PhaseUnwrap(Phi)
def PipFFT(index, F):
    return LP.PipFFT(index, F)
def Power(F):
    return LP.Power(F)
def RandomIntensity(seed, noise, F):
    return LP.RandomIntensity(seed, noise, F)
def RandomPhase(seed, maxPhase, F):
    return LP.RandomPhase(seed, maxPhase, F)
def RectAperture(sx, sy, x_shift, y_shift, angle, F):
    return LP.RectAperture(sx, sy, x_shift, y_shift, angle, F)
def RectScreen(sx, sy, x_shift, y_shift, angle, F):
    return LP.RectScreen(sx, sy, x_shift, y_shift, angle, F)
def Steps(z, nstep, refr, F):
    return LP.Steps(z, nstep, refr, F)
def Strehl(F):
    return LP.Strehl(F)
def SubIntensity(Intens, F):
    return LP.SubIntensity(Intens, F)
def SubPhase(Phase, F):
    return LP.SubPhase(Phase, F)
def Tilt(tx, ty, F):
    return LP.Tilt(tx, ty, F)
def Zernike(n, m, R, A, F):
    return LP.Zernike(n, m, R, A, F)
def version():
    return LP.version()
def help():
    return LP.help()
def getGridSize():
    return LP.getGridSize()
def setGridSize(newSize):
    return LP.setGridSize(newSize)
def getWavelength():
    return LP.getWavelength()
def setWavelength(newWavelength):
    return LP.setWavelength(newWavelength)
def getGridDimension():
    return LP.getGridDimension()


