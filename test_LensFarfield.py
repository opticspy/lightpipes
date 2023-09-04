#!/usr/bin/python
"""
This example demonstrates the Zernike command.
..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

from LightPipes import *
import matplotlib.pyplot as plt
wavelength=500*nm
size=20.0*mm
N=1000
f=500*cm

F = Begin(size, wavelength, N)
F = CircAperture(F, 5*mm)
F2=F
F=LensFarfield(F,f)
I=Intensity(F)
plt.imshow(I, cmap='rainbow'); plt.axis('off');plt.title('intensity pattern')
plt.show()

F2=Lens(F2,f)
F2=Fresnel(F2,f)
I2=Intensity(F2)
plt.imshow(I2, cmap='rainbow'); plt.axis('off');plt.title('intensity pattern')
plt.show()

