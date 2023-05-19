#! python3

import matplotlib.pyplot as plt
from LightPipes import *

wavelength=550*nm
size=5*mm
N=128
w=0.1*mm
h=2.5*mm
phi=15*rad
x=0.5*mm
z=75*cm

F = Begin(size,wavelength,N)
F1 = RectAperture(w, h,-x,0, 0, F)
F2 = RectAperture(w, h,x,0, phi, F) 
F=BeamMix(F1,F2)
I0=Intensity(2,F)
F=Fresnel(z,F)
I1=Intensity(1,F)

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.imshow(I0,cmap='gray',aspect='equal');ax1.axis('off'); ax1.set_title('Plane of the screen')
ax2.imshow(I1,cmap='gray',aspect='equal');ax2.axis('off'); ax2.set_title('Intensity distribution at a distance z from the screen')

plt.show()

