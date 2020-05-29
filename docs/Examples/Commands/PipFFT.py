from LightPipes import *
import matplotlib.pyplot as plt

size=15*mm
wavelength=1*um
N=150
z=1*m
R=3*mm
Rf=1.5*mm
seed=7
MaxPhase=1.5

F=Begin(size,wavelength,N);
F=CircAperture(R,0,0,F);
F=RandomPhase(seed,MaxPhase,F);
F=Fresnel(z,F);
I0=Intensity(0,F);

F=PipFFT(1,F);
F=CircAperture(Rf,0,0,F);
F=PipFFT(-1,F);
I1=Intensity(1,F);

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.imshow(I0,cmap='rainbow'); ax1.axis('off'); ax1.set_title('Unfiltered intensity')
ax2.imshow(I1,cmap='rainbow'); ax2.axis('off'); ax2.set_title('Filtered intensity')
plt.show()
