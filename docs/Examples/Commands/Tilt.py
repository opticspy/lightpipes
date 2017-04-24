from LightPipes import *
import matplotlib.pyplot as plt

size=40*mm
wavelength=1*um
N=256
w=20*mm
z=8*m
tx=0.1*mrad
ty=0.1*mrad

Field = Begin(size, wavelength, N)
Field = RectAperture(w, w, 0, 0, 0, Field)
Field = Tilt(tx,ty,Field)
I0 = Intensity(0,Field)


Field = Forvard(z, Field)
I1 = Intensity(0,Field)
phi1 = Phase(Field)

x=[]
for i in range(256):
    x.append((-size/2+i*size/N)/mm)

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot(x,I1[int(N/2)]);ax1.set_xlabel('x [mm]');ax1.set_ylabel('Intensity [a.u.]')
ax2.plot(x,phi1[int(N/2)]);ax2.set_xlabel('x [mm]');ax2.set_ylabel('Phase [rad]')

plt.show()
