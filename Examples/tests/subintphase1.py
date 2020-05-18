from LightPipes import *
import matplotlib.pyplot as plt
import math
import numpy as np

size=30*mm
wavelength=1*um
N=256
R=10*mm

Int=np.empty([N,N])
phase=np.empty([N,N])
for i in range(1,N):
    for j in range(1,N):
        Int[i][j]=math.fabs(math.sin(i/10.0)*math.cos(j/5.0))
        phase[i][j]=math.cos(i/10.0)*math.sin(j/5.0)

F=Begin(size,wavelength,N)
F=SubIntensity(Int,F)
F=SubPhase(phase,F)
F=CircAperture(R,0,0,F)

I=Intensity(0,F)
Phi=Phase(F)
fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.imshow(I,cmap='rainbow'); ax1.axis('off'); ax1.set_title('Intensity')
ax2.imshow(Phi,cmap='hot'); ax2.axis('off'); ax2.set_title('Phase')

plt.show()


