# LightPipes for Python
##Simulations of optical phenomena where diffraction is essential.
*LightPipes for Python* is a set of functions written in C++. It is designed to model coherent optical devices when the diffraction is essential. The toolbox consists of a number of functions. Each function represents an optical element or a step in the light propagation. There are apertures, intensity filters, beam-splitters, lenses and models of free space diffraction. There are also more advanced tools for manipulating the phase and amplitude of the light. The program operates on a large data structure, containing square two-dimensional arrays of complex amplitudes of the optical field of the propagating light beam.
The *LightPipes for Python* routines are modifications of the LightPipes C routines written by Gleb Vdovin for Unix, Linux, DOS and OS2 workstations.
The first step in Python is to import the *LightPipes for Python* library:


Install LightPipes for Python by opening a terminal window and type at the prompt:

###WINDOWS 32 AND 64 BIT:

easy_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/Windows-32-and-64-bits/LightPipes-1.0.0-py2.7-win32.egg

###LINUX 64 BIT:

easy_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/Linux-64-bit/LightPipes-1.0.0-py2.7-linux-x86_64.egg

###LINUX 32 BIT:

easy_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/Linux-32-bit/LightPipes-1.0.0-py2.7-linux-i686.egg

###Test by running (one of) the examples.
For example the Young interferometer ![Young.py](Examples/Young.py).

A plane wave is diffracted by two holes.
![](img/twoholesSetUp.png)

The resulting interference pattern on a screen at distance z looks like:
![](img/twoholesPattern.png)
