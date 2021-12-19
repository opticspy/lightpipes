#! /usr/bin/env python
"""
Script to test the new usePyFFTW option to compare pyFFTW and numpy FFT
"""
import time

from LightPipes import *
start_time = time.time()

wavelength = 500*nm
size = 25*mm
N = 1000

F=Begin(size, wavelength, N)
F=Fresnel(F, 100, usepyFFTW = True)
print(F.field[23,33])
#Fresnel: (1.0795142552372512+0.45098289321969964j)
#Forvard: (0.9865686238070652+0.16334733092228165j)

print("--- %s seconds ---" % (time.time() - start_time))

