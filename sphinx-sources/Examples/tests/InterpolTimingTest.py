# -*- coding: utf-8 -*-
"""
Benchmarking script to make sure the porting of the code to Python
produces correct results and compare the execution times.

Created on Fri Apr 10 17:37:42 2020

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
wavelength=1*um
size=20.0*mm
w = 10.0*mm
z = 0.5*m

N = 1005

newSize = 30.0*mm
newN = 678
rot_alpha = 32 #[deg]
scale = 0.767
shift_x = -1*mm
shift_y = -3*mm

def system(lib):
    """The optical system run by LightPipes library lib."""
    F = lib.Begin(size, wavelength, N)
    F = lib.RectAperture(w, w, 0, 0, 0, F)
    F = lib.Fresnel(z, F)
    # plotutils.Plot(F)
    with tictoc.printtimer('Interpol'):
        F = lib.Interpol(newSize, newN, shift_x, shift_y, rot_alpha, scale, F)
    return F

#********* Run for new python LP *******

F = system(lp)
I = lp.Intensity(0, F)
phi = lp.Phase(F)
# phi1 = lp.PhaseUnwrap(phi1)

x_mm = F.xvalues/mm

#****** Run for reference cpp OLP *******

Folp = system(olp)
I_o = np.asarray(olp.Intensity(0, Folp))
phi_o = np.asarray(olp.Phase(Folp))

x_mm=[]
for i in range(N):
    x_mm.append((-size/2+i*size/N)/mm)
x_mm = np.asarray(x_mm)

#*********** Plot results *******************

Idiff = I - I_o
phidiff = phi - phi_o

fig=plt.figure(figsize=(15,6))
ax1 = fig.add_subplot(221)
ax1.set_title('I')
p1 = ax1.imshow(I,cmap='rainbow'); ax1.axis('off')
fig.colorbar(p1, ax=ax1)

ax2 = fig.add_subplot(222, sharex = ax1, sharey = ax1)
ax2.set_title('I - I_o')
p2 = ax2.imshow(Idiff, cmap='rainbow'); ax2.axis('off')
fig.colorbar(p2, ax=ax2)

ax3 = fig.add_subplot(223, sharex = ax1, sharey = ax1)
ax3.set_title('Phi')
p3 = ax3.imshow(phi, cmap='rainbow'); ax3.axis('off')
fig.colorbar(p3, ax=ax3)

ax4 = fig.add_subplot(224, sharex = ax1, sharey = ax1)
ax4.set_title('Phi - Phi_olp')
p4 = ax4.imshow(phidiff, cmap='rainbow'); ax4.axis('off')
fig.colorbar(p4, ax=ax4)
plt.show()

