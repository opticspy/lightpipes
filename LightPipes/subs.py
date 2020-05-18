# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 19:55:44 2020

@author: Lenny
"""

from math import pi as Pi
import numpy as _np

def H(n, x):
    """
    Used for GaussHermite

    Parameters
    ----------
    n : int
        DESCRIPTION.
    x : double
        DESCRIPTION.

    Returns
    -------
    double.

    """
    # int k;
    # double p1,p2,p3;
    p1=1.0
    p2=0.0
    if (n == 0 ):
        return 1.0
    """
    for (k=1;k <=n; k++):{
       p3=p2;
       p2=p1;
       p1=2*x*p2-2*(k-1)*p3;
    }
    return p1"""
    pass

def Laguerre1(p, m, rho):
    """
    

    Parameters
    ----------
    p : int
        DESCRIPTION.
    m : int
        DESCRIPTION.
    rho : double
        DESCRIPTION.

    Returns
    -------
    double.

    """
    """CPP
    if (p==0) return 1.0;
    else
        if (p==1) return -1*rho+1+m;
        else
            return (2*p+m-1-rho)/p*Laguerre1(p-1,m,rho) - (p+m-1)/p*Laguerre1(p-2,m,rho);
    """
    pass

def Laguerre(p, m, rho):
    """
    

    Parameters
    ----------
    p : int
        DESCRIPTION.
    m : int
        DESCRIPTION.
    rho : double
        DESCRIPTION.

    Returns
    -------
    double.

    """
    """CPP
    double L0,L1,LaguerreL;
    int i;
    L1=0.0;
    LaguerreL=1.0;
    for (i=1;i<p+1;i++)
    {
        L0=L1;
        L1=LaguerreL;
        LaguerreL=((2*i-1+m-rho)*L1-(i-1+m)*L0)/i;
    }
    return LaguerreL;
    """
    pass


def Inv_Squares(xn,yn, field, dx):
    """
    
    *         Inverse square interpolation : 
    *         given square (x,y) (x+dx,y) (x,y+dx) (x+dx,y+dx) 
    *         with values   z     zx       zy        zxy 
    *         the program returns value for Z for arbitrary 
    *         xn and yn inside the rectangle.
    * new in Python version: z,zx,etc are taken from given field

    Parameters
    ----------
    xn : float
        Value where to interpolate.
    yn : float
        Value where to interpolate.
    xs : list/ndarray
        List of x values of old field (length N).
    ys : list/ndarray
        List of y values of old field (length N).
    field : complex ndarray NxN
        the complex field source data.

    Raises
    ------
    ValueError
        for coords outside old bounds (xs, ys).

    Returns
    -------
    complex
        Interpolated value.

    """
    #TODO will fail for single value, input must be ndarray for xn, yn
    N = field.shape[0]
    No2 = int(N/2)
    
    II = _np.floor(xn/dx+No2).astype(int)
    JJ = _np.floor(yn/dx+No2).astype(int)
    
    x = (II-No2)*dx #closest smaller x-value for each item in xn
    y = (JJ-No2)*dx
    
    tol = 1e-6*dx
    if (_np.any(xn < x-tol) or _np.any(xn > x+dx+tol) or
        _np.any(yn<y-tol) or _np.any(yn > y+dx+tol)):
        raise ValueError('Out of range')
        #TODO why not return 0.0??
        #TODO this is the wrong check. worked while not passing xs array
        # now we need another way of finding boundary xmin, xmax!
    
    xlow = xn-x
    xhigh = x+dx-xn
    ylow = yn-y
    yhigh = y+dx-yn
    
    if (_np.any(xlow < -tol) or _np.any(xhigh < -tol) or
        _np.any(ylow < -tol) or _np.any(yhigh < -tol)):
        raise ValueError('Out of range')
        #TODO this is the wrong check. worked while not passing xs array
        # now we need another way of finding boundary xmin, xmax!
    
    z = field[JJ, II] #II and JJ same length -> element-wise selection
    zx = field[JJ, II+1]
    zy = field[JJ+1, II]
    zxy = field[JJ+1, II+1]
    
    """Changed from Cpp code to Python:
        Some extra checks were made to avoid div by 0, however it turns
        out re-writing the formulas below one can find an expression which
        avoids the division altogether, probably also making the interpolation
        more stable when having small numbers for xhigh/low/etc.
        -> checks removed
        -> math rephrased to contain mostly multip/addition
    """
    """
    #old Cpp style:
    # if (abs(xlow) < tol):
    #     return z + ylow*(zy-z)/dx
    # if (abs(ylow) < tol):
    #     return z+xlow*(zx-z)/dx
    # if (abs(xhigh) < tol):
    #     return zx+ylow*(zxy-zx)/dx
    # if (abs(yhigh) < tol):
    #     return zy+xlow*(zxy-zy)/dx
    
    # s1=1./(xlow*ylow)
    # s2=1./(xhigh*ylow)
    # s3=1./(xlow*yhigh)
    # s4=1./(xhigh*yhigh)
    # summ = s1+s2+s3+s4
    
    # zout = z*s1 + zx*s2 + zy*s3 + zxy*s4
    # zout /= summ
    """
    
    zout = yhigh * (z*xhigh + zx*xlow)
    zout += ylow * (zy*xhigh + zxy*xlow)
    zout /= dx**2
    return zout


def elim(N, a, b, c, p, uu, alpha, beta):
    """
    elim. Called by LPSteps
    """
    """
    /* initial condition, everything is going to be zero at the edge */
    """
    alpha[0] = 0.0
    beta[0] = 0.0
    
    alpha[N-2] = 0.0
    beta[N-2] = 0.0
    
    """
    //* forward elimination */
    """
    for i in range(1, N-2):
        cc = c[i] - a * alpha[i-1]
        alpha[i] = b / cc
        beta[i]  = (p[i] + a * beta[i-1] ) / cc
    #basically same as one more loop ??:
    cc = c[N-1] - a * alpha[N-2]
    beta[N-1]  = (p[N-1] + a * beta[N-2] ) / cc
    """
    //* edge amplitude =0 */
    """
    uu[N-1] = beta[N-1]
    """
    //* backward elimination        */
    """
    for i in range(N-2, -1, -1):
        uu[i] = alpha[i] * uu[i+1] + beta[i]
        
    pass #modified in place, no return!


def elimH(N, a, b, c, p, UU, alpha, beta):
    """
    elimH. Called by LPSteps
    Double sweep elimination along the horizontal direction, i.e. row-wise
    Inputs NxN arrays or scalars
    """
    """
    /* initial condition, everything is going to be zero at the edge */
    """
    alpha[:,0] = 0.0
    beta[:,0] = 0.0
    
    alpha[:,N-2] = 0.0
    beta[:,N-2] = 0.0
    
    """
    //* forward elimination */
    """
    for i in range(1, N-2):
        cc = c[:,i] - a * alpha[:,i-1]
        alpha[:,i] = b / cc
        beta[:,i]  = (p[:,i] + a * beta[:,i-1] ) / cc
    #basically same as one more loop ??:
    cc = c[:,N-1] - a * alpha[:,N-2]
    beta[:,N-1]  = (p[:,N-1] + a * beta[:,N-2] ) / cc
    """
    //* edge amplitude =0 */
    """
    UU[:,N-1] = beta[:,N-1]
    """
    //* backward elimination        */
    """
    for i in range(N-2, -1, -1):
        UU[:,i] = alpha[:,i] * UU[:,i+1] + beta[:,i]
    pass #modified in place, no return!


def elimV(N, a, b, c, p, uu, alpha, beta):
    """
    elimV. Called by LPSteps
    Double sweep elimination along the vertical direction, i.e. column-wise
    Inputs NxN arrays or scalars
    """
    """
    /* initial condition, everything is going to be zero at the edge */
    """
    alpha[0,:] = 0.0
    beta[0,:] = 0.0
    
    alpha[N-2,:] = 0.0
    beta[N-2,:] = 0.0
    
    """
    //* forward elimination */
    """
    for i in range(1, N-2):
        cc = c[i,:] - a * alpha[i-1]
        alpha[i,:] = b / cc
        beta[i,:]  = (p[i,:] + a * beta[i-1,:] ) / cc
    #basically same as one more loop ??:
    cc = c[N-1,:] - a * alpha[N-2,:]
    beta[N-1,:]  = (p[N-1,:] + a * beta[N-2,:] ) / cc
    """
    //* edge amplitude =0 */
    """
    uu[N-1,:] = beta[N-1,:]
    """
    //* backward elimination        */
    """
    for i in range(N-2, -1, -1):
        uu[i,:] = alpha[i,:] * uu[i+1,:] + beta[i,:]
        
    pass #modified in place, no return!






