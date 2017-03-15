#Diffraction from a circular aperture.

from LightPipes import *
import matplotlib.pyplot as plt

pi=3.1415

wavelength=500*nm
size=50*mm
N=1500
w=5*mm
z=5*m

F=Begin(size,wavelength,N)
F=CircAperture(w,0,0,F)
F=Forvard(z,F)
I=Intensity(2,F)

plt.imshow(I)
plt.show()
