#Unstable resonator.
from LightPipes import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time

wavelength = 308*nm
size=14*mm
N=100
w=5.48*mm
f1=-10*m; f2=20*m; L=10*m; Isat=1.0; alpha=1e-4; Lgain=1e4;
tx=0.0; ty=0.00000;
Nrndtrips=20

X=np.zeros(N)
Y=np.zeros(N)
SR=np.zeros(Nrndtrips+1)
F=Begin(size,wavelength,N);
F=RandomIntensity(time.time(),1000,F)
F=RandomPhase(time.time(),10,F);

for k in range(1,Nrndtrips+1):
   F=RectAperture(w,w,0,0,0,F);
   F=Gain(Isat,alpha,2*Lgain,F);
   F=LensFresnel(f1,L,F);
   F=LensFresnel(f2,L,F);
   F=Tilt(tx,ty,F);
   SR[k]=Strehl(F);
   F=Interpol(size,N,0,0,0,1,F);
   print ('Round trip ',k,' Strehl ratio= ',SR[k],'\n');
   F2=RectScreen(w,w,0,0,0,F);
   I=Intensity(2,F2);
   plt.subplot(2,Nrndtrips/2,k)
   plt.title(k)
   plt.axis('off')
   plt.imshow(I)
F2=Convert(F2);
i=range(N)
j=i
X, Y=np.meshgrid(i,j)
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, I, rstride=2, cstride=2, cmap='rainbow', linewidth=0.0)
plt.axis('off'); plt.title('Near-field intensity distribution')

fig = plt.figure()
x=np.arange(1,1,Nrndtrips+1);
plt.plot(SR[1:Nrndtrips+1])
plt.title('Strehl ratio')

#Far-field calculation:
z=1.0*m; f=40.0*m;
ff=z*f/(f-z);
F2=Lens(f,0,0,F2);
F2=LensFresnel(ff,z,F2);
F2=Convert(F2);
I2=Intensity(1,F2);
fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, I2, rstride=1, cstride=1, cmap='rainbow', linewidth=0.0)
plt.axis('off'); plt.title('Far-field intensity distribution')

plt.show()
