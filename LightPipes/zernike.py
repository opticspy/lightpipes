# -*- coding: utf-8 -*-

import numpy as _np
from .field import Field
from .core import Phase, PhaseUnwrap, Intensity
from .zernikemath import zernike
from .misc import backward_compatible

@backward_compatible
def Zernike(Fin, n, m, R, A = 1.0, norm=True, units='opd'):
    """
    *Substitutes a Zernike aberration phase distribution in the field.*
        
    :math:`F_{out}(x,y)=e^{\\phi^m_n (x,y)}F_{in}(x,y)`
    
     with:
    
    :math:`\\phi^m_n(x,y)=-j \\frac{2 \\pi }{ \\lambda } Z^m_n {(\\rho (x,y) ,\\theta (x,y)) }`
    
    :math:`\\rho(x,y)=  \\sqrt{ \\frac{x^2+y^2}{R^2} }`
    
    :math:`\\theta (x,y)=atan \\big( \\frac{y}{x} \\big)`
    
    :math:`Z^m_n(\\rho , \\theta)=A \\sqrt{ \\frac{2(n+1)}{1+\\delta_{m0}} } V^m_n(\\rho)cos(m\\theta)`
    
    :math:`Z^{-m}_n(\\rho , \\theta)=A \\sqrt{ \\frac{2(n+1)}{1+\\delta_{m0}} }V^m_n(\\rho)sin(m\\theta)`
    
    :math:`V^m_n(\\rho)= \\sum_{s=0}^{ \\frac{n-m}{2} }  \\frac{(-1)^s(n-s)!}{s!( \\frac{n+m}{2}-s)!( \\frac{n-m}{2}-s )! } \\rho^{n-2s}`
    
    :math:`\\delta_{m0}= \\begin{cases}1 & m = 0\\\\0 & m  \\neq  0\\end{cases}`
        
    :param Fin: input field
    :type Fin: Field
    :param n: radial order
    :type n: int, float
    :param m: azimuthal order, n-\\|m\\| must be even, \\|m\\|<=n
    :type m: int, float    
    :param R: radius of the aberrated aperture
    :type R: int, float
    :param A: size of the aberration
    :type A: int, float
    :param norm: if True, normalize integral(Z over unit circle)=1, if False
                Z(rho=1)=1 on edge (-> True=rms const, False=PtV const) (default = True)
    :type norm: bool
    :param units: 'opd': A given in meters as optical path difference (default = 'opd')
                'lam': A given in multiples of lambda
                'rad': A given in multiples of 2pi
    :type units: string
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
        if norm=True and Aunit='lambda' and A=1.0, the wavefront
        will have an rms error of 1lambda, but PtV depending on n/m.
        If norm=False and Aunit='lambda' and A=1.0, the wavefront will
        have a PtV value of 2lambda (+ and -1 lambda!), but rms error
        depending on n/m.

    .. seealso::
    
        * :ref:`Manual: Zernike polynomials.<Zernike polynomials.>`
        * :ref:`Examples: Zernike aberration.<Zernike aberration.>`
        * `https://en.wikipedia.org/wiki/Zernike_polynomials <https://en.wikipedia.org/wiki/Zernike_polynomials>`_
    """
    mcorrect = False
    ncheck = n
    while ncheck >= -n:
        if ncheck == m:
            mcorrect = True
        ncheck -= 2
    if not mcorrect:
        raise ValueError('Zernike: n,m must fulfill: n>0, |m|<=n and n-|m|=even')
        
    Fout = Field.copy(Fin)
    
    
    k = 2*_np.pi/Fout.lam
    
    if units=='opd':
        A = k*A #if A=1e-6 [==1um~1lambda], this will yield 2pi/lam*1um, e.g. 1lambda OPD
    elif units=='lam':
        A = 2*_np.pi*A #if A=1, this will yield 1 lambda OPD
    elif units=='rad':
        A = A #if A=2pi, this will yield 1lambda OPD
    else:
        raise ValueError('Unknown value for option units={}'.format(units))
    
    if norm:
        if m==0:
            # wikipedia has modulo Pi? -> ignore for now
            # keep backward compatible and since not dep. on n/m irrelevant
            Nnm = _np.sqrt(n+1)
        else:
            Nnm = _np.sqrt(2*(n+1))
    else:
        Nnm = 1
    
    r, phi = Fout.mgrid_polar
    rho = r/R
    fi = -A*Nnm*zernike(n,m, rho, phi)
    Fout.field *= _np.exp(1j*fi)
    return Fout


def ZernikeFit(F, j_terms, R,  norm=True, units='lam'):
    """
    *Fit the first N terms (Noll indexing) to the given Field.*
    
    :param F: input field
    :type F: Field
    :param j_terms: if j_terms is a number, first j_terms terms will be fitted if j_terms is a collection (list, array), each number should represent one noll index to fit.
    :type j_terms: int, float, list array
    :param R: beam radius on which the Zernike coefficients should be defined.
    :type R: int,float
    :param norm: if True normalization (default = True)
    :param units: 'opd': A given in meters as optical path difference 
                'lam': A given in multiples of lambda (default = 'lam')
                'rad': A given in multiples of 2pi
    
    :return: (j_terms, A_fits) 
    :rtype: tuple of int, float
    
    The phase will be ignored at points with low intensity, but should unwrap
    correctly in valid region.
    
    Piston term (j=1 / n,m=0) is always necessary for fitting but generally
    meaningless in the result.
    """
    Ph = Phase(F, unwrap=True, units=units, blank_eps=1e-3) #blank phase where not well defined

    A = 1 #[a.u.] since reference amplitude is 1, coeffs from leastsq will
        # automatically have the correct units
    
    j_terms = _np.asarray(j_terms)
    if j_terms.ndim == 0:
        j_terms = _np.arange(1,j_terms+1)
    else:
        if not 1 in j_terms:
            j_terms = _np.array([1, *j_terms]) #always need the piston
    
    #Debug only filtered piston, but having it should always be allowed
    # if 1 in j_terms:
    #     j_terms = j_terms[j_terms != 1]
    
    zerns_to_fit = []
    for j_noll in j_terms:
        n, m = noll_to_zern(j_noll)
        if norm:
            if m==0:
                # wikipedia has modulo Pi? -> ignore for now
                # keep backward compatible and since not dep. on n/m irrelevant
                Nnm = _np.sqrt(n+1)
            else:
                Nnm = _np.sqrt(2*(n+1))
        else:
            Nnm = 1
        
        r, phi = F.mgrid_polar
        rho = r/R
        PhZ = -A*Nnm*zernike(n,m, rho, phi)
        zerns_to_fit.append(PhZ)
    b = Ph[~_np.isnan(Ph)] #select only non-NaN
    AA = _np.column_stack([PhZ[~_np.isnan(Ph)] for PhZ in zerns_to_fit])
    A_fits, res, rank, s = _np.linalg.lstsq(AA, b, rcond=None)
    # assert rank==j_terms.size #since Zernikes orthogonal by definition
    # assert _np.alltrue(s>1) #again, since always orthogonal
    # return (j_terms, A_fits, res, rank, s)
    return (j_terms, A_fits)


def ZernikeFilter(F, j_terms, R):
    """
    *Compute the input field's wavefront, filter out the specified
    Zernike orders and return the field with filtered wavefront.*
    
    :param F: input field
    :type F: Field
    :param j_terms: iterable of int which terms to filter. Given in Noll notation.
    :type j_terms: float, int
    :param R: radius of Zernike definition
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    
    """
    j_terms, A_fits = ZernikeFit(j_terms, R, F, norm=True, units='rad')
    # print(A_fits.round(4))
    # Ph = Phase(F, unwrap=True)
    Ph = _np.zeros_like(F.field)
    for idx in range(len(j_terms)):
        j_noll = j_terms[idx]
        A_i = A_fits[idx] #amplitude for this abberation in rad
            # -> no need to convert
        
        n, m = noll_to_zern(j_noll)
        if m==0:
            # wikipedia has modulo Pi? -> ignore for now
            # keep backward compatible and since not dep. on n/m irrelevant
            Nnm = _np.sqrt(n+1)
        else:
            Nnm = _np.sqrt(2*(n+1))
            
        r, phi = F.mgrid_polar
        rho = r/R
        Ph_i = -A_i*Nnm*zernike(n,m, rho, phi)
        # Ph -= Ph_i
        Ph += Ph_i
    
    Fout = F
    Fout.field *= _np.exp(-1j * Ph)
    # Fout = Field.copy(F)
    # Fout = SubPhase(Ph, Fout)
    return Fout
    

def ZernikeName(Noll):
    """
    *Returns the name of Zernike Noll term*
    
    :param Noll: Noll term (1 .. 21)
    :type Noll: int, float
    :return: name of Noll Zernike term
    :rtype: string
    
    .. seealso::
    
        * :ref:`Examples: Zernike aberration.<Zernike aberration.>`
    """
    if (Noll >= 1 and Noll <= 21):
        name = [
            "piston",
            "horizontal tilt",
            "vertical tilt",
            "defocus",
            "oblique primary astigmatism",
            "vertical primary astigmatism",
            "vertical coma",
            "horizontal coma",
            "vertical trefoil",
            "oblique trefoil",
            "primary spherical",
            "vertical secondary astigmatism",
            "oblique secondary astigmatism",
            "vertical quadrafoil",
            "oblique quadrafoil",
            "horizontal secondary coma",
            "vertical secondary coma",
            "oblique secondary trefoil",
            "vertical secondary trefoil",
            "oblique pentafoil",
            "vertical pentafoil",
        ]
        return name[Noll-1]
    elif Noll < 1:
        print( "Error in ZernikeName(Noll): argument must be larger than 1")
        return ""
    else:
        return ""


def noll_to_zern(j):
    """
    *Convert linear Noll index to tuple of Zernike indices.*
    
    :param j: the linear Noll coordinate, n is the radial Zernike index and m is the azimuthal Zernike index.
    :type j: int, float
    :return: name of Noll Zernike term
    :rtype: string (n, m) tuple of Zernike indices
    
    .. seealso::
    
        * :ref:`Manual: Zernike polynomials.<Zernike polynomials.>`
        * `https://oeis.org <https://oeis.org/A176988>`_
        * `Tim van Werkhoven, https://github.com/tvwerkhoven <https://github.com/tvwerkhoven>`_
        * :ref:`Examples: Zernike aberration.<Zernike aberration.>`
    """

    if (j == 0):
        raise ValueError("Noll indices start at 1, 0 is invalid.")

    n = 0
    j1 = j-1
    while (j1 > n):
        n += 1
        j1 -= n

    m = (-1)**j * ((n % 2) + 2 * int((j1+((n+1)%2)) / 2.0 ))
    return (n, m)

def ZernikeNolltoMN(Noll):
    #TODO not documented publicly -> private/unused/untested??
    #also, seems to give wrong results, test with:
    #[print(ZernikeNolltoMN(j)) for j in range(0,7)];
    # -> starts at 0, which is not correct
    # -> ordering for e.g. n=2 is (-2,2)(0,2)(2,2) which is oppsosite of Noll
    # -> returning [m,n] instead of (n,m) seems weird
    MN = []
    n = 0
    while (Noll > n):
        n += 1
        Noll -= n
    m = -n+2*Noll
    MN=[m,n]
    return MN


