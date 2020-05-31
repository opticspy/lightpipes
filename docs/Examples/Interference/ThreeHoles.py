from LightPipes import *
import matplotlib.pyplot as plt

wavelength=550*nm
size=5*mm
N=128
R=0.12*mm
x=0.5*mm
y=0.25*mm
z=75*cm

F=Begin(size,wavelength,N)
F1=CircAperture(R,-x, -y, F)
F2=CircAperture(R, x, -y, F)
F3=CircAperture(R, 0, y, F)  
F=BeamMix(BeamMix(F1,F2),F3)
I0=Intensity(2,F)
F=Fresnel(z,F)
I1=Intensity(2,F)

plt.imshow(I0, cmap='gray'); plt.axis('off');plt.title('Plane of the screen')
plt.show()

plt.imshow(I1, cmap='rainbow'); plt.axis('off');plt.title('Intensity distribution a distance z from the screen')
plt.show()
