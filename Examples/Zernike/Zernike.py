#!/usr/bin/python
"""
This example demonstrates the Zernike command.
..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

from LightPipes import *
import matplotlib.pyplot as plt
import math
import numpy as np

wavelength=500*nm
size=2.0*mm
N=200
A=wavelength/(2*math.pi)

plt.figure(figsize=(15,8)) 
for Noll in range (1,22):
    (nz,mz)=noll_to_zern(Noll)
    S=ZernikeName(Noll)
    F=Begin(size,wavelength,N)
    F=Zernike(nz,mz,size/2,A,F)
    F=CircAperture(size/2,0,0,F)
    Phi=Phase(F)
    plt.subplot(3,7,Noll)
    plt.imshow(Phi)
    s=repr(Noll) + '  ' + ' $Z^{'+repr(mz)+'}_{'+repr(nz)+'}$' + '\n' + S
    plt.title(s, fontsize=9);plt.axis('off')
plt.show()

