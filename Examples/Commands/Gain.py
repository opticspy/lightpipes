from LightPipes import *
import matplotlib.pyplot as plt

wavelength=500*nm
size=5.0*mm
N=100
R=1*mm
z=1*m
f=1*m
dx=0*mm
dy=0*mm

F=Begin(size,wavelength,N)
F=CircAperture(R, 0, 0, F)
F=Lens(f,dx,dy,F)
F=Gain(3,2,10,F)
F=Forvard(z,F)
I=Intensity(2,F)
#plt.imshow(I)
plt.plot(I[int(N/2)][:N])
plt.show()
