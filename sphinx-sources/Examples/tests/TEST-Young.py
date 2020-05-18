#! python3

#import time
import matplotlib.pyplot as plt

#print('Executed with python version: ' + sys.version)

#start_time = time.time()

from LightPipes import *
#help(LPdemo)
#LPdemo()
#print('using LightPipes version: ' + LPversion)
#LPtest()

wavelength=20*um
size=30.0*mm
N=500

#LPhelp()
#F=Begin(size,wavelength,N)
#F=GaussBeam(size,wavelength,N,size/40,0.04,0)
F1=PointSource(size,wavelength,N,-0.6*mm,0)
F2=PointSource(size,wavelength,N, 0.6*mm,0)

#F1=CircAperture(0.15*mm, -0.6*mm,0, F)
#F2=CircAperture(0.15*mm, 0.6*mm,0, F)    
F=BeamMix(F1,F2)
F=Fresnel(10*cm,F)
I=Intensity(0,F)

#print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time))   
plt.imshow(I,cmap='rainbow');plt.axis('off')
#plt.contourf(I,50); plt.axis('equal')
plt.show()

