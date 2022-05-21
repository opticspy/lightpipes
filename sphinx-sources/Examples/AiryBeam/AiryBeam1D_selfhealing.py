"""
Example of a self-healing 1D Airy beam.
A disk is inserted in the beam. Behind the disk the beam recovers.
"""

from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

wavelength = 2.3*um
size = 30*mm
N = 500
N2=N//2
x0=0.3*mm
a=0.1/mm
dz=1.25*cm
NZ=200
w=0.5*mm
x_shift = -1*mm
z_obst =10 *cm
k_obst = z_obst//dz

F0=Begin(size,wavelength,N)
F0=AiryBeam1D(F0,x0=x0, a=a)
Ix=np.zeros(N)
for k in range(0,NZ):
    if k==k_obst:
        F0=CircScreen(F0,w,x_shift=x_shift)
    F=Forvard(F0,dz*k)
    I=Intensity(F)
    Ix=np.vstack([Ix,I[N2]])

plt.figure(figsize = (12,5))
plt.imshow(Ix,
           extent=[-size/2/mm, size/2/mm, 0, NZ*dz/cm],
           aspect=0.08,
           origin='lower',
           cmap='jet',
           )
plt.title('self-healing 1D Airy beam')
plt.xlabel('x [mm]')
plt.ylabel('z [cm]')
s = r'LightPipes for Python' + '\n'+ '1D Airy beam' + '\n\n'\
    r'$\lambda = {:4.2f}$'.format(wavelength/um) + r' ${\mu}m$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$x_0 = {:4.2f}$'.format(x0/mm) + r' $mm$' + '\n'\
    r'$a = $' + '{:4.2f}'.format(a*mm) + r' $/mm$' + '\n'\
    r'{:4.1f}'.format(2*w/mm) + ' $mm$ ' + 'diameter disk as obstacle at '+ '\n'\
    r'x = {:4.1f}'.format(x_shift/mm) + ' $mm$ and at z = {:4.1f}'.format(z_obst/cm) + ' $cm$' + '\n'\
    r'${\copyright}$ Fred van Goor, May 2022'
plt.text(16, 50, s, bbox={'facecolor': 'white', 'pad': 5})
plt.show()
