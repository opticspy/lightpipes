#! /usr/bin/env python
"""
Script to test the Propagate command.
"""
from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import patches

wavelength = 500*nm
size = 25*mm
N = 500
N2=int(N/2)
w0=2*mm

F=Begin(size,wavelength,N)
F=GaussBeam(F, w0,n=2,m=2)
print(F._q)

#F=CircAperture(F,5*w0) # Comment to use pure Gauss propagation


Xc,Yc,NXc,NYc=Centroid(F)
wx,wy=D4sigma(F)

fcx=wx*size/N/wavelength
fcy=wy*size/N/wavelength

fc = (fcx, fcy)[int(fcx<fcy)]
print(fc,fcx,fcy)
f=1.1*fc
F=Propagate(F,f)
F=Lens(F,f)
F=Propagate(F,2*f,UseForvard=True)

I1=Intensity(F)
Phi1=Phase(F)

s1='fc = {:2.2f} cm'.format(fc/cm)
s2='f = {:2.2f} cm'.format(f/cm)
wx,wy=D4sigma(F)

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
main_ax.pcolormesh(F.xvalues/mm, F.yvalues/mm, I1)
main_ax.axvline(Xc/mm, color='r', ls='--')
main_ax.axhline(Yc/mm, color='g', ls='--')
main_ax.add_patch(patches.Ellipse((Xc/mm, Yc/mm), wx/mm, wy/mm, fill=False, lw=1, color='w', ls='--'))
right_ax.plot(I1[:,NXc],F.yvalues/mm, 'r-', lw=1)
top_ax.plot(F.xvalues/mm,I1[NYc,:], 'g-', lw=1)

plt.show()
