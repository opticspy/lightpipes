# -*- coding: utf-8 -*-
"""
Benchmarking script to make sure the porting of the code to Python
produces correct results and compare the execution times.

Based on example: Commands/Steps.py

Created on Sun Apr 19 13:18:33 2020

@author: Leonard.Doyle
"""


import numpy as np
import matplotlib.pyplot as plt

from LightPipes import tictoc
from LightPipes.units import * #m, mm, ...
from LightPipes import plotutils

import LightPipes as lp
"""reference LightPipes (Cpp) renamed and installed with "setup.py develop" as
oldLightPipes"""
import oldLightPipes as olp


#******** Simulation parameters *************
wavelength=632.8*nm
size=4*mm
N=200
R=1*mm
dz=10*mm
Nsteps=100
f=50*cm
n=(1.0 + 0.1j)*np.ones((N,N))
# n[int(N/4):int(N*3/4),int(N/4):int(N*5/8)] = 1.5 #create asymmtery to see
# if code accidentally flips anything etc.


X=range(N)
Z=range(Nsteps)
X, Z=np.meshgrid(X,Z)



def system(lib):
    """The optical system run by LightPipes library lib."""
    Icross=np.zeros((Nsteps,N))
    F = lib.Begin(size, wavelength, N)
    F = lib.CircAperture(R,0,0,F)
    F = lib.Lens(f,0,0,F)
    t_tot = 0.0
    for i in range(Nsteps):
        tictoc.tic()
        # with tictoc.printtimer('1 Steps'):
        F = lib.Steps(dz,1,n,F)
        t_tot += tictoc.toc()
        I = lib.Intensity(0,F)
        Icross[i,:] = I[int(N/2)][:] #center lineout
    print(t_tot)
    return F, Icross

#********* Run for new python LP *******

F, Icross_lp = system(lp)
I = lp.Intensity(0, F)
phi = lp.Phase(F)

#****** Run for reference cpp OLP *******

F_o, Icross_olp = system(olp)
I_o = np.asarray(olp.Intensity(0, F_o))
phi_o = np.asarray(olp.Phase(F_o))

#*********** Plot results *******************

fig, [ax1, ax2] = plt.subplots(1, 2, sharex=True, sharey=True)
ax1.imshow(Icross_lp)
im2 = ax2.imshow(Icross_lp- Icross_olp)
plt.colorbar(im2, ax=ax2)

Idiff = I - I_o
phidiff = phi - phi_o

fig=plt.figure(figsize=(15,6))
ax1 = fig.add_subplot(231)
ax1.set_title('I')
p1 = ax1.imshow(I,cmap='rainbow'); ax1.axis('off')
fig.colorbar(p1, ax=ax1)

ax2 = fig.add_subplot(232, sharex = ax1, sharey = ax1)
ax2.set_title('I_o')
p2 = ax2.imshow(I_o, cmap='rainbow'); ax2.axis('off')
fig.colorbar(p2, ax=ax2)

ax3 = fig.add_subplot(233, sharex = ax1, sharey = ax1)
ax3.set_title('I - I_o')
p3 = ax3.imshow(Idiff, cmap='rainbow'); ax2.axis('off')
fig.colorbar(p3, ax=ax3)

ax4 = fig.add_subplot(234, sharex = ax1, sharey = ax1)
ax4.set_title('Phi')
p4 = ax4.imshow(phi, cmap='rainbow'); ax3.axis('off')
fig.colorbar(p4, ax=ax4)

ax5 = fig.add_subplot(235, sharex = ax1, sharey = ax1)
ax5.set_title('Phi_o')
p5 = ax5.imshow(phi_o, cmap='rainbow'); ax3.axis('off')
fig.colorbar(p5, ax=ax5)

ax6 = fig.add_subplot(236, sharex = ax1, sharey = ax1)
ax6.set_title('Phi - Phi_olp')
p6 = ax6.imshow(phidiff, cmap='rainbow'); ax4.axis('off')
fig.colorbar(p6, ax=ax6)
plt.show()

