#! /usr/bin/env python
from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=8.0*mm
N=1000
R=300*mm
d1=340*mm
d2=340*mm
f=300*mm
f1=3000*mm
z=190*mm
f2=1/(1/f-1/f1)

F=Begin(size,wavelength,N)
F=CircAperture(R, 0, 0, F)
#I=Intensity(2,F)
F1=Forvard(d1,F)
F2=Forvard(d2-z,F)
F2=Lens(f1,0,0,F2)
F2=LensForvard(f2,z,F2)
F2=Convert(F2)
size_new=getGridSize()
F1=Interpol(size_new,N,0,0,0,1,F1)
F=BeamMix(F1,F2)
I=Intensity(2,F)

plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
plt.show()
