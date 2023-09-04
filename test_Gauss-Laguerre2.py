#! /usr/bin/env python
"""
Gauss_laser_mode.py
    
    Calculates the intensity- and phase distributions of Laguerre-Gauss
    laser modes.
    
    cc Fred van Goor, August 2023.
"""
from LightPipes import *
import matplotlib.pyplot as plt
if LPversion < "2.0.0":
    print(r'You need to upgrade LightPipes to run this script.' + '\n'+r'Type at a terminal prompt: $ pip install --upgrade LightPipes')
    exit(1)

wavelength = 500*nm
size = 15*mm
N = 200
w0=3*mm
i=0
ecs=0 #(0: exp, 1: cos, 2: sin)
n_max=6;m_max=6
fig, axs = plt.subplots(nrows=m_max, ncols=n_max,figsize=(11.0,7.0))
s=f'Laguerre-Gauss laser modes, ecs={ecs}'

fig.suptitle(s)
fig.subplots_adjust(hspace=0.4)

F=Begin(size,wavelength,N)
for m in range(int(m_max/2)):
    for n in range(n_max):
        F=GaussLaguerre(F, w0, p=m, l=n, ecs=ecs)
        F=Forvard(F,100*cm)
        I=Intensity(0,F)
        Phi=Phase(F)
        s=f'$LG_{n}$' + f'$_{m}$'
        axs[m+i][n].imshow(I,cmap='jet'); axs[m+i][n].axis('off'); axs[m+i][n].set_title(s)
        axs[m+1+i][n].imshow(Phi,cmap='rainbow'); axs[m+1+i][n].axis('off');
    i+=1

plt.show()

