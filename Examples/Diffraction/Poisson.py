from LightPipes import *
import matplotlib.pyplot as plt

wavelength=5*um
size=25.0*mm
N=500

F=Begin(size,wavelength,N)
F=GaussHermite(0,0,1,size/3,F)
F=CircScreen(3*mm,0*mm,0*mm,F)
F=Fresnel(20*cm,F)
I=Intensity(2,F)

plt.imshow(I); plt.axis('off'); plt.title("Poisson's spot")
plt.show()
