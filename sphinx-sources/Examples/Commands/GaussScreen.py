from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=5.0*mm
N=100
w=0.2*mm
T=2
z=1*m
dx=1.0*mm
dy=1.0*mm

F=Begin(size,wavelength,N)
F=GaussScreen(w,dx,dy,T,F)
F=Forvard(z,F)
I=Intensity(2,F)
plt.imshow(I)
#plt.plot(I[N/2][:N])
plt.show()
