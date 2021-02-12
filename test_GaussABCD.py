#! /usr/bin/env python

from LightPipes import *
import matplotlib.pyplot as plt


wavelength = 500*nm
size = 7*mm
N = 1000
w0=1*mm
f=1*m
z1=1*m
z2=2*m
z3=1*m

M_lens=[
    [1.0,       0.0],
    [-1.0/f,    1.0]
  ]
  
M_propagate=[
    [1.0,       z1 ],
    [0.0,       1.0]
  ]

F=Begin(size,wavelength,N)
F0=GaussBeam(F, w0,n=0,m=0)
I0=Intensity(F0,0)
print("Beam power source at z=0.0:",Power(F0))

F1n=Forvard(F0,z1)
#F1=GaussForvard(F0,z1)
F1=GaussABCD(F0,M_propagate)

F2n=Lens(F1n,f)
F2=GaussLens(F1,f)

F3n=Forvard(F2n,z2)
F3=GaussForvard(F2,z2)

F4n=Lens(F3n,f)
#F4=GaussLens(F3,f)
F4=GaussABCD(F3,M_lens)

F5n=Forvard(F4n,z3)
F5=GaussForvard(F4,z3)

print("Output beam power analytical:", Power(F5))
print("Output beam power numerical:", Power(F5n))

I5=Intensity(F5)
I5n=Intensity(F5n)
Phi5=Phase(F5)
Phi5n=Phase(F5n)

fig=plt.figure(figsize=(11,6))

fig.subplots_adjust(hspace=0.4)
ax1 = fig.add_subplot(221);ax1.set_title('Analytical using ABCD propagation')#;ax1.axis('off')
ax2 = fig.add_subplot(222);ax2.set_title('Numerical using Forvard')#;ax2.axis('off')
ax3 = fig.add_subplot(223);ax3.set_title('Analytical using ABCD propagation') #;ax3.axis('off')
ax4 = fig.add_subplot(224);ax4.set_title('Numerical using Forvard')#;ax4.axis('off')

ax1.imshow(I5,cmap='jet')
ax2.imshow(I5n,cmap='jet')
ax3.imshow(Phi5,cmap='jet')
ax4.imshow(Phi5n,cmap='jet')

plt.show()
