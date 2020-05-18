# -*- coding: utf-8 -*-
"""
Benchmarking script to make sure the porting of the code to Python
produces correct results and compare the execution times.

Created on Sun Apr  5 23:37:26 2020

@author: Leonard.Doyle
"""

import numpy as np
import matplotlib.pyplot as plt

from LightPipes import tictoc
from LightPipes.units import * #m, mm, ...

import LightPipes as lp
"""reference LightPipes (Cpp) renamed and installed with "setup.py develop" as
oldLightPipes"""
import oldlightpipes as olp


#******** Simulation parameters *************
wavelength=1*um
size=20.0*mm

N = 2048

R=5*mm
z=-1*m


#********* Run for new python LP *******

F = lp.Begin(size, wavelength, N)
F = lp.CircAperture(R, 0, 0, F)
F = lp.RectAperture(5*mm, size, 2.5*mm, 0, 23, F)
with tictoc.printtimer('lp.Forvard (N={})'.format(N)):
    F = lp.Forvard(z, F)
Ilp = lp.Intensity(0, F)
# Ilp = lp.Phase(F)
x_mm = F.xvalues/mm

#****** Run for reference cpp OLP *******

F = olp.Begin(size, wavelength, N)
F = olp.CircAperture(R, 0, 0, F)
F = olp.RectAperture(5*mm, size, 2.5*mm, 0, 23, F)
with tictoc.printtimer('olp.Forvard (N={})'.format(N)):
    F = olp.Forvard(z, F)
Iolp = np.asarray(olp.Intensity(0, F))
# Iolp = np.asarray(olp.Phase(F))

x_mm=[]
for i in range(N):
    x_mm.append((-size/2+i*size/N)/mm)
x_mm = np.asarray(x_mm)

#*********** Plot results *******************

Idiff = Ilp - Iolp

fig=plt.figure(figsize=(15,6))
ax1 = fig.add_subplot(131)
ax1.set_title('I of LP')
ax2 = fig.add_subplot(132)
ax2.set_title('difference I_lp - I_olp')
ax3 = fig.add_subplot(133)
ax3.set_title('lineout in middle')
p1 = ax1.imshow(Ilp,cmap='rainbow'); ax1.axis('off')
fig.colorbar(p1, ax=ax1)
p2 = ax2.imshow(Idiff,cmap='rainbow'); ax2.axis('off')
fig.colorbar(p2, ax=ax2)
ax3.plot(x_mm, Ilp[int(N/2),:]); ax3.set_xlabel('x [mm]'); ax3.set_ylabel('Intensity [a.u.]')
ax3.plot(x_mm, Iolp[int(N/2),:]); ax3.legend(['LP','OLP'])
ax3.grid('on')
plt.show()

