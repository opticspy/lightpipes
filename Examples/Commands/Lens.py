from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

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


II=np.zeros((100,100))
F=MultPhase(II,F)   
F=Forvard(z,F)


I=Intensity(2,F)
#plt.imshow(I)
plt.plot(I[int(N/2)][:N])
plt.show()
