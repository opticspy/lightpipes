#! /usr/bin/python
"""
    Phase recovery from two meausured intensity distributions using Gerchberg Saxton.

..  :copyright: (c) 2017 by Fred van Goor.
    :license: MIT, see License for more details.
"""

import matplotlib.pyplot as plt
import numpy as np
import LightPipes
from LightPipes import cm, m, mm, nm, um

#Parameters used for the experiment:
size=11*mm; #The CCD-sensor has an area of size x size (NB LightPipes needs square grids!)
wavelength=632.8*nm; #wavelength of the HeNe laser used
z=2*m; #propagation distance from near to far field
N_iterations=300 #number of iterations

#Read near and far field (at a distance of z=2 m) from disk:
f=open('Inear.prn','r')
lines=f.readlines()
f.close()
data = [line.split() for line in lines]
Inear = np.asfarray(data)

f=open('Ifar.prn','r')
lines=f.readlines()
f.close()
data = [line.split() for line in lines]
Ifar = np.asfarray(data)

N=len(Inear)
N_new=256;size_new=40*mm;

plt.subplot(3,2,1);plt.imshow(Inear);
plt.title('Measured Intensity near field'); plt.axis ('off');
plt.subplot(3,2,2);plt.imshow(Ifar);
plt.title('Measured Intensity far field');plt.axis ('off');

LP=LightPipes.Init()
#Define a field with uniform amplitude- (=1) and phase (=0) distribution
#(= plane wave)
F=LP.Begin(size,wavelength,N);

#The iteration:
for k in range(1,100):
    F=LP.SubIntensity(Ifar,F) #Substitute the measured far field into the field
    F=LP.Interpol(size_new,N_new,0,0,0,1,F);#interpolate to a new grid
    F=LP.Forvard(-z,F) #Propagate back to the near field
    F=LP.Interpol(size,N,0,0,0,1,F) #interpolate to the original grid
    F=LP.SubIntensity(Inear,F) #Substitute the measured near field into the field
    F=LP.Forvard(z,F) #Propagate to the far field

#The recovered far- and near field and their phase- and intensity
#distributions (phases are unwrapped (i.e. remove multiples of PI)):
Ffar_rec=F;
Ifar_rec=LP.Intensity(0,Ffar_rec); Phase_far_rec=LP.Phase(Ffar_rec);

Phase_far_rec=np.unwrap(np.unwrap(Phase_far_rec,np.pi,0),np.pi,1);
Fnear_rec=LP.Forvard(-z,F);
Inear_rec=LP.Intensity(0,Fnear_rec); Phase_near_rec=LP.Phase(Fnear_rec);
Phase_near_rec=np.unwrap(np.unwrap(Phase_near_rec,np.pi,1),np.pi,0);

#Plot the recovered intensity- and phase distributions:
plt.subplot(3,2,3);plt.imshow(Inear_rec);
plt.title('Recovered Intensity near field'); plt.axis ('off')
plt.subplot(3,2,4);plt.imshow(Ifar_rec);
plt.title('Recovered Intensity far field'); plt.axis ('off')
plt.subplot(3,2,5);plt.imshow(Phase_near_rec);
plt.title('Recovered phase near field');plt.axis ('off')
plt.subplot(3,2,6);plt.imshow(Phase_far_rec);
plt.title('Recovered phase far field'); plt.axis ('off')

plt.show()
