#! python3
import LightPipes as lp
import time
import sys
import matplotlib.pyplot as plt
print('Executed with python version:')
print(sys.version);print('\n')

start_time = time.time()

m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
    LP=lp.Init()

    wavelength=20*um
    size=30.0*mm
    N=500
    print('using LightPipes version: ')
    LP.version();print('\n')
    #LP.help()
    F=LP.Begin(size,wavelength,N)
    F1=LP.CircAperture(0.15*mm, -0.6*mm,0, F)
    F2=LP.CircAperture(0.15*mm, 0.6*mm,0, F)    
    F=LP.BeamMix(F1,F2)
    F=LP.Forvard(10*cm,F)
    I=LP.Intensity(2,F)
    print("Execution time: --- %4.2f seconds ---" % (time.time() - start_time))   
    #plt.imshow(I);
    plt.contourf(I,50); plt.axis('equal')
    plt.show()
finally:
    del lp
