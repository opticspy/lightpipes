from LightPipes import *
import matplotlib.pyplot as plt

wavelength=1*um
size=25.0*mm
N=300

F=Begin(size,wavelength,N)
F=CircAperture(5*mm, 0, 0, F)
F=Forvard(100*cm,F)
I=Intensity(2,F)

plt.imshow(I)
plt.show()
