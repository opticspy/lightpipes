#Interference from two holes.
import matplotlib.pyplot as plt

from LightPipes import *

wavelength=20*um
size=30.0*mm
N=200
print(LPversion)
#F=Begin(size,wavelength,N)
#F1=CircAperture(0.15*mm,  -0.6*mm,0, F)
#F2=CircAperture(0.15*mm,  0.6*mm,0, F)
#Use the PointSource command for version = 1.2.0
if LPversion < "2.0.0":
    F1=PointSource(size,wavelength,N,-0.6*mm,0)
    F2=PointSource(size,wavelength,N,0.6*mm,0)
else:
    F=Begin(size,wavelength,N)
    F1=PointSource(F,x = -0.6*mm)
    F2=PointSource(F,x =  0.6*mm)
F=BeamMix(F1,F2)
F=Fresnel(30.0*cm,F)
I=Intensity(2,F)
plt.imshow(I,cmap='jet'); plt.axis('off');plt.title('intensity pattern')
plt.show()
