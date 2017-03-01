import LightPipes
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um


LP=LightPipes.Init()

wavelength=1000*nm
size=10*cm
N=500
w=25*mm
f=200*m
z=100000*m

F=LP.Begin(size,wavelength,N)
F=LP.CircAperture(w,0,0,F)
F=LP.Lens(f,0,0,F)
F=LP.LensFresnel(-f,z,F)
F=LP.IntAttenuator(0.5,F)
I=LP.Intensity(2,F)
#plt.imshow(I)
plt.plot(I[N/2][:N])
plt.show()
