#LightPipes for Python, demonstration of the Steps command
#Calcultion of the intensity distribution in the focus of a lens.
#
#Date: November 4, 2014
#Author: Fred van Goor
#File: Steps.py
#

from LightPipes import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from LightPipes import cm, m, mm, nm, um

wavelength=632.8*nm;
size=4*mm;
N=100;
R=1.5*mm;
dz=10*mm;
Nsteps=100;
f=50*cm;
n=(1.0 + 0.1j)*np.ones((N,N))
Icross=np.zeros((Nsteps,N))
X=range(N)
Z=range(Nsteps)
X, Z=np.meshgrid(X,Z)
F=Begin(size,wavelength,N);
F=CircAperture(R,0,0,F);   
F=Lens(f,0,0,F);
for i in range(0,Nsteps):
    F=Steps(dz,1,n,F);
    I=Intensity(0,F);
    Icross[i][:N]=I[int(N/2)][:N]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Z, Icross, rstride=1, cstride=1,
    cmap='rainbow',
    linewidth=0.0,
    )
plt.axis('off'); plt.title('intensity at focus'); plt.show();
