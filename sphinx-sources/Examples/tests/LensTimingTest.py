# -*- coding: utf-8 -*-
"""
Benchmarking script to make sure the porting of the code to Python
produces correct results and compare the execution times.

Created on Mon Apr  6 22:38:34 2020

@author: Lenny
"""


import numpy as np
import matplotlib.pyplot as plt

from LightPipes import tictoc
from LightPipes.units import * #m, mm, ...

import LightPipes as lp
"""reference LightPipes (Cpp) renamed and installed with "setup.py develop" as
oldLightPipes"""
import oldLightPipes as olp


#******** Simulation parameters *************
wavelength=1*um
size=20.0*mm

N = 1000

f=10*cm
f1=10*m
f2=f1*f/(f1-f)
frac=f/f1
newsize=frac*size
w=5*mm

#********* Run for new python LP *******

F = lp.Begin(size, wavelength, N)
F = lp.RectAperture(w,w,0,0,0,F)

#1) Using Lens and Fresnel:
with tictoc.printtimer('Lens and Fresnel (N={})'.format(N)):
    F1 = lp.Lens(f,0,0,F)
    F1 = lp.Fresnel(f,F1)
I1 = lp.Intensity(0, F1)
phi1 = lp.Phase(F1)
# phi1 = lp.PhaseUnwrap(phi1)

#2) Using Lens + LensFresnel and Convert:
with tictoc.printtimer('With LensF+Convert (N={})'.format(N)):
    F2 = lp.Lens(f1,0,0,F)
    F2 = lp.LensFresnel(f2,f,F2)
    F2 = lp.Convert(F2)
I2 = lp.Intensity(0,F2)
phi2 = lp.Phase(F2)
# phi2 = lp.PhaseUnwrap(phi2)

x_mm = F.xvalues/mm

#****** Run for reference cpp OLP *******

F = olp.Begin(size, wavelength, N)
F = olp.RectAperture(w,w,0,0,0,F)

#1) Using Lens and Fresnel:
with tictoc.printtimer('Lens and Fresnel OLP (N={})'.format(N)):
    F1 = olp.Lens(f,0,0,F)
    F1 = olp.Fresnel(f,F1)
I1olp = olp.Intensity(0, F1)
phi1 = olp.Phase(F1)
phi1 = olp.PhaseUnwrap(phi1)

#2) Using Lens + LensFresnel and Convert:
with tictoc.printtimer('With LensF+Convert (N={})'.format(N)):
    F2 = olp.Lens(f1,0,0,F)
    F2 = olp.LensFresnel(f2,f,F2)
    F2 = olp.Convert(F2)
I2olp = olp.Intensity(0,F2)
phi2olp = olp.Phase(F2)
phi2olp = olp.PhaseUnwrap(phi2olp)

I1olp = np.asarray(I1olp)
I2olp = np.asarray(I2olp)

x_mm=[]
for i in range(N):
    x_mm.append((-size/2+i*size/N)/mm)
x_mm = np.asarray(x_mm)

#*********** Plot results *******************

I1diff = I1 - I1olp
I2diff = I2 - I2olp

fig=plt.figure(figsize=(15,6))
ax1 = fig.add_subplot(131)
ax1.set_title('I1 - I1olp')
ax2 = fig.add_subplot(132)
ax2.set_title('I2 - I2olp')
ax3 = fig.add_subplot(133)
ax3.set_title('lineout in middle')
p1 = ax1.imshow(I1diff,cmap='rainbow'); ax1.axis('off')
fig.colorbar(p1, ax=ax1)
p2 = ax2.imshow(I2diff,cmap='rainbow'); ax2.axis('off')
fig.colorbar(p2, ax=ax2)
ax3.plot(x_mm, I1[int(N/2),:]); ax3.set_xlabel('x [mm]'); ax3.set_ylabel('Intensity [a.u.]')
ax3.plot(x_mm, I1olp[int(N/2),:]); ax3.legend(['LP','OLP'])
ax3.grid('on')
plt.show()

