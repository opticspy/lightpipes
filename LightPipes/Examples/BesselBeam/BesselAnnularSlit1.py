from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np

img=mpimg.imread('bessel1.png')
plt.imshow(img); plt.axis('off');plt.title('Spot of Poisson')
plt.show()

wavelength=1000.0*nm
size=10*mm
N=1000

N2=int(N/2)
ZoomFactor=10
NZ=N2/ZoomFactor

a=1.5*mm
z_start=0.001*cm; z_end= 150*cm;
steps=11;
delta_z=(z_end-z_start)/steps
z=z_start
#x=[]
#for i in range(1,N):
#   x.append((-size/2 + i*size/N)/mm)

F=Begin(size,wavelength,N);
F=GaussHermite(0,0,1,size/3.5,F)
F=CircScreen(a,0,0,F)

w0=2.44/math.pi*wavelength/a
for i in range(1,steps):
    w=w0*z

    #y=[]
    F=Fresnel(delta_z,F);
    I=Intensity(0,F);
    #for j in range(1,N):
    #    y.append(I[N2][j])
    plt.subplot(2,5,i)

    s='z= %3.1f m \n' % (z/m) + 'width = %3.2f mm' % (w/mm)
    plt.title(s, fontsize=8)
    #plt.plot(x,y)
    plt.imshow(I,cmap='jet');plt.axis('off')
    plt.axis([N2-NZ, N2+NZ, N2-NZ, N2+NZ])
    #plt.axis([-1, 1, 0,1])
    z=z+delta_z
plt.show()
