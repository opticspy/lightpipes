from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import patches

wavelength = 1500*nm
size = 25*mm
N = 500

F=Begin(size,wavelength,N)
F=CircAperture(F, 2*mm, x_shift=-6*mm, y_shift=-2*mm)
F=Fresnel(F, 0.4*m)
Xc,Yc, NXc, NYc =Centroid(F)
sx, sy = D4sigma(F)
I0=Intensity(F)

# Axes ...
fig, main_ax = plt.subplots(figsize=(5, 5))
divider  = make_axes_locatable(main_ax)
top_ax   = divider.append_axes("top",   1.05, pad=0.1, sharex=main_ax)
right_ax = divider.append_axes("right", 1.05, pad=0.1, sharey=main_ax)

# Make some labels invisible
top_ax.xaxis.set_tick_params(labelbottom=False)
right_ax.yaxis.set_tick_params(labelleft=False)

# Labels ...
main_ax.set_xlabel('X [mm]')
main_ax.set_ylabel('Y [mm]')
top_ax.set_ylabel('Intensity [a.u.]')
right_ax.set_xlabel('Intensity [a.u.]')

#plot ...
main_ax.pcolormesh(F.xvalues/mm, F.yvalues/mm, I0)
main_ax.axvline(Xc/mm, color='r')
main_ax.axhline(Yc/mm, color='g')
main_ax.add_patch(patches.Ellipse((Xc/mm, Yc/mm), sx/mm, sy/mm, fill=False, lw=1,color='w', ls='--'))
right_ax.plot(I0[:,NXc],F.yvalues/mm, 'r-', lw=1)
top_ax.plot(F.xvalues/mm,I0[NYc,:], 'g-', lw=1)

plt.show()
