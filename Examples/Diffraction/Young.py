#Interference from two holes.
import matplotlib.pyplot as plt
import LightPipes
from LightPipes import cm, m, mm, nm, um


LP=LightPipes.Init()

wavelength=20*um
size=30.0*mm
N=1000
LP.version()
F=LP.Begin(size,wavelength,N)
F1=LP.CircAperture(0.15*mm,  -0.6*mm,0, F)
F2=LP.CircAperture(0.15*mm,  0.6*mm,0, F)
F=LP.BeamMix(F1,F2)
F=LP.Fresnel(30.0*cm,F)
I=LP.Intensity(2,F)
plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
plt.show()
