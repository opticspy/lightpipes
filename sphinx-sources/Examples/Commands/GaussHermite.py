from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=5.0*mm
N=100
w0=0.2*mm
A=1
z=1*m

F=Begin(size,wavelength,N)
if LPversion < '2.0.0':
    F=GaussHermite(2, 3, A, w0, F)
else:
    F=GaussHermite(F, w0, 2, 3, A)
F=Fresnel(z,F)
I=Intensity(2,F)
plt.imshow(I)
plt.show()
