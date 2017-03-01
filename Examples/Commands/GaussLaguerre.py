import LightPipes as lp
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um


LP=lp.Init()

wavelength=500*nm
size=10.0*mm
N=500
w0=0.2*mm
A=1
z=1*m

F=LP.Begin(size,wavelength,N)
F=LP.GaussLaguerre(1,4,A,w0,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
plt.imshow(I)
plt.show()
