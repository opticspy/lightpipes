# -*- coding: utf-8 -*-
"""
User defined functions for LightPipes for Python

"""
import numpy as _np
from scipy.optimize import fsolve
from .field import Field
from .core import BeamMix, CircAperture

def RowOfFields(Fin,Ffield,Nfields,sep,y=0.0):
    """
    *Inserts an row of fields in the field*
    
    :param Fin: input field
    :type Fin: Field 
    :param Ffield: field to be inserted
    :type Ffield: Field, numpy.ndarray 
    :param Nfields: number of inserted field in x-direction
    :type Nfields: int, float
    :param sep: separation of the inserted fields in the x-direction
    :type sep: int, float
    :param y: position of the row in the y-direction (Default = 0.0)
    :type y: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:
    
    >>> #Insert a row of fields or numpy arrays in the input field at y (Default=0.0):    
    >>> F=Begin(size,wavelength,N)
    >>> #Define the field, Ffield, to be inserted:
    >>> Nfield=int(size_field/size*N)
    >>> Ffield=Begin(size_field,wavelength,Nfield)
    >>> Ffield=CircAperture(Ffield,Dlens/2)
    >>> Ffield=Lens(Ffield,f)
    >>> #Insert the Ffield's in the field F:
    >>> F=RowOfFields(F,Ffield,Nfields,sep)
    >>> Ifields=Intensity(F)
    
    .. seealso::
        
        * :ref:`Examples: Multi- holes and slits. <Multi- holes and slits.>`
    
    """
    if (Nfields+1)*sep > Fin.siz:
       print('Field to be inserted does not fit in input field')
       exit(1)
    Fout = Field.copy(Fin)
    Fout.field*=0.0
    isField=False
    if isinstance(Ffield, Field):
        isField=True
        Nfieldx=Ffield.N
        Nfieldy=Ffield.N
    else:
        Nfieldy, Nfieldx = Ffield.shape
    ch=int(Nfieldy/2)
    cw=int(Nfieldx/2)
    N2=int(Fin.N/2)
    for i in range(0,Nfields):
        if (Nfields %2) == 0.0:
            sx=(i+1/2-int(Nfields/2))*sep
        else:
            sx=(i-int(Nfields/2))*sep
        sy=y
        Nx=-int(sx/Fin.siz*Fin.N)
        Ny=int(sy/Fin.siz*Fin.N)
        Nx_field=N2-cw-Nx
        Ny_field=N2-ch-Ny
        if isField:
            Fout.field[Ny_field:Ny_field+Nfieldy, Nx_field:Nx_field+Nfieldx]=Ffield.field
        else:
            Fout.field[Ny_field:Ny_field+Nfieldy, Nx_field:Nx_field+Nfieldx]=Ffield
    return Fout


 
def FieldArray2D(Fin,Ffield,Nfieldsx,Nfieldsy,x_sep,y_sep):
    """
    *Inserts an array of fields in the field*
    
    :param Fin: input field
    :type Fin: Field 
    :param Ffield: field to be inserted
    :type Ffield: Field  
    :param Nfieldsx: number of inserted field in x-direction
    :type Nfieldsx: int, float
    :param Nfieldy: number of inserted field in y-direction
    :type Nfieldy: int, float
    :param x_sep: separation of the inserted fields in the x-direction
    :type x_sep: int, float
    :param y_sep: separation of the inserted fields in the y-direction
    :type y_sep: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> #Insert an array of lenses in the field    
    >>> F=Begin(size,wavelength,N)
    >>> #Define the field, Ffield, to be inserted:
    >>> Nfield=int(size_field/size*N)
    >>> Ffield=Begin(size_field,wavelength,Nfield)
    >>> Ffield=CircAperture(Ffield,Dlens/2)
    >>> Ffield=Lens(Ffield,f)
    >>> #Insert the Ffield's in the field F:
    >>> F=FieldArray2D(F,Ffield,Nfields,Nfields,x_sep,y_sep)
    >>> Ifields=Intensity(F)
    
    .. seealso::
        
        * :ref:`Examples: Shack Hartmann sensor <Shack Hartmann sensor.>`
    """

    Fout = Field.copy(Fin)
    F = _np.ndarray((Nfieldsy,),dtype=_np.object)
    F[0]=Ffield
    if (Nfieldsy %2) == 0:
        Nfieldsy2=int(Nfieldsy/2)
        ys=(1/2-Nfieldsy2)*y_sep
    else:
        Nfieldsy2=int((Nfieldsy-1)/2)
        ys=-Nfieldsy2*y_sep        
    F[0]=RowOfFields(Fin,Ffield,Nfieldsx,x_sep,ys)
    for i in range(1,Nfieldsy):
        if (Nfieldsy %2) == 0:
            ys=(i+1/2-Nfieldsy2)*y_sep
        else:
            ys=(i-Nfieldsy2)*y_sep
        F[i]=RowOfFields(Fin,Ffield,Nfieldsx,x_sep,ys)
        F[i]=BeamMix(F[i-1],F[i])
    Fout=F[Nfieldsy-1]
    return Fout
    
def CylindricalLens(Fin,f,x_shift=0.0,y_shift=0.0,angle=0.0):
    """
    *Inserts a cylindrical lens in the field*
    
    :param Fin: input field
    :type Fin: Field  
    :param f: focal length
    :type f: int, float
    :param x_shift: shift in the x-direction (default = 0.0)
    :type x_shift: int, float
    :param y_shift: shift in the y-direction (default = 0.0)
    :type y_shift: int, float
    :param angle: rotation angle (default = 0.0, horizontal)
    :type angle: int, float    
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F=Begin(size,wavelength,N)
    >>> F=CylindricalLens(F,f) #Cylindrical lens in the center
    >>> F=CylindricalLens(F,f, x_shift=2*mm) #idem, shifted 2 mm in x direction
    >>> F=CylindricalLens(F,f, x_shift=2*mm, angle=30.0*deg) #idem, rotated 30 degrees
    
    .. seealso::
        
        * :ref:`Examples: Transformation of high order Gauss modes <Transformation of high order Gauss modes.>`
    """
    Fout = Field.copy(Fin)
    k = 2*_np.pi/Fout.lam
    yy, xx = Fout.mgrid_cartesian
    xx -= x_shift
    yy -= y_shift
    if angle!=0.0:
        cc = _np.cos(angle)
        ss = _np.sin(angle)
        xx = cc * xx + ss * yy
    fi = -k*(xx**2)/(2*f)
    Fout.field *= _np.exp(1j * fi)
    return Fout

def ZonePlate(Fin, N_zones,f=None, p=None,q=None, T=1.0, PassEvenZones=True ):
    Fout = Field.copy(Fin)
    Y, X = Fout.mgrid_cartesian
    T=_np.sqrt(T)
    
    R = _np.sqrt( X**2 + Y**2) #squared, no need for sqrt
    if (not f==None) and (p==None) and (q==None):
        Rzone=_np.zeros(N_zones+1)
        for n in range(1,N_zones+1):
            Rzone[n] = _np.sqrt(n * Fout.lam * f + ((n * Fout.lam)**2)/4)
            if PassEvenZones:
                if (n % 2)==0.0:
                    Fout.field[R>=Rzone[n-1]]=Fin.field[R>=Rzone[n-1]]*T
                else:
                    Fout.field[R>=Rzone[n-1]]=0.0
            else:
                if not (n % 2)==0.0:
                    Fout.field[R>=Rzone[n-1]]=Fin.field[R>=Rzone[n-1]]*T
                else:
                    Fout.field[R>=Rzone[n-1]]=0.0
        w=Rzone[N_zones]-Rzone[N_zones-1]
    elif (not p==None) and (not q==None) and (f==None):
        def get_r(p,q,n):
            c=p+q+n*Fout.lam/2
            def equations(P):
                x,y,r=P
                F=_np.empty(3)
                F[0]=x-_np.sqrt(p**2+r**2)
                F[1]=y-_np.sqrt(q**2+r**2)
                F[2]=x+y-c
                return F
            r=fsolve(equations,(1,1,1))[2]
            return r
        Rzone=_np.zeros(N_zones+1)
        for n in range(1,N_zones+1):
            # Rzone[n]=((n*Fout.lam)**4)/16 +\
                     # (((n*Fout.lam)**3)*(p+q))/2 +\
                     # ((n*Fout.lam)**2)*(p*q+(p+q)**2) +\
                     # 4*n*Fout.lam*q*(p+q)
            # Rzone[n]/=4*(p+q)*(n*Fout.lam+p+q)+(n*Fout.lam)**2
            # Rzone[n]=_np.sqrt(Rzone[n])
            Rzone[n] = get_r(p,q,n)
            if PassEvenZones:
                if (n % 2)==0.0:
                    Fout.field[R>=Rzone[n-1]]=Fin.field[R>=Rzone[n-1]]*T
                else:
                    Fout.field[R>=Rzone[n-1]]=0.0
            else:
                if not (n % 2)==0.0:
                    Fout.field[R>=Rzone[n-1]]=Fin.field[R>=Rzone[n-1]]*T
                else:
                    Fout.field[R>=Rzone[n-1]]=0.0
        w=Rzone[N_zones]-Rzone[N_zones-1]
        Fout=CircAperture(Fout,Rzone[N_zones])
    else:
        print("Error in ZonePlate: either the focal length, 'f',  or the object- and image distances, 'p and q', must be given.")
        exit(1)                
    return Fout,w
