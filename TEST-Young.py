#! python3

import time
import sys
import matplotlib.pyplot as plt

print('Executed with python version:')
print(sys.version);print('\n')

start_time = time.time()

from LightPipes import *
print('test LightPipes installation: ');LPtest()
print('using LightPipes version: ',LPversion)

wavelength=20*um
size=30.0*mm
N=500

#LPhelp()
F=Begin(size,wavelength,N)
F1=CircAperture(0.15*mm, -0.6*mm,0, F)
F2=CircAperture(0.15*mm, 0.6*mm,0, F)    
F=BeamMix(F1,F2)
F=Fresnel(10*cm,F)
I=Intensity(2,F)

print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time))   
#plt.imshow(I);
plt.contourf(I,50); plt.axis('equal')
plt.show()

