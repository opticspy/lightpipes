from .field import Field
from .core import BeamMix, Phase, MultPhase, IntAttenuator, CircAperture, GaussHermite, GaussLaguerre, Interpol
from .misc import PI,Tilt
def PointSource(Fin,**kwargs):
    """
    Fout=PointSource(Fin, x=0, y=0)
    :ref:`Creates a point source. <Begin>`

    Args::
    
        required:
            Fin: input field
        
        optional:
            x=0, y=0: position of the point source.
        
        
    Returns::
     
        Fout: N x N square array of complex numbers (0+0j, or 1+0j where the pointsorce is ).
            
    Example:
    
    :ref:`Diffraction from a circular aperture <Diffraction>`
    
    """
    Fout = Field.copy(Fin)
    x , y = kwargs.get('x',0.0), kwargs.get('y',0.0)
    if abs(x) >= Fin.siz/2 or abs(y) >= Fin.siz/2:
        raise ValueError(
        'error in PointSource: x and y must be inside grid size, between: {:4.4f} and {:4.4f}, got: x = {:4.4f}, y = {:4.4f}'.format(-Fin.siz/2,Fin.siz/2,x,y))
    Fout=IntAttenuator(0,Fin)
    nx=int(Fin.N/2*(1+2*x/Fin.siz))
    ny=int(Fin.N/2*(1+2*y/Fin.siz))        
    Fout.field[ny, nx] = 1.0
    return Fout
    
def PlaneWave(w,tx,ty,xshift,yshift,Fin):
    """
    Fout=PlaneWave( w, tx, ty, xshift, yshift, Fin)
    :ref:`Creates a plane wavefront. <Begin>`
    
    Args::
    
        w: diameter of the source
        tx, ty: tilt of the wavefront
        xshift, yshift: shift of the source
        

    Returns::
     
        Fout: N x N square array of complex numbers (1+0j).
            
    Example:
    
    :ref:`Diffraction from a circular aperture <Diffraction>`
    
    """
    Fout = Field.copy(Fin)
    Fout=CircAperture(w/2,xshift,yshift,Fout)
    Fout=Tilt(tx,ty,Fout)
    return Fout

def GaussBeam(w0, Fin, **kwargs,):
    """
    F=GaussBeam(w0, tx, ty, xshift, yshift)
    :ref:`Creates a Gaussian beam in its waist. <Begin>`

    Args::
        required:
        w0: size of the Gauss waist
        Fin: input field

        optional:
        tx, ty: tilt of the beam
        xshift, yshift: shift of the beam
        n, m: TEMn,m  Hermite-Gauss or  Laguerre-Gauss mode.
        doughnut: if True a dougnut mode is generated
        LG: if True a Laguerre-Gauss mode is generated, otherwise a Hermite-Gauss mode.
        
    Returns::
     
        F: N x N square array of complex numbers (1+0j).
            
    Example:
    
    :ref:`Diffraction from a circular aperture <Diffraction>`
    
    """

    Fout=Field.copy(Fin)
    if not kwargs.get('doughnut'):
        if kwargs.get('LG'):
            Fout = GaussLaguerre(kwargs.get('n',0), kwargs.get('m',0), 1, w0, Fin)
        else:
            Fout = GaussHermite(kwargs.get('n',0), kwargs.get('m',0), 1, w0, Fin)
    else:
        m = kwargs.get('m',1)
        if m == 0:
            raise ValueError(
                    'm cannot be zero for the doughnut mode')
        Fout = GaussLaguerre(kwargs.get('n',0), m, 1, w0, Fin)
        Fout = Interpol(Fout.siz, Fout.N, 0, 0, 360 / (4 * m), 1, Fout)
        Fout = MultPhase(PI/2, Fout)
        Fout = BeamMix(GaussLaguerre(kwargs.get('n',0), m, 1, w0, Fin), Fout)
    Fout = Interpol(Fin.siz, Fin.N, kwargs.get('xshift',0.0), kwargs.get('yshift',0.0), 0, 1, Fout)
    Fout = Tilt(kwargs.get('tx',0.0), kwargs.get('ty',0.0), Fout)
    return Fout


