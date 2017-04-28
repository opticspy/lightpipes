from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=5.0*mm
N=100
w0=0.2*mm
A=1
z=1*m

F=Begin(size,wavelength,N)
F=GaussHermite(2,3,A,w0,F)
F=Fresnel(z,F)
I=Intensity(2,F)
plt.imshow(I)
plt.show()
