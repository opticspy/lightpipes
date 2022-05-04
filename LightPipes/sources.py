from .field import Field
from scipy import special
from .core import BeamMix, Phase, MultPhase, IntAttenuator, CircAperture, GaussHermite, GaussLaguerre, Interpol
from .misc import PI,Tilt, backward_compatible
import numpy as _np

def AiryBeam1D(Fin, x0 = 0.001, a = 100):
    """
    *Creates a 1D nonspreading Airy beam.*

        :math:`F(x,y,z=0) = Ai\\left(\\dfrac{x}{x_0}\\right)e^{ax}`

    :param Fin: input field
    :type Fin: Field
    :param x0: scale x (default = 1*mm)
    :type x0: int, float
    :param a: degree of apodization x (default = 0.1/mm)
    :type a: int, float

    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        import matplotlib.pyplot as plt
        import numpy as np
        
        wavelength = 2.3*um
        size = 30*mm
        N = 500
        N2=N//2
        x0=0.3*mm
        a=0.1/mm
        dz=1.25*cm
        NZ=200
        
        F0=Begin(size,wavelength,N)
        F0=AiryBeam1D(F0,x0=x0, a=a)
        Ix=np.zeros(N)
        for k in range(0,NZ):
            F=Forvard(F0,dz*k)
            I=Intensity(F)
            Ix=np.vstack([Ix,I[N2]])
        plt.figure(figsize = (12,5))
        plt.imshow(Ix,
                   extent=[-size/2/mm, size/2/mm, 0, NZ*dz/cm],
                   aspect=0.08,
                   origin='lower',
                   cmap='jet',
                   )
        plt.xlabel('x [mm]')
        plt.ylabel('z [cm]')
        s = r'LightPipes for Python' + '\\n'+ '1D Airy beam' + '\\n\\n'\\
            r'$\\lambda = {:4.2f}$'.format(wavelength/um) + r' ${\\mu}m$' + '\\n'\\
            r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\\n'\\
            r'$N = {:4d}$'.format(N) + '\\n'\\
            r'$x_0 = {:4.2f}$'.format(x0/mm) + r' $mm$' + '\\n'\\
            r'$a = $' + '{:4.2f}'.format(a*mm) + r' $/mm$' + '\\n'\\
            r'${\\copyright}$ Fred van Goor, May 2022'
        plt.text(16, 50, s, bbox={'facecolor': 'white', 'pad': 5})
        plt.show()
    
    .. plot:: ./Examples/Commands/AiryBeam1D.py
    
    ref: M. V. Berry and N. L. Balazs, “Nonspreading wave packets,” Am. J. Phys. 47, 264–267 (1979).
    """
    Fout = Field.copy(Fin)
    Y, X = Fout.mgrid_cartesian
    Fout.field = special.airy(X/x0)[0]*_np.exp(X*a)
    Fout._IsGauss=False
    return Fout

def AiryBeam2D(Fin, x0 = 0.001, y0 = 0.001, a1 = 100, a2 = 100):
    """
    *Creates a 2D nonspreading Airy beam.*

        :math:`F(x,y,z=0) = Ai\\left(\\dfrac{x}{x_0}\\right)Ai\\left(\\dfrac{y}{y_0}\\right)e^{a_1x+a_2y}`

    :param Fin: input field
    :type Fin: Field
    :param x0: scale x (default = 1*mm)
    :type x0: int, float
    :param y0: scale y (default = 1*mm)
    :type y0: int, float
    :param a1: degree of apodization x (default = 0.1/mm)
    :type a1: int, float
    :param a2: degree of apodization y (default = 0.1/mm)
    :type a2: int, float

    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        import matplotlib.pyplot as plt
        import numpy as np
        
        wavelength = 2.3*um
        size = 30*mm
        N = 500
        x0=y0=1*mm
        a1=a2=0.1/mm
        z=900*cm
        
        F0=Begin(size,wavelength,N)
        F0=AiryBeam2D(F0,x0=x0, y0=y0, a1=a1, a2=a2)
        F=Fresnel(F0,z)
        I=Intensity(F)
        plt.figure(figsize = (9,5))
        plt.imshow(I,
                   extent=[-size/2/mm, size/2/mm, -size/2/mm, size/2/mm],
                   origin='lower',
                   cmap='jet',
                   )
        plt.title('2D Airy beam')
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        s = r'LightPipes for Python' + '\\n'+ '2D Airy beam' + '\\n\\n'\\
            r'$\\lambda = {:4.2f}$'.format(wavelength/um) + r' ${\\mu}m$' + '\\n'\\
            r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\\n'\\
            r'$N = {:4d}$'.format(N) + '\\n'\\
            r'$x_0 = y_0 = {:4.2f}$'.format(x0/mm) + r' $mm$' + '\\n'\\
            r'$a1 = a2 =  $' + '{:4.2f}'.format(a1*mm) + r' $/mm$' + '\\n'\\
            r'$z = $' + '{:4.2f}'.format(z/cm) + r' $cm$' + '\\n'\\
            r'${\\copyright}$ Fred van Goor, May 2022'
        plt.text(16, -10, s, bbox={'facecolor': 'white', 'pad': 5})
        plt.show()
    
    .. plot:: ./Examples/Commands/AiryBeam2D.py
    
    ref: M. V. Berry and N. L. Balazs, “Nonspreading wave packets,” Am. J. Phys. 47, 264–267 (1979).
    
    .. seealso::
        
        * :ref:`Examples: Non-diffracting Airy beams<Generation of a 2-dimensional Airy beam from a Gaussian laser beam.>`
    """
    Fout = Field.copy(Fin)
    Y, X = Fout.mgrid_cartesian
    Fout.field = special.airy(X/x0)[0]*special.airy(Y/y0)[0]*_np.exp(X*a1)*_np.exp(Y*a2)
    Fout._IsGauss=False
    return Fout

@backward_compatible
def PointSource(Fin, x=0.0, y=0.0):
    """
    *Creates a point source.*

    :param Fin: input field
    :type Fin: Field
    :param x: x-position of the point source (default = 0.0)
    :type x: int, float
    :param y: y-position of the point source (default = 0.0)
    :type y: int, float    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = PointSource(F) # point source at center of the grid
    >>> F = PointSource(F, x = 5*mm) # point source at x=5mm, y=0.0
    >>> F = PointSource(F, 5*mm, 0.0) # Idem
    """
    Fout = Field.copy(Fin)
    if abs(x) >= Fin.siz/2 or abs(y) >= Fin.siz/2:
        raise ValueError(
        'error in PointSource: x and y must be inside grid size, between: {:4.4f} and {:4.4f}, got: x = {:4.4f}, y = {:4.4f}'.format(-Fin.siz/2,Fin.siz/2,x,y))
    Fout=IntAttenuator(0,Fin)
    nx = int(Fin.N * (0.5 + x / Fin.siz))
    ny = int(Fin.N * (0.5 + y / Fin.siz))        
    Fout.field[ny, nx] = 1.0
    Fout._IsGauss=False
    return Fout
    
def PlaneWave(Fin, w, tx=0.0, ty=0.0, x_shift=0.0, y_shift=0.0):
    """
    *Creates a (circular) plane wavefront.*

    :param Fin: input field
    :type Fin: Field
    :param w: diameter of the plane wave
    :param tx: tilt in radiants (default = 0.0)
    :type tx: int, float
    :param ty: tilt in radiants (default = 0.0)
    :type ty: int, float
    :param x_shift: shift in x direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in y direction (default = 0.0)
    :type y_shift: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = PlaneWave(F, w = 2*mm) # plane wave with diameter of 2 mm at center of the grid
    >>> F = PlaneWave(F, w = 2*mm, x = 5*mm) # Idem at x=5mm, y=0.0
    >>> F = PlaneWave(F, w = 2*mm, x = 5*mm, ty = 1.0*mrad) # Idem at x=5mm, y=0.0, tilted 1.0 mrad
    >>> F = PlaneWave(F, 2*mm, 5*mm, 0.0, 1.0*mrad) # Idem
    """
    Fout = Field.copy(Fin)
    Fout=CircAperture(Fout, w/2, x_shift, y_shift )
    Fout=Tilt(Fout, tx, ty)
    Fout._IsGauss=False
    return Fout
    
@backward_compatible
def GaussBeam( Fin, w0, n=0, m=0, x_shift=0, y_shift=0, tx=0, ty=0, doughnut=False, LG=False):
    """
    *Creates a Gaussian beam in its waist.*

    :param Fin: input field
    :type Fin: Field
    :param w0: size of the Gauss waist
    :param x_shift: shift in x direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in y direction (default = 0.0)
    :type y_shift: int, float
    :param tx: tilt in radiants (default = 0.0)
    :type tx: int, float
    :param ty: tilt in radiants (default = 0.0)
    :type ty: int, float
    :param doughnut: if True a dougnut mode is generated (default = False)
    :type doughnut: bool
    :param LG: if True a (n,m) Laguerre-Gauss mode is generated, if False a Hermite Gauss mode (default = False)
    :type LG: bool
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> w0 = 3*mm
    >>> F=GaussBeam(w0,F) #TEM0,0 Hermite Gauss beam with size (radius) 3 mm in center of the grid
    >>> F=GaussBeam(w0,F,LG=True,n=2,m=5) # LG2,5 Laguerre Gauss beam
    >>> F=GaussBeam(w0,F,doughnut=True,m=1) # LG0,1* doughnut beam
    >>> F=GaussBeam(w0,F,doughnut=True,m=1, tx = 1*mrad, x_shift = 1*mm) #  idem, tilted and shifted
    """
    Fout=Field.copy(Fin)

    if not doughnut:
        if LG:
            Fout = GaussLaguerre(Fin, w0, p=n, l=m, A=1.0)
        else:
            Fout = GaussHermite(Fin, w0, n ,m, A=1.0)
    else:
        if m==0:
            m=1
            # alternative: raise error
            #raise ValueError(
            #        'm cannot be zero for the doughnut mode')
        Fout = GaussLaguerre(Fin, w0, p=n, l=m, A = 1.0 )
        Fout = Interpol( Fout, Fout.siz, Fout.N, 0, 0, 360 / (4 * m), 1)
        Fout = MultPhase(Fout, PI/2 )
        Fout = BeamMix(GaussLaguerre(Fin, w0, p=n, l=m, A=1 ), Fout)
    Fout = Interpol(Fout, Fin.siz, Fin.N, x_shift, y_shift, 0, 1 )
    Fout = Tilt(Fout, tx, ty )
    
    if not LG and not doughnut and tx == 0.0 and ty == 0.0 and x_shift == 0.0 and y_shift == 0.0:
        Fout._IsGauss = True #analytical propagation is possible using ABCD matrices
        Fout._q = -1j* _np.pi*w0*w0/Fout.lam
        Fout._w0 = w0
        Fout._z = 0.0
        Fout._A = 1.0
        Fout._n = n
        Fout._m = m

    return Fout
    
    
