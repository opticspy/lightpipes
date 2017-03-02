from LightPipes import *
import matplotlib.pyplot as plt

wavelength=1000*nm
size=10*cm
N=500
w=25*mm
f=200*m
z=100000*m

F=Begin(size,wavelength,N)
F=CircAperture(w,0,0,F)
F=Lens(f,0,0,F)
F=LensFresnel(-f,z,F)
F=IntAttenuator(0.5,F)
I=Intensity(2,F)
#plt.imshow(I)
plt.plot(I[int(N/2)][:N])
plt.show()
