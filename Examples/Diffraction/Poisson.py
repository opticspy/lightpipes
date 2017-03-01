#spot of Poisson
import LightPipes
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um

pi=3.1415

LP=LightPipes.Init()
wavelength=500*nm
size=10*mm
N=1500
w=1*mm
z=1*m
F=LP.Begin(size,wavelength,N)
F=LP.CircScreen(w,0,0,F)
F=LP.Forvard(z,F)
I=LP.Intensity(2,F)
plt.imshow(I)
plt.title('the spot of Poisson')
plt.axis('off')
plt.show()
