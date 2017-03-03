from LightPipes import *
import matplotlib.pyplot as plt

wavelength=1*um
size=25.0*mm
N=300

F=Begin(size,wavelength,N)
F=CircAperture(5*mm, 0, 0, F)
#F=CircScreen(5*mm, 0, 0, F)
#F=RectScreen(5*mm, 5*mm,0,0*mm,0,F)
F=Forvard(100*cm,F)
#F=Forvard(10*cm,F)
#F=Interpol(size*2,N/2,0,0,0,1,F)
I=Intensity(2,F)
#plt.plot(I[N/2][:N])
plt.imshow(I)
plt.show()
