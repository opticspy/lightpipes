from LightPipes import *
import matplotlib.pyplot as plt
import math
import numpy as np
size=15*mm
wavelength=1*um
N=500
R=4.5*mm
z=1.89*m

A = wavelength/(2*math.pi*math.sqrt(2*(2+1)))
Field = Begin(size, wavelength, N)
Field = CircAperture(R, 0, 0, Field)
I0 = Intensity(1,Field)
Field = Zernike(2,2,R,-20*A,Field)
Field = Zernike(2,0,R,10*A,Field)
Field = Fresnel(z, Field)
#Field = Interpol(size,N,0,0,-45,1,Field)
I1 = Intensity(1,Field)

x=np.linspace(-size/2.0,size/2.0,N)/mm

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(224)

ax1.imshow(I0,cmap='gray'); ax1.axis('off')
ax2.imshow(I1,cmap='gray'); ax2.axis('off')
ax3.plot(x,I1[int(N/2)],x,zip(*I1)[int(N/2)])
ax3.set_xlabel('x [mm]');ax3.set_ylabel('Intensity [a.u.]')
plt.show()
