#! /usr/bin/env python

from LightPipes import *
import matplotlib.pyplot as plt

wavelength = 500*nm
size = 25*mm
N = 200
w0=1*mm
z1=10*m
z2=2*m

F=Begin(size,wavelength,N)
F0=GaussBeam(F, w0,n=2,m=2)
I0=Intensity(F0,0)
print("Beam power source at z=0.0:",Power(F0))

F1n=Forvard(F0,z1)
F1=GaussForvard(F0,z1)

F2n=Forvard(F1n,z2)
F2=GaussForvard(F1,z2)

print("Beam power analytical at z=z1+z2:", Power(F2))
print("Beam power numerical at z=z1+z2:", Power(F2n))

I2=Intensity(F2,0)
I2n=Intensity(F2n)
Phi2=Phase(F2)
Phi2n=Phase(F2n)

fig=plt.figure(figsize=(11,6))

fig.subplots_adjust(hspace=0.4)
ax1 = fig.add_subplot(221);ax1.set_title('Analytical using ABCD propagation')#;ax1.axis('off')
ax2 = fig.add_subplot(222);ax2.set_title('Numerical using Forvard')#;ax2.axis('off')
ax3 = fig.add_subplot(223);ax3.set_title('Analytical using ABCD propagation') #;ax3.axis('off')
ax4 = fig.add_subplot(224);ax4.set_title('Numerical using Forvard')#;ax4.axis('off')

ax1.imshow(I2,cmap='jet')
ax2.imshow(I2n,cmap='jet')
ax3.imshow(Phi2,cmap='jet')
ax4.imshow(Phi2n,cmap='jet')

plt.show()
