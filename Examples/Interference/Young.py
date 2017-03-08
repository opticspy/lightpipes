from LightPipes import *
import matplotlib.pyplot as plt

wavelength=5*um
size=20.0*mm
N=500

F=Begin(size,wavelength,N)
F1=CircAperture(0.15*mm,-0.6*mm, 0, F)
F2=CircAperture(0.15*mm, 0.6*mm, 0, F)    
F=BeamMix(F1,F2)
F=Fresnel(50*cm,F)
I=Intensity(2,F)
plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
plt.show()
