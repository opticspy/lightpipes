import LightPipes
import matplotlib.pyplot as plt
from scipy import misc
#import matplotlib.image as mpimg
#import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m
pi=3.1415

LP=LightPipes.Init()
wavelength=500*nm
size=2.0*mm
N=200
nz=8
mz=-2

F=LP.Begin(size,wavelength,N)
F=LP.Zernike(nz,mz,size/2,wavelength/(2*pi),F)
F=LP.CircAperture(size/2,0,0,F)
Phi=LP.Phase(F)
plt.imshow(Phi)
plt.title(print( "{\\fontsize{10}Z^{%d}_{%d}}  \n",mz,nz))
plt.show()

