from LightPipes import *
import matplotlib.pyplot as plt

wavelength=1*um
size=25.0*mm
N=1000

F=Begin(size,wavelength,N)
F=CircAperture(5*mm, 0, 0, F)
F=Forvard(100*cm,F)
I=Intensity(0,F)

plt.imshow(I,cmap='jet')
plt.show()
