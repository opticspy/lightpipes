#!/usr/bin/python
"""
This example demonstrates a radial shear interferometer.
Only a 'bare-bone' model, so no propagation and diffraction, is considered.
..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

from LightPipes import *
import matplotlib.pyplot as plt
import math

pi=3.1415


wavelength=500*nm
size=40.0*mm
N=200
R=10*mm
nz=10
mz=4
Rz=10*mm

Az=wavelength/(2*pi)

Rbs=0.5
M=1.5

F=Begin(size,wavelength,N)

F=Zernike(nz,mz,Rz,Az,F)
F=CircAperture(R,0,0,F)
phi=Phase(F)
fig=plt.figure(figsize=(8,8))
fig.suptitle('radial shear interferometer',fontsize=20, color='red')
plt.subplot(2,1,1)
plt.imshow(phi);plt.axis('off');plt.axis('equal')
plt.title('phase distribution input beam')
F1=IntAttenuator(Rbs,F)
F2=IntAttenuator(1-Rbs,F)

F1=Interpol(size,N,0,0,0,M,F1)
F=BeamMix(F1,F2)
I=Intensity(2,F)
plt.subplot(2,1,2)
plt.imshow(I)
plt.axis('off');plt.axis('equal')
plt.title('intensity distribution output beam')

plt.show()

