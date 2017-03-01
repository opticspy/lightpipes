#Diffraction from a circular aperture.

import LightPipes
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um

pi=3.1415

LP=LightPipes.Init()
wavelength=500*nm
size=50*mm
N=1500
w=5*mm
z=5*m
F=LP.Begin(size,wavelength,N)
F=LP.CircAperture(w,0,0,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
plt.imshow(I)
plt.show()
