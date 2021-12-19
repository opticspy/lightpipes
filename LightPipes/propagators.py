# -*- coding: utf-8 -*-
import numpy as _np
from scipy.special import fresnel as _fresnel, hermite
from scipy.optimize import least_squares #TODO hide from public
from scipy.sparse import coo_matrix

from .field import Field
from . import tictoc
from .subs import elim, elimH, elimV
from .misc import backward_compatible
from .core import D4sigma
from LightPipes.config import _USE_PYFFTW

@backward_compatible
def Fresnel(Fin, z, usepyFFTW = False):
    """
    *Propagates the field using a convolution method.*

    :param Fin: input field
    :type Fin: Field
    :param z: propagation distance
    :type z: int, float
    :param usepyFFTW: use the pyFFTW Fast Fourier package (default = False)
                       Has no effect if _USEPYFFTW = True in config.py
    :type usepyFFTW: bool
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Examples:
    
    >>> F = Fresnel(F, 20*cm) # propagates the field 20 cm
    >>> F = Fresnel(F, 20*cm, usepyFFTW = True) # propagates the field 20 cm using the pyFFTW package
    >>> F = Fresnel(F, 20*cm, usepyFFTW = False) # propagates the field 20 cm using numpy fft
    
    .. seealso::
        
        * :ref:`Manual: Direct integration as a convolution: FFT approach. <Direct integration as a convolution: FFT approach.>`
        
        * :ref:`Examples: Young's experiment.<Young's experiment.>`
    """
    if z < 0:
        raise ValueError('Fresnel does not support negative z')
    if z == 0:
        Fout = Field.copy(Fin)
        return Fout #return copy to avoid hidden reference/link
    Fout = Field.shallowcopy(Fin) #no need to copy .field as it will be
    # re-created anyway inside _field_Fresnel()
    Fout.field = _field_Fresnel(z, Fout.field, Fout.dx, Fout.lam, Fout._dtype, usepyFFTW)
    Fout._IsGauss=False
    return Fout


def _field_Fresnel(z, field, dx, lam, dtype, usepyFFTW):
    """
    Separated the "math" logic out so that only standard and numpy types
    are used.
    
    Parameters
    ----------
    z : float
        Propagation distance.
    field : ndarray
        2d complex numpy array (NxN) of the field.
    dx : float
        In units of sim (usually [m]), spacing of grid points in field.
    lam : float
        Wavelength lambda in sim units (usually [m]).
    dtype : dtype
        complex dtype of the array.
    usepyFFTW : bool
        Use the pyFFTW package if True
        Use numpy FFT if False

    Returns
    -------
    ndarray (2d, NxN, complex)
        The propagated field.

    """
    
    """ *************************************************************
    Major differences to Cpp based LP version:
        - dx =siz/N instead of dx=siz/(N-1), more consistent with physics 
            and rest of LP package
        - fftw DLL uses no normalization, numpy uses 1/N on ifft -> omitted
            factor of 1/(2*N)**2 in final calc before return
        - bug in Cpp version: did not touch top row/col, now we extract one
            more row/col to fill entire field. No errors noticed with the new
            method so far
    ************************************************************* """
    _using_pyfftw = False # determined if loading is successful  
    if usepyFFTW or _USE_PYFFTW:
        try:
            import pyfftw as _pyfftw
            from pyfftw.interfaces.numpy_fft import fft2 as _fft2
            from pyfftw.interfaces.numpy_fft import ifft2 as _ifft2
            _fftargs = {'planner_effort': 'FFTW_ESTIMATE',
                        'overwrite_input': True,
                        'threads': -1} #<0 means use multiprocessing.cpu_count()
            _using_pyfftw = True 
        except ImportError:
            #import warnings
            #warnings.warn(_WARNING)
            _WARNING =  '\n**************************** WARNING ***********************\n'\
            +'In the Fresnel command you required FFT with the pyFFTW package.\n'\
            +'or  _USE_PYFFTW = True in your config.py file.\n'\
            +'However LightPipes cannot import pyFFTW because it is not installed.\n'\
            +'Falling back to numpy.fft.\n'\
            +'(Try to) install pyFFTW on your computer for faster performance.\n'\
            +'Enter at a terminal prompt: python -m pip install pyfftw.\n'\
            +'Or reinstall LightPipes with the option pyfftw\n'\
            +'Enter: python -m pip install lightpipes[pyfftw]\n\n'\
            +'*************************************************************'
            print(_WARNING)
    if not _using_pyfftw:
        from numpy.fft import fft2 as _fft2
        from numpy.fft import ifft2 as _ifft2
        _fftargs = {}
    tictoc.tic()
    N = field.shape[0] #assert square
    
    legacy = True #switch on to numerically compare oldLP/new results
    if legacy:
        kz = 2.*3.141592654/lam * z
        siz = N*dx
        dx = siz/(N-1) #like old Cpp code, even though unlogical
    else:
        kz = 2*_np.pi/lam*z
        
    
    cokz = _np.cos(kz)
    sikz = _np.sin(kz)
    
    No2 = int(N/2) #"N over 2"
    """The following section contains a lot of uses which boil down to
    2*No2. For even N, this is N. For odd N, this is NOT redundant:
        2*No2 is N-1 for odd N, therefore sampling an even subset of the
        field instead of the whole field. Necessary for symmetry of first
        step involving Fresnel integral calc.
    """
    if _using_pyfftw:
        in_outF = _pyfftw.zeros_aligned((2*N, 2*N),dtype=dtype)
        in_outK = _pyfftw.zeros_aligned((2*N, 2*N),dtype=dtype)
    else:
        in_outF = _np.zeros((2*N, 2*N),dtype=dtype)
        in_outK = _np.zeros((2*N, 2*N),dtype=dtype)
    
    """Our grid is zero-centered, i.e. the 0 coordiante (beam axis) is
    not at field[0,0], but field[No2, No2]. The FFT however is implemented
    such that the frequency 0 will be the first element of the output array,
    and it also expects the input to have the 0 in the corner.
    For the correct handling, an fftshift is necessary before *and* after
    the FFT/IFFT:
        X = fftshift(fft(ifftshift(x)))  # correct magnitude and phase
        x = fftshift(ifft(ifftshift(X)))  # correct magnitude and phase
        X = fftshift(fft(x))  # correct magnitude but wrong phase !
        x = fftshift(ifft(X))  # correct magnitude but wrong phase !
    A numerically faster way to achieve the same result is by multiplying
    with an alternating phase factor as done below.
    Speed for N=2000 was ~0.4s for a double fftshift and ~0.1s for a double
    phase multiplication -> use the phase factor approach (iiij).
    """
    # Create the sign-flip pattern for largest use case and 
    # reference smaller grids with a view to the same data for
    # memory saving.
    ii2N = _np.ones((2*N),dtype=float)
    ii2N[1::2] = -1 #alternating pattern +,-,+,-,+,-,...
    iiij2N = _np.outer(ii2N, ii2N)
    iiij2No2 = iiij2N[:2*No2,:2*No2] #slice to size used below
    iiijN = iiij2N[:N, :N]

    RR = _np.sqrt(1/(2*lam*z))*dx*2
    io = _np.arange(0, (2*No2)+1) #add one extra to stride fresnel integrals
    R1 = RR*(io - No2)
    fs, fc = _fresnel(R1)
    fss = _np.outer(fs, fs) #    out[i, j] = a[i] * b[j]
    fsc = _np.outer(fs, fc)
    fcs = _np.outer(fc, fs)
    fcc = _np.outer(fc, fc)
    
    """Old notation (0.26-0.33s):
        temp_re = (a + b + c - d + ...)
        # numpy func add takes 2 operands A, B only
        # -> each operation needs to create a new temporary array, i.e.
        # ((((a+b)+c)+d)+...)
        # since python does not optimize to += here (at least is seems)
    New notation (0.14-0.16s):
        temp_re = (a + b) #operation with 2 operands
        temp_re += c
        temp_re -= d
        ...
    Wrong notation:
        temp_re = a #copy reference to array a
        temp_re += b
        ...
        # changing `a` in-place, re-using `a` will give corrupted
        # result
    """
    temp_re = (fsc[1:, 1:] #s[i+1]c[j+1]
               + fcs[1:, 1:]) #c[+1]s[+1]
    temp_re -= fsc[:-1, 1:] #-scp [p=+1, without letter =+0]
    temp_re -= fcs[:-1, 1:] #-csp
    temp_re -= fsc[1:, :-1] #-spc
    temp_re -= fcs[1:, :-1] #-cps
    temp_re += fsc[:-1, :-1] #sc
    temp_re += fcs[:-1, :-1] #cs
    
    temp_im = (-fcc[1:, 1:] #-cpcp
               + fss[1:, 1:]) # +spsp
    temp_im += fcc[:-1, 1:] # +ccp
    temp_im -= fss[:-1, 1:] # -ssp
    temp_im += fcc[1:, :-1] # +cpc
    temp_im -= fss[1:, :-1] # -sps
    temp_im -= fcc[:-1, :-1] # -cc
    temp_im += fss[:-1, :-1]# +ss
    
    temp_K = 1j * temp_im # a * b creates copy and casts to complex
    temp_K += temp_re
    temp_K *= iiij2No2
    temp_K *= 0.5
    in_outK[(N-No2):(N+No2), (N-No2):(N+No2)] = temp_K
    
    in_outF[(N-No2):(N+No2), (N-No2):(N+No2)] \
        = field[(N-2*No2):N,(N-2*No2):N] #cutting off field if N odd (!)
    in_outF[(N-No2):(N+No2), (N-No2):(N+No2)] *= iiij2No2
    
    tictoc.tic()
    in_outK = _fft2(in_outK, **_fftargs)
    in_outF = _fft2(in_outF, **_fftargs)
    t_fft1 = tictoc.toc()
    
    in_outF *= in_outK
    
    in_outF *= iiij2N
    tictoc.tic()
    in_outF = _ifft2(in_outF, **_fftargs)
    t_fft2 = tictoc.toc()
    #TODO check normalization if USE_PYFFTW
    
    Ftemp = (in_outF[No2:N+No2, No2:N+No2]
             - in_outF[No2-1:N+No2-1, No2:N+No2])
    Ftemp += in_outF[No2-1:N+No2-1, No2-1:N+No2-1]
    Ftemp -= in_outF[No2:N+No2, No2-1:N+No2-1]
    comp = complex(cokz, sikz)
    Ftemp *= 0.25 * comp
    Ftemp *= iiijN
    field = Ftemp #reassign without data copy
    ttotal = tictoc.toc()
    t_fft = t_fft1 + t_fft2
    t_outside = ttotal - t_fft
    debug_time = False
    if debug_time:
        print('Time total = fft + rest: {:.2f}={:.2f}+{:.2f}'.format(
            ttotal, t_fft, t_outside))
    return field

@backward_compatible
def Forward(Fin, z, sizenew, Nnew ):
    """
    *Propagates the field using direct integration.*

    :param Fin: input field
    :type Fin: Field
    :param z: propagation distance
    :type z: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = Forward(F, 20*cm, 10*mm, 20) # propagates the field 20 cm, for a new grid size of 10 mm and a new grid dimension 20
    
    .. seealso::
        
        * :ref:`Manual: Direct integration. <Direct integration.>`
        
        * :ref:`Manual: Splitting and mixing beams.<Splitting and mixing beams.>` (figure 10.)
    """
    if z <= 0:
        raise ValueError('Forward does not support z<=0')
    Fout = Field.begin(sizenew, Fin.lam, Nnew, Fin._dtype)
    
    field_in = Fin.field
    field_out = Fout.field
    
    field_out[:,:] = 0.0 #default is ones, clear
    
    old_size = Fin.siz
    old_n    = Fin.N
    new_size = sizenew #renaming to match cpp code
    new_n = Nnew

    on2     = int(old_n/2)
    nn2     = int(new_n/2) #read "new n over 2"
    dx_new   = new_size/(new_n-1)
    dx_old   = old_size/(old_n-1)
    #TODO again, dx seems better defined without -1, check this
    
    R22 = _np.sqrt(1/(2*Fin.lam*z))

    X_new = _np.arange(-nn2, new_n-nn2) * dx_new
    Y_new = X_new #same
    X_old = _np.arange(-on2, old_n-on2) * dx_old
    Y_old = X_old #same
    for i_new in range(new_n):
        x_new = X_new[i_new]
        
        P1 = R22*(2*(X_old-x_new)+dx_old)
        P3 = R22*(2*(X_old-x_new)-dx_old)
        Fs1, Fc1 = _fresnel(P1)
        Fs3, Fc3 = _fresnel(P3)
        for j_new in range(new_n):
            y_new = Y_new[j_new]
            
            P2 = R22*(2*(Y_old-y_new)-dx_old)
            P4 = R22*(2*(Y_old-y_new)+dx_old)
            Fs2, Fc2 = _fresnel(P2)
            Fs4, Fc4 = _fresnel(P4)
            
            C4C1=_np.outer(Fc4, Fc1) #out[i, j] = a[i] * b[j] 
            C2S3=_np.outer(Fc2, Fs3) #->  out[j,i] = a[j]*b[i] here
            C4S1=_np.outer(Fc4, Fs1)
            S4C1=_np.outer(Fs4, Fc1)
            S2C3=_np.outer(Fs2, Fc3)
            C2S1=_np.outer(Fc2, Fs1)
            S4C3=_np.outer(Fs4, Fc3)
            S2C1=_np.outer(Fs2, Fc1)
            C4S3=_np.outer(Fc4, Fs3)
            S2S3=_np.outer(Fs2, Fs3)
            S2S1=_np.outer(Fs2, Fs1)
            C2C3=_np.outer(Fc2, Fc3)
            S4S1=_np.outer(Fs4, Fs1)
            C4C3=_np.outer(Fc4, Fc3)
            C4C1=_np.outer(Fc4, Fc1)
            S4S3=_np.outer(Fs4, Fs3)
            C2C1=_np.outer(Fc2, Fc1)
            
            Fr = 0.5 * field_in.real
            Fi = 0.5 * field_in.imag
            Temp_c = (Fr * (C2S3 + C4S1 + S4C1 + S2C3
                            - C2S1 - S4C3 - S2C1 - C4S3)
                      + Fi * (-S2S3 + S2S1 + C2C3 - S4S1
                              - C4C3 + C4C1 + S4S3 - C2C1)
                      + 1j * Fr *(-C4C1 + S2S3 + C4C3 - S4S3
                                  + C2C1 - S2S1 + S4S1 - C2C3)
                      + 1j * Fi*(C2S3 + S2C3 + C4S1 + S4C1
                                 - C4S3 - S4C3 - C2S1 - S2C1))
            field_out[j_new, i_new] = Temp_c.sum() #complex elementwise sum
    Fout._IsGauss=False
    return Fout

@backward_compatible
def Forvard(Fin, z, usepyFFTW = False):
    """
    *Propagates the field using a FFT algorithm.*

    :param Fin: input field
    :type Fin: Field
    :param z: propagation distance
    :type z: int, float
    :param usepyFFTW: use the pyFFTW Fast Fourier package (default = False)
                       Has no effect if _USEPYFFTW = True in config.py
    :type usepyFFTW: bool
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Examples:
    
    >>> F = Forvard(F, 20*cm) # propagates the field 20 cm
    >>> F = Forvard(F, 20*cm, usepyFFTW = True) # propagates the field 20 cm using the pyFFTW package
    >>> F = Forvard(F, 20*cm, usepyFFTW = False) # propagates the field 20 cm using numpy FFT
    
    .. seealso::
        
        * :ref:`Manual: FFT propagation (spectral method).<FFT propagation (spectral method).>`
        
        * :ref:`Examples: Diffraction from a circular aperture.<Diffraction from a circular aperture.>`
    """
    _using_pyfftw = False # determined if loading is successful
    if usepyFFTW or _USE_PYFFTW:
        try:
            import pyfftw as _pyfftw
            from pyfftw.interfaces.numpy_fft import fft2 as _fft2
            from pyfftw.interfaces.numpy_fft import ifft2 as _ifft2
            _fftargs = {'planner_effort': 'FFTW_ESTIMATE',
                        'overwrite_input': True,
                        'threads': -1} #<0 means use multiprocessing.cpu_count()
            _using_pyfftw = True 
        except ImportError:
            #import warnings
            #warnings.warn(_WARNING)
            _WARNING =  '\n**************************** WARNING ***********************\n'\
            +'In the Forvard command you required FFT with the pyFFTW package, \n'\
            +'or  _USE_PYFFTW = True in your config.py file.\n'\
            +'However LightPipes cannot import pyFFTW because it is not installed.\n'\
            +'Falling back to numpy.fft.\n'\
            +'(Try to) install pyFFTW on your computer for faster performance.\n'\
            +'Enter at a terminal prompt: python -m pip install pyfftw.\n'\
            +'Or reinstall LightPipes with the option pyfftw\n'\
            +'Enter: python -m pip install lightpipes[pyfftw]\n\n'\
            +'*************************************************************'
            print(_WARNING)
    if not _using_pyfftw:
        from numpy.fft import fft2 as _fft2
        from numpy.fft import ifft2 as _ifft2
        _fftargs = {}

    if z==0:
        Fout = Field.copy(Fin)
        return Fout #return copy to avoid hidden reference
    Fout = Field.shallowcopy(Fin)
    N = Fout.N
    size = Fout.siz
    lam = Fout.lam
    dtype = Fin._dtype
    
    if _using_pyfftw:
        in_out = _pyfftw.zeros_aligned((N, N),dtype=dtype)
    else:
        in_out = _np.zeros((N, N),dtype=dtype)
    in_out[:,:] = Fin.field
    
    _2pi = 2*_np.pi
    legacy = True
    if legacy:
        _2pi = 2.*3.141592654 #make comparable to Cpp version by using exact same val
    if (z==0): #check if z==0, return Fin
        return Fin
    zz = z
    z = abs(z)
    kz = _2pi/lam*z
    cokz = _np.cos(kz)
    sikz = _np.sin(kz)
    
    # Sign pattern effectively equals an fftshift(), see Fresnel code
    iiN = _np.ones((N,),dtype=float)
    iiN[1::2] = -1 #alternating pattern +,-,+,-,+,-,...
    iiij = _np.outer(iiN, iiN)
    in_out *= iiij
    
    z1 = z*lam/2
    No2 = int(N/2)

    SW = _np.arange(-No2, N-No2)/size
    SW *= SW
    SSW = SW.reshape((-1,1)) + SW #fill NxN shape like np.outer()
    Bus = z1 * SSW
    Ir = Bus.astype(int) #truncate, not round
    Abus = _2pi*(Ir-Bus) #clip to interval [-2pi, 0]
    Cab = _np.cos(Abus)
    Sab = _np.sin(Abus)
    CC = Cab + 1j * Sab #noticably faster than writing exp(1j*Abus)
    
    if zz >= 0.0:
        in_out = _fft2(in_out, **_fftargs)
        in_out *= CC
        in_out = _ifft2(in_out, **_fftargs)
    else:
        in_out = _ifft2(in_out, **_fftargs)
        CCB = CC.conjugate()
        in_out *= CCB
        in_out = _fft2(in_out, **_fftargs)
    
    in_out *= (cokz + 1j* sikz)
    in_out *= iiij #/N**2 omitted since pyfftw already normalizes (numpy too)
    Fout.field = in_out
    Fout._IsGauss=False
    return Fout

def GForvard(Fin,z):
    """
    *Propagates a pure Gaussian field using ABCD matrix theory.*

    :param Fin: input field, must be pare Gaussian.
    :type Fin: Field
    :param z: propagation distance
    :type z: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        
        wavelength = 500*nm
        size = 7*mm
        N = 1000
        
        w0 = 1*mm
        z = 1*m

        F = Begin(size,wavelength,N)
        F = GaussBeam(F, w0,n=0,m=0)
        F = GForvard(F,z)      
    """
    A=1.0
    B=z
    C=0.0
    D=1.0
    M=[[A,B],[C,D]]
    Fout=ABCD(Fin,M)
    return Fout
    
def ABCD(Fin, M):
    """
    *Propagates a pure Gaussian field using ABCD matrix theory.*

    :param Fin: input field, must be pare Gaussian.
    :type Fin: Field
    :param M: 2 x 2 ABCD matrix
    :type M: List
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    .. code-block::
    
        from LightPipes import *
        
        wavelength = 500*nm
        size = 7*mm
        N = 1000
        
        w0 = 1*mm
        f = 1*m
        z = 1*m

        M_lens = [
            [1.0,       0.0],
            [-1.0/f,    1.0]
          ]
          
        M_propagate = [
            [1.0,       z ],
            [0.0,       1.0]
          ]
        
        F = Begin(size,wavelength,N)
        F = GaussBeam(F, w0,n=0,m=0)
        F = ABCD(F,M_lens)
        F = ABCD(F,M_propagate)
        
    """
    Fout = Field.copy(Fin)    
    A=M[0][0]
    B=M[0][1]
    C=M[1][0]
    D=M[1][1]
    if Fin._IsGauss:
        Fout._q = (A*Fin._q + B)/(C*Fin._q + D)
        Fout._z=Fin._z + B
        w2=-Fin.lam/_np.pi*(Fout._q.imag+Fout._q.real*Fout._q.real/Fout._q.imag)
        w02=Fin._w0 * Fin._w0
        w=_np.sqrt(w2)
        inv_R=(1/Fout._q).real
        
        z0=_np.pi*w02/Fin._lam
        k = 2*_np.pi/Fin.lam
        phase_z=k*Fout._z-(Fin._m+Fin._n+1)*_np.arctan(Fout._z/z0)
        
        r2 = Fin.mgrid_Rsquared
        Y,X = Fin.mgrid_cartesian

        phase_trans=k/2*inv_R*r2
        sqrt2w=_np.sqrt(2)/w
        sqrt2xw=sqrt2w*X
        sqrt2yw=sqrt2w*Y
        w0w=Fin._w0/w
        Fout.field=Fin._A*w0w*_np.exp(-r2/w2)*hermite(Fin._n)(sqrt2xw)*hermite(Fin._m)(sqrt2yw)*_np.exp(1j*(phase_trans+phase_z))
        Fout._IsGauss = True
        Fout._w0=Fin._w0
        Fout._n=Fin._n
        Fout._m=Fin._m
        Fout._A=Fin._A
        return Fout
    else:
        print("not pure Gauss beam, field not propagated")
        return Fout

def Propagate(Fin,z,UseFresnel=False,UseForvard=False):
    """
    *Experimental general propagation command*
    
    Propagate is an experimental propagation command which selects the best propagation routine automatically.
    The idea is to use something like the Fesnel number to select the Forvard, GForvard or the Fresnel command.
    Please provide us with tips to improve this command by starting an issue on our github repository!
    
    At this moment the code looks like this:
    
    .. code-block::
    
        def Propagate(Fin,z,UseFresnel=False,UseForvard=False):
            xs,ys=D4sigma(Fin)
            M=10
            NF=M*(((xs**4)/Fin.lam)**0.333)/z # Check with formula given by jjmelko in issue 59
            #NF=xs*xs/Fin.lam/z #Check with Fresnel number
            print(NF)
            if Fin._IsGauss: #obvious choice ...
                print('using GForvard, pure Gauss field')
                return GForvard(Fin,z)
            else:
                if UseFresnel:
                    print('forced to use Fresnel')
                    return Fresnel(Fin,z)
                if UseForvard:
                    print('forced to use Forvard')
                    return Forvard(Fin,z)
                if NF > 1:
                    print('using Fresnel because NF = {:4.2f}'.format(NF))
                    return Fresnel(Fin,z)
                else:
                    print('using Forvard because NF = {:4.2f}'.format(NF))
                    return Forvard(Fin,z)

    """
    xs,ys=D4sigma(Fin)
    M=10
    NF=M*(((xs**4)/Fin.lam)**0.333)/z # Check with formula given by jjmelko in issue 59
    #NF=xs*xs/Fin.lam/z #Check with Fresnel number
    print(NF)
    if Fin._IsGauss: #obvious choice ...
        print('using GForvard, pure Gauss field')
        return GForvard(Fin,z)
    else:
        if UseFresnel and not UseForvard:
            print('forced to use Fresnel')
            return Fresnel(Fin,z)
        if UseForvard and not UseFresnel:
            print('forced to use Forvard')
            return Forvard(Fin,z)
        if UseForvard and UseFresnel:
            print('cannot force both methods!, no propagation performed')
            return Fin
        if NF > 1:
            print('using Fresnel because NF = {:4.2f}'.format(NF))
            return Fresnel(Fin,z)
        else:
            print('using Forvard because NF = {:4.2f}'.format(NF))
            return Forvard(Fin,z)

@backward_compatible
def Steps(Fin, z, nstep = 1, refr = 1.0, save_ram=False, use_scipy=False):
    """
    *Propagates the field a distance, nstep x z, in nstep steps in a
    medium with a complex refractive index stored in the
    square array refr.*
    
    :param Fin: input field
    :type Fin: Field
    :param z: propagation distance per step
    :type z: int, float
    :param nstep: number of steps (default = 1)
    :type nstep: int, float
    :param refr: refractive index (N x N array of complex numbers) (default = 1.0)
    :type refr: numpy.ndarray
    :param save_ram: saves ram but slower! (default = False)
    :type save_ram: bool
    :param use_scipy: should not be used; for development only! (default = False)
    :type use_scipy: bool    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    .. seealso::
    
        * :ref:`Manual: Finite difference method.<Finite difference method.>`
        
        * :ref:`Examples: Propagation in a lens-like, absorptive medium.<Propagation in a lens-like, absorptive medium.>`
    """
    if use_scipy:
        print('Warning! Non-functional develop version for testing')
        return _TODOStepsScipy(z, nstep, refr, Fin)
    else:
        if save_ram:
            """Loops version goes line by line and therefore only needs
            1 field in RAM and several vectors of length N.
            The other version also works line by line, but instead of looping
            uses numpy syntax to operate on all lines simultaneously.
            Thus, several arrays of size N^2 have to be stored simultaneously!
            """
            return _StepsLoopElim(z, nstep, refr, Fin)
        else:
            return _StepsArrayElim(z, nstep, refr, Fin)


def _StepsArrayElim(z, nstep, _refr, Fin):

    if Fin._curvature != 0.0:
        raise ValueError('Cannot operate on spherical coords.'
                         + 'Use Convert() first')
    if type(_refr) != _np.ndarray:
        refr=_np.ones((Fin.N,Fin.N))*_refr
    else:
        refr = _refr
    
    if Fin.field.shape != refr.T.shape:
        #TODO fix the .T problem
        raise ValueError('refractive index refr must have same NxN'
                         + ' dimension as field.')
    
    Fout = Field.copy(Fin)
    N = Fout.N
    lam = Fout.lam
    size = Fout.siz
    dtype = Fout._dtype
    
    legacy = True
    if legacy:
        Pi = 3.141592654 #to compare Cpp results accurately
    else:
        Pi = _np.pi
    K = 2.*Pi/lam
    dz = z/2. #since 2 staggered steps, each row then col-wise
    Pi4lz = 2*K/dz
    imPi4lz = 1j * Pi4lz
    
    delta = size/(N-1.) #dx
    delta2 = delta*delta
    
    """
    /* absorption at the borders is described here */
    """
    AA= -10./dz/nstep #/* total absorption */
    band_pow=2.   #/* profile of the absorption border, 2=quadratic*/
    """
    /* width of the absorption border */
    """
    i_left  = N/2 + 1.0 - 0.4*N
    i_right = N/2 + 1.0 + 0.4*N
    
    """
    ///* absorption borders are formed here */
    """
    c_absorb_x = _np.zeros(N, dtype=dtype)
    iv = _np.arange(N, dtype=int)
    mask = iv+1<=i_left
    iii = i_left - iv[mask]
    c_absorb_x[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = iv+1 >= i_right
    iii = iv[mask2]-i_right+2
    im = N-i_right+1
    c_absorb_x[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    
    c_absorb_x2 = _np.zeros(N, dtype=dtype)
    mask = iv+1<=i_left
    iii = i_left - iv[mask]
    c_absorb_x2[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = iv+1 >= i_right
    iii = iv[mask2]-i_right+1 #TODO why 1 difference
    im = N-i_right+1
    c_absorb_x2[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    
    c_absorb_y = _np.zeros(N, dtype=dtype)
    jv = _np.arange(N, dtype=int)
    mask = jv+1<=i_left
    iii = i_left - jv[mask] -1# REM +1 in i direction, why different here?
    c_absorb_y[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = jv+1 >= i_right
    iii = jv[mask2]-i_right+1
    im = N-i_right+1
    c_absorb_y[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    # c_absorb_y2 = _np.zeros(N, dtype=complex)
    # mask = jv+1<=i_left
    # iii = i_left - jv[mask]-1# REM +1 in i direction, why different here?
    # c_absorb_y2[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    # mask2 = jv+1 >= i_right
    # iii = jv[mask2]-i_right+1
    # im = N-i_right+1
    # c_absorb_y2[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    c_absorb_y2 = c_absorb_y
    #TODO last two were identical, why are absorbx,x2,y different?
    # probably can just assume same everywhere after legacy=False...
    """
    ///* end absorption */
    """

    refr = refr.T #TODO I messed up somewhere...
    
    """The refraction part (real part of refr. index n) is separated out
    and applied as a phase term instead of stepping through like the
    imaginary part. According to LightPipes for MATLAB manual, this proved
    to be more stable."""
    
    # expfi4 = _np.exp(1j*0.25*K*dz*(refr.real-1.0))
    tempfi = 1j*refr.real
    tempfi -= 1j*1.0 #avoid mem copies where possible
    tempfi *= 0.25*K*dz 
    expfi4 = _np.exp(tempfi, out=tempfi) #quarter phase fi, for half phase apply twice
    
    # medium = (-1j*K)*refr.imag
    mediumIm = -K*refr.imag #half the RAM vs. complex, real part 0 anyway
    
    CCX = -2/delta2 + 1j*(Pi4lz + mediumIm)
    CCX[1:N-2:2,:] -= c_absorb_x
    CCX[2:N-1:2,:] -= c_absorb_x2
    CCY = -2/delta2 + 1j*(Pi4lz + mediumIm)
    CCY[:,1:N-2:2] -= c_absorb_y.reshape((-1,1)) #to column vector
    CCY[:,2:N-1:2] -= c_absorb_y2.reshape((-1,1)) #to column vector
    
    #Variables for elimination function elim():
    a = -1/delta2
    b = -1/delta2 #keep both since one day might be different dx and dy
    UU = _np.zeros((N,N), dtype=dtype)
    Alpha = _np.zeros((N,N), dtype=dtype)
    Beta = _np.zeros((N,N), dtype=dtype)
    P = _np.zeros((N,N), dtype=dtype)
    tempCNN = _np.zeros((N,N), dtype=dtype) #use as scratch to avoid mem alloc in loop
    
    """
    /*  Main  loop, steps here */
    """
    for istep in range(nstep):
        """
        /*  Elimination in the direction i  */
        """
        Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
        
        # P[1:N-1, 1:N-1] = -1/delta2 * (Uij_1 + Uij1 -2.0 * Uij) + imPi4lz * Uij
        # re-write avoiding mem-alloc of large arrays:
        Uij = Fout.field[1:N-1, 1:N-1] #creates a view, no overhead
        Uij1 = Fout.field[2:N, 1:N-1]
        Uij_1 = Fout.field[0:N-2, 1:N-1]
        P[1:N-1, 1:N-1] = Uij
        P[1:N-1, 1:N-1] *= -2
        P[1:N-1, 1:N-1] += Uij_1
        P[1:N-1, 1:N-1] += Uij1
        P[1:N-1, 1:N-1] *= -1/delta2
        tempCNN[1:N-1, 1:N-1] = Uij
        tempCNN[1:N-1, 1:N-1] *= imPi4lz
        P[1:N-1, 1:N-1] += tempCNN[1:N-1, 1:N-1]
        
        elimH(N, a, b, CCX, P, UU, Alpha, Beta)
        
        #loop-identical, even though maybe buggy:
        Fout.field[0, :] = 0.0
        Fout.field[1:N-2, :] = UU[1:N-2, :] #only runs to N-3 inclusive!
        #field[N-2, ] is skipped!!!
        Fout.field[N-1, :] = UU[N-2, :]
        
        Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
        Fout.field *= expfi4 #twice makes it 0.5*k*dz*(n-1)
        
        """
        /* Elimination in the j direction */
        """
        
        # P[1:N-1, 1:N-1] = -1/delta2 * (Ui_1j + Ui1j -2.0 * Uij) + imPi4lz * Uij
        # re-write avoiding mem-alloc of large arrays:
        Uij = Fout.field[1:N-1, 1:N-1] #creates a view, no overhead
        Ui1j = Fout.field[1:N-1, 2:N]
        Ui_1j = Fout.field[1:N-1, 0:N-2]
        P[1:N-1, 1:N-1] = Uij
        P[1:N-1, 1:N-1] *= -2
        P[1:N-1, 1:N-1] += Ui_1j
        P[1:N-1, 1:N-1] += Ui1j
        P[1:N-1, 1:N-1] *= -1/delta2
        tempCNN[1:N-1, 1:N-1] = Uij
        tempCNN[1:N-1, 1:N-1] *= imPi4lz
        P[1:N-1, 1:N-1] += tempCNN[1:N-1, 1:N-1]
        
        elimV(N, a, b, CCY, P, UU, Alpha, Beta)
        
        #loop-identical, even though maybe buggy:
        Fout.field[:, 0] = 0.0
        Fout.field[:, 1:N-2] = UU[:, 1:N-2] #only runs to N-3 inclusive!
        
        #TODO BUG! why are we accessing i here? out of scope. Last value:
        #resulting from for(ii in range(1, N-2, 2))
        # -> last ii in loop is int((N-2)/2)*2-1
        # and i=ii+1
        # -> i_final = int((N-2)/2)*2-1+1 = int((N-2)/2)*2
        # tested OK for even and odd N -> works for all N
        i = int((N-2)/2)*2
        #TODO also, why 0:N-1 where all else is 0:N?
        Fout.field[0:N-1, i] = UU[1:N, N-2]
    """
    ///* end j */
    """
    #TODO should this be in nstep loop??
    # seems so, that would add up to 1*ikz*n, right now its 3/4*ikz per iter
    # and a final 1/4 ??
    Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
    Fout._IsGauss=False
    return Fout


def _StepsLoopElim(z, nstep, _refr, Fin):
    """
    Fout = StepsLoopElim(z, nstep, refr, Fin)

    """
    if Fin._curvature != 0.0:
        raise ValueError('Cannot operate on spherical coords.'
                         + 'Use Convert() first')

    if type(_refr) != _np.ndarray:
        refr=_np.ones((Fin.N,Fin.N))*_refr
    else:
        refr = _refr
    
    if Fin.field.shape != refr.T.shape:
        #TODO fix the .T problem
        raise ValueError('refractive index refr must have same NxN'
                         + ' dimension as field.')
        
    Fout = Field.copy(Fin)
    N = Fout.N
    lam = Fout.lam
    size = Fout.siz
    dtype = Fout._dtype
    
    legacy = True
    if legacy:
        Pi = 3.141592654 #to compare Cpp results accurately
    else:
        Pi = _np.pi
    K = 2.*Pi/lam
    dz = z/2. #since 2 staggered steps, each row then col-wise
    Pi4lz = 2*K/dz
    imPi4lz = 1j * Pi4lz
    
    delta = size/(N-1.) #dx
    delta2 = delta*delta
    
    """
    /* absorption at the borders is described here */
    """
    AA= -10./dz/nstep #/* total absorption */
    band_pow=2.   #/* profile of the absorption border, 2=quadratic*/
    """
    /* width of the absorption border */
    """
    i_left  = N/2 + 1.0 - 0.4*N
    i_right = N/2 + 1.0 + 0.4*N
    
    """
    ///* absorption borders are formed here */
    """
    c_absorb_x = _np.zeros(N, dtype=dtype)
    iv = _np.arange(N, dtype=int)
    mask = iv+1<=i_left
    iii = i_left - iv[mask]
    c_absorb_x[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = iv+1 >= i_right
    iii = iv[mask2]-i_right+2
    im = N-i_right+1
    c_absorb_x[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    
    c_absorb_x2 = _np.zeros(N, dtype=dtype)
    mask = iv+1<=i_left
    iii = i_left - iv[mask]
    c_absorb_x2[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = iv+1 >= i_right
    iii = iv[mask2]-i_right+1 #TODO why 1 difference
    im = N-i_right+1
    c_absorb_x2[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    
    c_absorb_y = _np.zeros(N, dtype=dtype)
    jv = _np.arange(N, dtype=int)
    mask = jv+1<=i_left
    iii = i_left - jv[mask] -1# REM +1 in i direction, why different here?
    c_absorb_y[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    mask2 = jv+1 >= i_right
    iii = jv[mask2]-i_right+1
    im = N-i_right+1
    c_absorb_y[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    
    # c_absorb_y2 = _np.zeros(N, dtype=complex)
    # mask = jv+1<=i_left
    # iii = i_left - jv[mask]-1# REM +1 in i direction, why different here?
    # c_absorb_y2[mask] = 1j* (AA*K)*_np.power(iii/i_left, band_pow)
    
    # mask2 = jv+1 >= i_right
    # iii = jv[mask2] +1-i_right#REM +1 for i-direction loop, why different?
    # im = N-i_right+1
    # c_absorb_y2[mask2] = 1j* (AA*K)*_np.power(iii/im, band_pow)
    
    c_absorb_y2 = c_absorb_y
    #TODO last two were identical, why are absorbx,x2,y different?
    # probably can just assume same everywhere after legacy=False...
    """
    ///* end absorption */
    """
    
    refr = refr.T #TODO I messed up somewhere...
    
    """The refraction part (real part of refr. index n) is separated out
    and applied as a phase term instead of stepping through like the
    imaginary part. According to LightPipes for MATLAB manual, this proved
    to be more stable."""
    
    # expfi4 = _np.exp(1j*0.25*K*dz*(refr.real-1.0))
    tempfi = 1j*refr.real
    tempfi -= 1j*1.0 #avoid mem copies where possible
    tempfi *= 0.25*K*dz 
    expfi4 = _np.exp(tempfi, out=tempfi) #quarter phase fi, for half phase apply twice
    
    # medium = (-1j*K)*refr.imag
    mediumIm = -K*refr.imag #half the RAM vs. complex, real part 0 anyway
    
    CCX = -2/delta2 + 1j*(Pi4lz + mediumIm)
    CCX[1:N-2:2,:] -= c_absorb_x
    CCX[2:N-1:2,:] -= c_absorb_x2
    CCY = -2/delta2 + 1j*(Pi4lz + mediumIm)
    CCY[:,1:N-2:2] -= c_absorb_y.reshape((-1,1)) #to column vector
    CCY[:,2:N-1:2] -= c_absorb_y2.reshape((-1,1)) #to column vector
    
    #Variables for elimination function elim():
    a = -1/delta2
    b = -1/delta2
    uu = _np.zeros(N, dtype=dtype)
    uu2 = _np.zeros(N, dtype=dtype)
    alpha = _np.zeros(N, dtype=dtype)
    beta = _np.zeros(N, dtype=dtype)
    p = _np.zeros(N, dtype=dtype)
    
    """
    /*  Main  loop, steps here */
    """
    for istep in range(nstep):
        """
        /*  Elimination in the direction i, halfstep  */
        """
        Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
        
        for j in range(1, N-1):
            uij = Fout.field[j, 1:N-1]
            uij1 = Fout.field[j+1, 1:N-1]
            uij_1 = Fout.field[j-1, 1:N-1]
            p[1:N-1] = -1/delta2 * (uij_1 + uij1 -2.0 * uij) + imPi4lz * uij
            
            elim(N, a, b, CCX[j,:], p, uu, alpha, beta)
            
            Fout.field[j-1, :] = uu2[:] #apply result from previous elim!
            uu2[:] = uu[:] #store this elim for next application
            # this is necessary to not overwrite the data used in the next
            # elim step
        
        Fout.field[N-1, :] = uu2[:] #apply final elim in this direction
        
        Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
        Fout.field *= expfi4 #twice makes it 0.5*k*dz*(n-1)
        
        """
        /* Elimination in the j direction is here, halfstep */
        """
        uu2[:] = 0.0
        
        for i in range(1, N-1):
            uij = Fout.field[1:N-1, i]
            ui1j = Fout.field[1:N-1, i+1]
            ui_1j = Fout.field[1:N-1, i-1]
            p[1:N-1] = -1/delta2 * (ui_1j + ui1j -2.0 * uij) + imPi4lz * uij
            
            elim(N, a, b, CCY[:,i], p, uu, alpha, beta)
            
            Fout.field[:, i-1] = uu2[:]
            uu2[:] = uu[:]
        
        #TODO BUG! why are we accessing i here? out of scope. Last value:
        #resulting from for(ii in range(1, N-2, 2))
        # -> last ii in loop is int((N-2)/2)*2-1
        # and i=ii+1
        # -> i_final = int((N-2)/2)*2-1+1 = int((N-2)/2)*2
        # tested OK for even and odd N -> works for all N
        i = int((N-2)/2)*2
        #TODO also, why 0:N-1 where all else is 0:N?
        Fout.field[0:N-1, i] = uu2[1:N]
    """
    ///* end j */
    """
    #TODO should this be in nstep loop??
    # seems so, that would add up to 1*ikz*n, right now its 3/4*ikz per iter
    # and a final 1/4 ??
    Fout.field *= expfi4 #*=_np.exp(1j*(0.25*K*dz*(refr.real-1.0)))
    Fout._IsGauss=False
    return Fout


def _TODOStepsScipy(z, nstep, refr, Fin):
    """Right now this is just a test and collection of code from
    https://scipy-cookbook.readthedocs.io/items/discrete_bvp.html
    which is not functional for Lightpipes!
    Also, its really really slow, so possibly not useful at all.
    """

    if Fin._curvature != 0.0:
        raise ValueError('Cannot operate on spherical coords.'
                         + 'Use Convert() first')
    Fout = Field.copy(Fin)
    N = Fout.N
    lam = Fout.lam
    size = Fout.siz
    dtype = Fout._dtype
    
    legacy = True
    if legacy:
        Pi = 3.141592654 #to compare Cpp results accurately
    else:
        Pi = _np.pi
    K = 2.*Pi/lam
    z = z/2.
    Pi4lz = 4.*Pi/lam/z
    imPi4lz = 1j * Pi4lz
    
    delta = size/(N-1.) #dx
    delta2 = delta*delta
    
    n = 100
    c = 1
    # n = N
    # c = delta**2
    def f(u, ):
        return u**3
    
    def f_prime(u):
        return 3 * u**2
    
    def fun(u, n, f, f_prime, c, **kwargs):
        v = _np.zeros((n + 2, n + 2))
        u = u.reshape((n, n))
        v[1:-1, 1:-1] = u
        y = v[:-2, 1:-1] + v[2:, 1:-1] + v[1:-1, :-2] + v[1:-1, 2:] - 4 * u + c * f(u)
        return y.ravel()

    def compute_jac_indices(n):
        i = _np.arange(n)
        jj, ii = _np.meshgrid(i, i)
    
        ii = ii.ravel()
        jj = jj.ravel()
    
        ij = _np.arange(n**2)
    
        jac_rows = [ij]
        jac_cols = [ij]
    
        mask = ii > 0
        ij_mask = ij[mask]
        jac_rows.append(ij_mask)
        jac_cols.append(ij_mask - n)
    
        mask = ii < n - 1
        ij_mask = ij[mask]
        jac_rows.append(ij_mask)
        jac_cols.append(ij_mask + n)
    
        mask = jj > 0
        ij_mask = ij[mask]
        jac_rows.append(ij_mask)
        jac_cols.append(ij_mask - 1)
    
        mask = jj < n - 1
        ij_mask = ij[mask]
        jac_rows.append(ij_mask)
        jac_cols.append(ij_mask + 1)
    
        return _np.hstack(jac_rows), _np.hstack(jac_cols)
    jac_rows, jac_cols = compute_jac_indices(N)
    # u0 = np.ones(n**2) * 0.5
    u0 = Fin.field.ravel() #initial guess is old field
    
    def jac(u, n, f, f_prime, c, jac_rows=None, jac_cols=None):
        jac_values = _np.ones_like(jac_cols, dtype=float)
        jac_values[:n**2] = -4 + c * f_prime(u)
        return coo_matrix((jac_values, (jac_rows, jac_cols)),
                          shape=(n**2, n**2))
    
    res_1 = least_squares(fun, u0.real, jac=jac, gtol=1e-3,
                          args=(N, f, f_prime, c),
                          kwargs={'jac_rows': jac_rows,
                                  'jac_cols': jac_cols},
                          verbose=0)
    # print(res_1)
    Fout.field = res_1.x.reshape((N, N))
    Fout._IsGauss=False
    return Fout





