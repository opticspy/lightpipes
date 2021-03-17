#! /usr/bin/env python
"""
Test script: compare analytical and numerical propagation commands.
"""
from LightPipes import *
import matplotlib.pyplot as plt

wavelength = 500*nm
size = 7*mm
N = 100
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
F0=GaussBeam(F, w0,n=3,m=2)
I0=Intensity(F0,0)

F1n=Forvard(F0,z1)

#GForvard and ABCD should be identical
#F1=GForvard(F0,z1)
F1=ABCD(F0,M_propagate)

F2n=Lens(F1n,f)
F2=GLens(F1,f)

F3n=Forvard(F2n,z2)
F3=GForvard(F2,z2)

F4n=Lens(F3n,f)

#GLens and ABCD should be identical
F4=GLens(F3,f)
#F4=ABCD(F3,M_lens)

F5n=Forvard(F4n,z3)
F5=GForvard(F4,z3)

I5=Intensity(F5)
I5n=Intensity(F5n)
Phi5=Phase(F5)
Phi5n=Phase(F5n)

s1 = "LightPipes for Python"
s2 =r'test_GaussABCD.py' + '\n\n'\
    r'4f relay imaging set up to compare analytical with' + '\n'\
    r' numerical results' + '\n\n'\
    r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$w_0 = {:4.4f}$'.format(w0/mm) + r' $mm$' + '\n'\
    r'$f =  {:4.3f}$'.format(f/m) + r' $m$' + '\n'\
    r'$z1 = {:4.2f}$'.format(z1/m) + r' $m$' + '\n'\
    r'$z2 = {:4.2f}$'.format(z2/m) + r' $m$' + '\n'\
    r'$z3 = {:4.2f}$'.format(z3/m) + r' $m$' + '\n'\
    r'beam power at source = ${:4.2f}$'.format(Power(F0)) + '\n'\
    r'output beam power analytical = ${:4.2f}$'.format(Power(F5)) + '\n'\
    r'output beam power numerical = ${:4.2f}$'.format(Power(F5n)) + '\n'\
    r'${\copyright}$ Fred van Goor, March 2021'

fig=plt.figure(figsize=(11,6))

fig.subplots_adjust(hspace=0.4)
ax1 = fig.add_subplot(231);ax1.set_title('Analytical using ABCD propagation'+'\n' +'(intensity)')#;ax1.axis('off')
ax2 = fig.add_subplot(232);ax2.set_title('Numerical using Forvard'+'\n' +'(intensity)')#;ax2.axis('off')

ax3 = fig.add_subplot(233);ax3.axis('off')
ax4 = fig.add_subplot(234);ax4.set_title('Analytical using ABCD propagation'+'\n' +'(phase)') #;ax5.axis('off')
ax5 = fig.add_subplot(235);ax5.set_title('Numerical using Forvard'+'\n' +'(phase)')#;ax4.axis('off')

ax1.imshow(I5,cmap='jet')
ax2.imshow(I5n,cmap='jet')
ax3.text(0,1.0,s1, fontsize=15,va='top')
ax3.text(0,0.8,s2, va = 'top')
ax4.imshow(Phi5,cmap='jet')
ax5.imshow(Phi5n,cmap='jet')

plt.show()
