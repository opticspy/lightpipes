============
Introduction
============

LightPipes for Python is a set of functions written in C++ available to Python.It is designed to model coherent optical devices when the diffraction is essential.The toolbox consists of a number of functions. Each function represents an optical element or a step in the light propagation. There are apertures, intensity filters,
beam-splitters, lenses and models of free space diffraction in LightPipes.
There are also more advanced tools for manipulating the phase and amplitude of the light.
The program operates on a large data structure, containing square two-dimensional arrays
of complex amplitudes of the optical field of the propagating light beam.
          
See for more details:
https://github.com/FredvanGoor/LightPipes-for-Python
        
LightPipes was made  by Gleb Vdovin for MSDOS and Linux
There are also versions of LightPipes for Matlab, Octave and Mathcad. These can be obtained from:
        
`Flexible Optical <http://www.okotech.com>`_, Rijswijk, The Netherlands.
 
.. figure::  _static/OKO_logo_new.png
               :align:   center

Example:

See: :ref:`Two holes interferometer<young>`

.. code-block:: python

    #Simulation of a two-holes interferometer.   
    import LightPipes as lp
    import matplotlib.pyplot as plt
    m=1
    nm=1e-9*m
    um=1e-6*m
    mm=1e-3*m
    cm=1e-2*m
    try:
        LP=lp.Init()
        wavelength=20*um
        size=30.0*mm
        N=500
        F=LP.Begin(size,wavelength,N)
        F1=LP.CircAperture(0.15*mm, -0.6*mm,0, F)
        F2=LP.CircAperture(0.15*mm, 0.6*mm,0, F)    
        F=LP.BeamMix(F1,F2)
        F=LP.Forvard(10*cm,F)
        I=LP.Intensity(2,F)
        plt.contourf(I,50); plt.axis('equal')
        plt.show()
    finally:
        del lp
