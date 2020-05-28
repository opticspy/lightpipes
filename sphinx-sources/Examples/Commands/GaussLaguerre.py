from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=10.0*mm
N=500
w0=0.2*mm
A=1
z=1*m

F=Begin(size,wavelength,N)
if LPversion < '2.0.0':
    F=GaussLaguerre(1, 4, A, w0, F)
else:
    F=GaussLaguerre(F, w0, 1, 4, A)
F=Forvard(z,F)
I=Intensity(2,F)
plt.imshow(I)
plt.show()
