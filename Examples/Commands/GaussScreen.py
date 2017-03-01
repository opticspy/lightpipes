import LightPipes as lp
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um


LP=lp.Init()

wavelength=500*nm
size=5.0*mm
N=100
w=0.2*mm
T=2
z=1*m
dx=1.0*mm
dy=1.0*mm

F=LP.Begin(size,wavelength,N)
F=LP.GaussScreen(w,dx,dy,T,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
plt.imshow(I)
#plt.plot(I[N/2][:N])
plt.show()
