import LightPipes
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um

Pi=3.1415
deg=Pi/180.0

LP=LightPipes.Init()

wavelength=632.8*nm
size=5.0*mm
N=500
phi=179.8*deg
n1=1.5
z=80*cm

F=LP.Begin(size,wavelength,N)
F=LP.Axicon(phi,n1,0,0,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
plt.imshow(I)
plt.show()
