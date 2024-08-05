#! /usr/bin/env python
from LightPipes import *
import matplotlib.pyplot as plt

wavelength=632.8*nm #wavelength of HeNe laser
size=15*mm # size of the grid
N=500 # number (NxN) of grid pixels
R=9*mm # laser beam radius
z1=8*cm # length of arm 1
z2=7*cm # length of arm 2
z3=3*cm # distance laser to beamsplitter
z4=5*cm # distance beamsplitter to screen
Rbs=0.5 # reflection beam splitter
tx=0.0*mrad; ty=0.0*mrad # tilt of mirror 1
zernabb = 7 # Zernike aberration (7 = vertical coma)

print(ZernikeName(zernabb))
print(noll_to_zern(zernabb))

#Generate a weak diverging laser beam using a weak negative lens:
F=Begin(size,wavelength,N)
F=GaussBeam(F, R)
#F=Lens(F,-0.5*m)
#Propagate to the beamsplitter:
F=Forvard(z3,F)

#Split the beam and propagate to mirror #2:
F2=IntAttenuator(1-Rbs,F)
F2=Forvard(z2,F2)

#Introduce aberration and propagate back to the beamsplitter:
F2=Tilt(tx,ty,F2)
(mz, nz) = noll_to_zern(zernabb)
F2=Zernike(F2, mz, nz, 6*mm, A=1.03*wavelength)
F2=Forvard(z2,F2)
F2=IntAttenuator(Rbs,F2)

#Split off the second beam and propagate to- and back from the mirror #1:
F10=IntAttenuator(Rbs,F)
F1=Forvard(z1*2,F10)
F1=IntAttenuator(1-Rbs,F1)

#Recombine the two beams and propagate to the screen:
F=BeamMix(F1,F2)
F=Forvard(z4,F)
I=Intensity(1,F)

s1 =    r'LightPipes for Python ' + LPversion + '\n'
s2 =    r'Michelson.py'+ '\n\n'\
        f'size = {size/mm:4.2f} mm' + '\n'\
        f'$\\lambda$ = {wavelength/um:4.2f} $\\mu$m' + '\n'\
        f'N = {N:d}' + '\n'\
        f'R = {R/mm:4.2f} mm beam radius of the laser' + '\n'\
        f'z1 = {z1/mm:4.2f} mm length of arm 1' + '\n'\
        f'z2 = {z2/mm:4.2f} mm length of arm 2' + '\n'\
        f'z3 = {z3/mm:4.2f} mm distance from the laser to the beam splitter' + '\n'\
        f'z4 = {z4/mm:4.2f} mm distance from the beam splitter to the screen' + '\n'\
        f'tx, ty = {tx/mrad:4.2f}, {ty/mrad:4.2f} mrad tilt of mirror 2' + '\n'\
        f'Zernike aberration = {noll_to_zern(zernabb)}, {ZernikeName(zernabb)}' + '\n'\
        r'${\copyright}$ Fred van Goor, June 2020'

fig=plt.figure(figsize=(12,12));
ax1 = fig.add_subplot(311);ax1.axis('off')

ax2 = fig.add_subplot(312);ax2.axis('on')
ax3 = fig.add_subplot(313);ax3.axis('on')
ax1.imshow(I,cmap='rainbow');ax1.set_title('intensity pattern')


ax2.text(0.0,1.0,s1,fontsize=12, fontweight='bold')
ax3.text(0.0,0.5,s2)
#plt.imshow(I,cmap='jet'); plt.axis('off');plt.title('intensity pattern')
plt.show()
