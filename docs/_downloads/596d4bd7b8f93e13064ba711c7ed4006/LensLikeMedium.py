from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np

size=1*mm
wavelength=1*um
N=100; N2=int(N/2)

#refractive index:
n0=1.5
n1=400.0/m/m
kappa=1.0

#tilt of input beam:
tx=1*mrad
#step size and number of steps in z-direction:
dz=1*mm
NZ=200

X=np.linspace(-size/2,size/2,N)/um
Z=np.linspace(0,NZ*dz,NZ)/cm

#fill the refractive index list:
n=np.zeros([N,N])*(1+1j)
for i in range(0,N-1):
    x=-size/2+i*size/N
    for j in range(1,N):
        y=-size/2+j*size/N
        f=math.sqrt(n0*n0-n0*n1*(x*x+y*y))
        #n[i][j]=f*(1.0-0.9*1j)
        n[i][j]=f-kappa*1j

K=math.pi*2/wavelength
w0=math.sqrt(2/K/math.sqrt(n0*n1))

F=Begin(size,wavelength,N)
F=GaussAperture(w0,0,0,1,F)
F=Tilt(tx,0,F)
Ix=np.zeros([NZ,N])
Iy=np.zeros([NZ,N])
for k in range(0,NZ):
    F=Steps(dz,10,n,F)
    I=Intensity(0,F)
    Iy[k]=list(zip(*I))[N2]
    Ix[k]=I[N2]

fig=plt.figure(figsize=(10,6))
X, Z=np.meshgrid(X,Z)
ax1=fig.add_subplot(121, projection = '3d')
ax1.azim=-45
ax1.elev=70

ax1.plot_surface(X, Z, Ix,
                rstride=1,
                cstride=1,
                antialiased=False,
                cmap='rainbow',
                linewidth=0.0,
                )
ax1.set_title('Radial energy distribution in the x-direction')
ax1.set_xlabel(r'x [$\mu m$]')
ax1.set_ylabel('z [cm]')
ax1.set_zlabel('Intensity [.a.u.]')

ax2 = fig.add_subplot(122, projection = '3d')
ax2.plot_surface(X, Z, Iy,
                rstride=1,
                cstride=1,
                antialiased=False,
                cmap='rainbow',
                linewidth=0.0,
                )
ax2.set_title('Radial energy distribution in the y-direction')
ax2.set_xlabel(r'x [$\mu m$]')
ax2.set_ylabel('z [cm]')
ax2.set_zlabel('Intensity [.a.u.]')
ax2.azim=-45
ax2.elev=70

plt.show()
