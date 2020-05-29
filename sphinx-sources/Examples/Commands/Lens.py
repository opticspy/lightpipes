from LightPipes import *
import matplotlib.pyplot as plt

size=40*mm
wavelength=1*um
N=256
w=20*mm
f=8*m
z=4*m

Field = Begin(size, wavelength, N)
Field = RectAperture(w, w, 0, 0, 0, Field)
Field = Lens(f,0,0,Field)
I0 = Intensity(0,Field)
phi0 = Phase(Field)

Field = Forvard(z, Field)
I1 = Intensity(0,Field)

x=[]
for i in range(256):
    x.append((-size/2+i*size/N)/mm)

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

ax1.plot(x,phi0[int(N/2)]);ax1.set_xlabel('x [mm]');ax1.set_ylabel('Phase [rad]')
ax2.imshow(I0,cmap='gray'); ax2.axis('off')
ax3.imshow(I1,cmap='gray'); ax3.axis('off')
plt.show()
