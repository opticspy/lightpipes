from LightPipes import *
import matplotlib.pyplot as plt
import numpy as nb
wavelength=500*nm
size=5*mm
N=500
r=nb.arange(-size/2,size/2,size/N)
F=Begin(size,wavelength,N)
F=GaussHermite(0,0,1,size/3,F)
F=CircScreen(1*mm,0*mm,0*mm,F)
F=Fresnel(40*cm,F)
I=Intensity(1,F)
plt.plot(r,I[250])
#plt.imshow(I,cmap='jet'); plt.axis('off'); plt.title("Poisson's spot")
plt.show()
