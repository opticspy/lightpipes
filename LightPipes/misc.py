# -*- coding: utf-8 -*-

import numpy as _np
import functools

from .field import Field

PI=_np.pi
def backward_compatible(fn):
    """Decorator to wrap new-convention (field first) LP methods to also
    accept old convention (field last).
    This decorator should work for any new-convention functions that
    only changed the order of the field. If the order or number of other
    arguments has also changed, this decorator might fail and one has to
    manually take care of the order inside that function!
    
    If the user supplies only positional arguments (without keyword), the
    field is searched as first argument for new-convention functions. If not
    found, the field is searched as last argument (old convention) and swapped
    to front if found. If neither first nor last, an error is raised.
    
    The handling of all possible combinations of positional and keyword-
    supplied arguments is tricky, so it might fail in rare occasions/
    strange use cases (e.g. someone supplying kwargs even though all args
    are given and in the correct order).
    Therefore, if at least one argument is supplied via keyword and the first
    positional argument is not a field, an error is raised (swapping would be
    guessing). The solution is to either provide all positional, all keyword
    or update to new syntax putting Field as first argument.
    
    Example new-convention definition:
    @backward_compatible
    def CircScreen(Fin, R, x_shift=0, y_shift=0):
        #old convention was
        # CircScreen(R, x_shift, y_shift, Fin)
    
    Valid function calls then are:
        F = CircScreen(F, 1, 0, 0) #new style, all positional
        F = CircScreen(F, 1) #new style, all positional, some default value
        F = CircScreen(F, 1, y_shift=1) #new style, some default, some kwarg
        
        F = CircScreen(1, 0, 0, F) #old style, all positional
        F = CircScreen(R=1, x_shift=0, y_shift=0, Fin=F) #old, all kwargs
        
        F = CircScreen(R=1, x_shift=0, Fin=F, y_shift=0) #...
            # all kwargs, order irrelevant
    
    Invalid function calls (resolving cannot be guaranteed by decorator):
        F = CircScreen(1, 0, 0, Fin=F) #old style, at least one kwarg
        F = CircScreen(1, F, 0, 0) #plain wrong, neither old nor new style
    
    Grey area:
        F = CircScreen(1, F) #old style part positional, part default value
            #interestingly, this will not raise an error in decorator
            # but might fail in the function call since order not clear
    """
    @functools.wraps(fn)
    def fn_wrapper(*args, **kwargs):
        args = list(args) #make mutable
        if len(kwargs)==0:
            #no keyword args supplied, all args stricly by order/positional
            # -> easy, this decorator won't fail
            if not isinstance(args[0], Field):
                #first arg is not a field, either backward compat syntax or
                # complete usage error -> find out if Field is last, else error
                if isinstance(args[-1], Field):
                    #found field in last arg, push last arg to first:
                    args.insert(0, args.pop()) #[1,2,3,4] -> [4, 1, 2, 3]
                    #-> now all the variables contain what is expected in new style
                else:
                    raise ValueError(fn.__name__ + '(backward compatibility'
                                     + ' check): Field is neither first'
                                     + ' nor last parameter, please check '
                                     + 'syntax/usage.')
        else:
            if len(args)>0:
                #at least one argument is supplied by explicitly naming it,
                # while others are positiobal args.
                # In this case flipping the order or the rest seems
                # dangerous/wrong/unpredictable
                if isinstance(args[0], Field):
                    #all good, Field still first even though kwargs later
                    pass
                else:
                    raise ValueError(fn.__name__ + ' (backward comaptibility'
                                     + ' check): Field not first and kwargs '
                                     + 'used, please update to new '
                                     + 'syntax/usage.')
        
        return fn(*args, **kwargs)
    
    return fn_wrapper
@backward_compatible
def Gain(Fin, Isat, alpha0, Lgain) :
    """
    *Propagates the field through a thin saturable gain sheet.*
        
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
    
    :param Fin: input field
    :type Fin: Field
    :param Isat: saturation intensity
    :type Isat: int, float
    :param alpha0: small signal gain
    :type alpha0: int, float
    :param Lgain: length of the gain medium
    :type Lgain: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> Isat=131*W/cm/cm; alpha=0.0067/cm; Lgain=30*cm;
    >>> F = Gain(F, Isat, alpha, Lgain) # amplifacation of the field
    
    .. seealso::
    
        * :ref:`Examples: Unstable laser resonator <Unstable laser resonator.>`
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

@backward_compatible
def PipFFT(Fin, index = 1 ):
    """
    *Performs a 2D Fourier transform of the field.*
    
    :param Fin: input field
    :type Fin: Field
    :param index: 1 = forward transform, -1 = back transform (default = 1)
    :type index: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = PipFFT(F) # forward transform
    >>> F = PipFFT(F, -1) # back transform
    
    .. seealso::
    
        * :ref:`Manual: FFT and spatial filters.<FFT and spatial filters.>`
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

@backward_compatible
def Tilt( Fin, tx, ty,):
    """
    *Tilts the field.*
    
    :param Fin: input field
    :type Fin: Field
    :param tx: tilt in radians
    :type tx: int, float
    :param ty: tilt in radians
    :type ty: int, float    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> F = Tilt(F, tx = 2*mrad, ty = 1*mrad) # wavefront tilt of 2 mrad in x and 1 mrad in y direction
    >>> F = Tilt(F, 2*mrad, 1*mrad) # Idem
    
    .. seealso::
    
        * :ref:`Examples: Michelson interferometer.<Michelson interferometer.>`
    """

    Fout = Field.copy(Fin)
    yy, xx = Fout.mgrid_cartesian
    k = 2*_np.pi/Fout.lam
    fi = -k*(tx*xx + ty*yy)
    Fout.field *= _np.exp(1j * fi)
    return Fout
