"""
Test script for testing the AiryBeam command.
"""

from LightPipes import *
import matplotlib.pyplot as plt

wavelength = 1500*nm
size = 25*mm
N = 500

x0=y0=1*mm
a1=a2=0.100/mm

F=Begin(size,wavelength,N)
F=AiryBeam1D(F)
I=Intensity(F)
plt.imshow(I,cmap='jet')
plt.show()
