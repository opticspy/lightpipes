#! python3

import time
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

print('Executed with python version:')
print(sys.version);print('\n')

start_time = time.time()

from LightPipes import *
print('test LightPipes installation: ');LPtest()
print('using LightPipes version: ',LPversion)

wavelength=1000*nm
size=10*mm
N=256
w=5*mm

z=400*m
sizenew=400*mm
Nnew=64

F = Begin(size,wavelength,N)

F = RectAperture(w, w,0,0, 0, F)
F = Forvard(0.2*m,F)
I0=Intensity(2,F)

F = Interpol(7.5*mm,Nnew,0,0,0,1,F)
F=Forward(z,sizenew,Nnew,F)

I1=Intensity(2,F)

print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time)) 
  
plt.imshow(I0, cmap='gray');plt.axis('off'); plt.title('near field')
plt.show()

X=range(Nnew)
Y=range(Nnew)
X, Y=np.meshgrid(X,Y) 
fig=plt.figure(figsize=(10,6))
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y,I1,
                rstride=1,
                cstride=1,
                cmap='rainbow',
                linewidth=0.0,
                )
ax.axis('off'); ax.set_title('far field')
plt.show()

