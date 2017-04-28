from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=10.0*mm
N=500
w0=0.2*mm
A=1
z=1*m

F=Begin(size,wavelength,N)
F=GaussLaguerre(1,4,A,w0,F)
F=Forvard(z,F)
I=Intensity(2,F)
plt.imshow(I)
plt.show()
