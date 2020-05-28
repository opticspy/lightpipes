#! /usr/bin/env python
"""
Gauss_laser_mode.py
    
    Calculates the intensity- and phase distributions of Laguerre-Gauss
    (LG=True) or Hermite-Gauss (LG=False) laser modes.
    
    cc Fred van Goor, May 2020.
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
LG=True

n_max=6;m_max=6
fig, axs = plt.subplots(nrows=m_max, ncols=n_max,figsize=(11.0,7.0))
if LG:
    s=r'Laguerre-Gauss laser modes'
else:
    s=r'Hermite-Gauss laser modes'

fig.suptitle(s)
fig.subplots_adjust(hspace=0.4)

F=Begin(size,wavelength,N)
for m in range(int(m_max/2)):
    for n in range(n_max):
        F=GaussBeam(F, w0, LG=LG,n=n,m=m)
        I=Intensity(0,F)
        Phi=Phase(F)
        if LG:
            s=f'$LG_{n}$' + f'$_{m}$'
        else:
            s=f'$HG_{n}$' + f'$_{m}$'
        axs[m+i][n].imshow(I,cmap='jet'); axs[m+i][n].axis('off'); axs[m+i][n].set_title(s)
        axs[m+1+i][n].imshow(Phi,cmap='rainbow'); axs[m+1+i][n].axis('off');
    i+=1

plt.show()
