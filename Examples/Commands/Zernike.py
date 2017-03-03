#!/usr/bin/python
"""
This example demonstrates the Zernike command.
..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

import LightPipes
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um

pi=3.1415

LP=LightPipes.Init()
wavelength=500*nm
size=2.0*mm
N=200

#Zernike
mz=-3 #azimuthal order
nz=5 #radial order

F=LP.Begin(size,wavelength,N)
F=LP.Zernike(nz,mz,size/2,wavelength/(2*pi),F)
F=LP.CircAperture(size/2,0,0,F)
Phi=LP.Phase(F)
plt.imshow(Phi)
s='Zernike Polynomial: $Z^{'+repr(mz)+'}_{'+repr(nz)+'}$'
plt.title(s);plt.axis('off')
plt.show()
