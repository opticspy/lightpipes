# -*- coding: utf-8 -*-
"""

Created on Sun Feb 23 17:53:56 2020

@author: Leonard.Doyle@physik.uni-muenchen.de
"""

import numpy as _np
import copy as _copy

class Field:
    """
    Lightpipes Field object, containing the field data and meta
    parameters as well as helper functions to change data formats etc.
    """
    
    
    @classmethod
    def begin(cls, grid_size, wavelength, N, dtype=None):
        """
        Initialize a new field object with the given parameters.
        This method is preferred over direct calling of constructor.
        

        Parameters
        ----------
        grid_size : float
            [m] physical size of the square grid
        wavelength : float
            [m] physical wavelength
        N : int
            number of grid points in each dimension (square)
        dtype : dtype
            complex dtype to use

        Returns
        -------
        The initialized Field object.

        """
        inst = cls(None, grid_size, wavelength, N, dtype)
        return inst
        
    @classmethod
    def copy(cls, Fin):
        """
        Create a copy of the input field with identical values but
        no common references to numpy fields etc.

        Parameters
        ----------
        Fin : Field
            Input field to copy/clone

        Returns
        -------
        A new Field object with identical values as Fin.

        """
        return _copy.deepcopy(Fin)
        
    @classmethod
    def shallowcopy(cls, Fin):
        """
        Create a shallow copy of the input field, i.e. the parameters are
        cloned but the reference to the numpy field is the same!
        This may be useful if a function (e.g. Fresnel) returns a copied
        field anyways, so a deep copy like Field.copy() would be redundant.

        Parameters
        ----------
        Fin : Field
            Input field to copy (common reference to .field!)

        Returns
        -------
        A new Field object with identical values as Fin and common reference
        to .field

        """
        return _copy.copy(Fin)
    
    def __init__(self, Fin=None, grid_size=1.0, wavelength=1.0, N=0, dtype=None):
        """Private, use class method factories instead."""
        
        if dtype in (complex, _np.complex64, _np.complex128):
            self._dtype = dtype
        else:
            if dtype is None:
                self._dtype=complex
            else:
                print("Begin command: invalid dtype given, dtype must be complex, numpy.complex128 or numpy.complex64. dtype is set to: complex")
                self._dtype = complex

        if Fin is None:
            if not N:
                raise ValueError('Cannot create zero size field (N=0)')
            Fin = _np.ones((N,N),dtype=self._dtype)
        else:
            Fin = _np.asarray(Fin, dtype=self._dtype)
        self._field = Fin
        self._lam = wavelength
        self._siz = grid_size
        self._int1 = 0 #remembers PipFFT direction
        self._curvature = 0.0 #remembers field curvature or 0.0 for normal
        self._IsGauss = False
        self._w0 = 0.2*grid_size
        self._q = -1j* _np.pi*self._w0*self._w0/wavelength
        self._z = 0.0
        self._A = 1.0
        self._n = 0
        self._m = 0
    
    def _get_grid_size(self):
        """Get or set the grid size in [m]."""
        return self._siz
    
    def _set_grid_size(self, gridsize):
        self._siz = gridsize
    
    grid_size = property(_get_grid_size, _set_grid_size)
    siz = grid_size
    
    def _get_wavelength(self):
        """Get or set the wavelength of the field. All units in [m]."""
        return self._lam
    
    def _set_wavelength(self, wavelength):
        self._lam = wavelength
    
    wavelength = property(_get_wavelength, _set_wavelength)
    lam = wavelength
    
    @property
    def grid_dimension(self):
        return self._field.shape[0] #assert square
    
    N = grid_dimension
    
    
    @property
    def grid_step(self):
        """Distance in [m] between 2 grid points"""
        return self.siz/self.N
    
    dx = grid_step
    
    @property
    def field(self):
        """Get the complex E-field."""
        return self._field
    
    @field.setter
    def field(self, field):
        """The field must be a complex 2d square numpy array.
        """
        field = _np.asarray(field, dtype=self._dtype)
        #will not create a new instance if already good
        self._field = field


    @property
    def xvalues(self):
        """
        Return a 1d numpy array of the cartesian X coordinates for the pixels
        of the field.
        
        Following the matplotlib.pyplot.imshow convention:
        - positive shift in x is right
        - positive shift in y is down
        - coords define pixel center, so extent will be
            [xmin-1/2dx, xmax+1/2dx]
        For an odd number of pixels this puts a pixel in the center as expected
        for an even number, the "mid" pixel shifts right and down by 1

        Returns
        -------
        A 1d numpy array of each pixels center x-coordinate

        """
        w = self.N
        cx = int(w/2)
        xvals = self.dx * _np.arange(-cx, (w-cx))
        return xvals


    @property
    def yvalues(self):
        """
        Return a 1d numpy array of the cartesian Y coordinates for the pixels
        of the field.
        
        Following the matplotlib.pyplot.imshow convention:
        - positive shift in x is right
        - positive shift in y is down
        - coords define pixel center, so extent will be
            [xmin-1/2dx, xmax+1/2dx]
        For an odd number of pixels this puts a pixel in the center as expected
        for an even number, the "mid" pixel shifts right and down by 1

        Returns
        -------
        A 1d numpy array of each pixels center y-coordinate

        """
        h = self.N
        cy = int(h/2)
        yvals = self.dx * _np.arange(-cy, (h-cy))
        return yvals

    
    @property
    def mgrid_cartesian(self):
        """Return a meshgrid tuple (Y, X) of cartesian coordinates for each 
        pixel of the field.
        
        Following the matplotlib.pyplot.imshow convention:
        - positive shift in x is right
        - positive shift in y is down
        - coords define pixel center, so extent will be
            [xmin-1/2dx, xmax+1/2dx]
        For an odd number of pixels this puts a pixel in the center as expected
        for an even number, the "mid" pixel shifts right and down by 1
        
        """
        
        """LightPipes manual/ examples Matlab and Python version:
            plotting the Intensity with imshow() yields coord sys:
                positive shift in x is right
                positive shift in y is down!!
            -> stick to this convention where possible
        
        Adapted from matplotlib.imshow convention: coords define pixel center,
        so extent will be xmin-1/2dx, xmax+1/2dx
        For an odd number of pixels this puts a pixel in the center as expected
        for an even number, the "mid" pixel shifts right and down by 1
        """
        h, w = self.N, self.N
        cy, cx = int(h/2), int(w/2)
        Y, X = _np.mgrid[:h, :w]
        Y = (Y-cy)*self.dx
        X = (X-cx)*self.dx
        return (Y, X)


    @property
    def mgrid_Rsquared(self):
        """Return a meshgrid of radius R**2 in polar coordinates for each
        pixel in the field."""
        Y, X = self.mgrid_cartesian
        return X**2+Y**2


    @property
    def mgrid_R(self):
        """Return a meshgrid of radius R in polar coordinates for each
        pixel in the field."""
        #often phi might not be required, no need to calc it
        return _np.sqrt(self.mgrid_Rsquared)


    @property
    def mgrid_polar(self):
        """Return a meshgrid tuple (R, Phi) of polar coordinates for each
        pixel in the field (matching legacy LP convention)."""
        Y, X = self.mgrid_cartesian
        r = _np.sqrt(X**2+Y**2)
        phi = _np.arctan2(Y, X) + _np.pi
        return (r, phi)


