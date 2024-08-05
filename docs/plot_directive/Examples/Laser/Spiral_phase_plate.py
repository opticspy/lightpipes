#! /usr/bin/env python
"""
Spiral_phase_plate.py
    
    Transforms a Gauss beam into a Gauss doughnut beam.
    
    cc Fred van Goor, May 2020.
"""
from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
if LPversion < "2.0.0":
    print(r'You need to upgrade LightPipes to run this script.' + '\n'+r'Type at a terminal prompt: $ pip install --upgrade LightPipes')
    exit(1)

wavelength = 500*nm
size = 10*mm
N=501
w0=1*mm
z=100*cm
order = 1

F=Begin(size,wavelength,N)
F=GaussBeam(F, w0)
Iin=Intensity(0,F)
F=PhaseSpiral(F,m=order)
phase=Phase(F,unwrap=True)
F=Fresnel(z,F)
I=Intensity(0,F)

s = r'LightPipes for Python,' + '\n'+ 'Spiral_phase_plate.py' + '\n\n'\
    r'$\lambda = {:4.2f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$w_0 = {:4.2f}$'.format(w0/mm) + r' $mm$' + '\n'\
    r'$z = $' + '{:4.2f}'.format(z/cm) + r' $cm$' + '\n'\
    r'$order = $' + '{:2d}'.format(order) + '\n'\
    r'${\copyright}$ Fred van Goor, May 2020'

fig, _axs = plt.subplots(nrows = 2, ncols=2,figsize=(8.0,6.5))
fig.suptitle('Gauss beam transformation to doughnut with spiral phase plate')
fig.subplots_adjust(hspace=0.3)
axs = _axs.flatten()

axs[0].imshow(Iin,cmap='jet')
axs[0].grid(color='white', ls='solid')
axs[0].axis('off')
axs[0].set_title(f'intensity at z = 0 cm')

axs[1].imshow(I,cmap='jet')
axs[1].grid(color='white', ls='solid')
axs[1].axis('off')
axs[1].set_title(f'intensity at z = {z/cm} cm')

img1=axs[2].imshow(phase, cmap='jet',vmin=0., vmax=7)
axs[2].axis('off')
axs[2].set_title(r'phase distribution of the spiral phase plate'\
                 + '\n' + f' with order {order}')

axs[3].text(0.3,0.3,s)
axs[3].axis('off')

divider = make_axes_locatable(axs[2])
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar=plt.colorbar(img1, cax=cax, ticks=[0, PI, 2*PI], orientation='vertical')
cbar.ax.set_yticklabels(['0', r'$\pi$', r'$2\pi$'])

plt.show()
