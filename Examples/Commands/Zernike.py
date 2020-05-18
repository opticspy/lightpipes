#!/usr/bin/python
"""
This example demonstrates the Zernike command.
..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

from LightPipes import *
import matplotlib.pyplot as plt

pi=PI


wavelength=500*nm
size=2.0*mm
N=200

#Zernike
mz=-3 #azimuthal order
nz=7 #radial order

F=Begin(size,wavelength,N)
F=Zernike(nz,mz,size/2,wavelength/(2*pi),F)
F=CircAperture(size/2,0,0,F)
Phi=Phase(F)
plt.imshow(Phi,cmap='jet')
s='Zernike Polynomial: $Z^{'+repr(mz)+'}_{'+repr(nz)+'}$'
plt.title(s);plt.axis('off')
plt.show()
