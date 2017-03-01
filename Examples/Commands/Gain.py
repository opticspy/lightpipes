import LightPipes as lp
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um


LP=lp.Init()

wavelength=500*nm
size=5.0*mm
N=100
R=1*mm
z=1*m
f=1*m
dx=0*mm
dy=0*mm

F=LP.Begin(size,wavelength,N)
F=LP.CircAperture(R, 0, 0, F)
F=LP.Lens(f,dx,dy,F)
F=LP.Gain(3,2,10,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
#plt.imshow(I)
plt.plot(I[N/2][:N])
plt.show()
