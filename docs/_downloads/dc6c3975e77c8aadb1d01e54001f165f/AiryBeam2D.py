"""
Test script for testing the AiryBeam2D command.
"""

from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

wavelength = 2.3*um
size = 30*mm
N = 500
x0=y0=1*mm
a1=a2=0.1/mm
z=900*cm

F0=Begin(size,wavelength,N)
F0=AiryBeam2D(F0,x0=x0, y0=y0, a1=a1, a2=a2)
F=Fresnel(F0,z)
I=Intensity(F)
plt.figure(figsize = (9,5))
plt.imshow(I,
           extent=[-size/2/mm, size/2/mm, -size/2/mm, size/2/mm],
           origin='lower',
           cmap='jet',
           )
plt.title('2D Airy beam')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
s = r'LightPipes for Python' + '\n'+ '2D Airy beam' + '\n\n'\
    r'$\lambda = {:4.2f}$'.format(wavelength/um) + r' ${\mu}m$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$x_0 = y_0 = {:4.2f}$'.format(x0/mm) + r' $mm$' + '\n'\
    r'$a1 = a2 =  $' + '{:4.2f}'.format(a1*mm) + r' $/mm$' + '\n'\
    r'$z = $' + '{:4.2f}'.format(z/cm) + r' $cm$' + '\n'\
    r'${\copyright}$ Fred van Goor, May 2022'
plt.text(16, -10, s, bbox={'facecolor': 'white', 'pad': 5})
plt.show()
