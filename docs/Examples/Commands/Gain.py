from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

wavelength=1000*nm
size=30*mm
N=100
R=1*mm
gain=0.2
Isat=1
L=3*m

F=Begin(size,wavelength,N)
F=GaussHermite(0,0,1,5,F)
Iin=Intensity(0,F)
F=Gain(0.2,1,3,F)
Iout=Intensity(2,F)

X=range(N)
Y=range(N)
X, Y=np.meshgrid(X,Y)
fig = plt.figure()
ax1 = fig.gca(projection='3d')
ax1.plot_surface(X, Y,
        Iin,
        rstride=1,
        cstride=1,
        cmap='rainbow',
        linewidth=0.0,
        )
ax1.axis('off')
plt.show()
