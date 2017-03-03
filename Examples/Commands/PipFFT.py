from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

F=Begin(0.01,1e-6,500);
F=CircAperture(0.003,0,0,F);
F=RandomPhase(3,5,F);
F=Fresnel(1,F);
Iunf=Intensity(1,F);
fig = plt.figure()
plt.imshow(Iunf);
F=PipFFT(1,F);
F=CircAperture(0.0001,0,0,F);
F=PipFFT(-1,F);
Ifil=Intensity(1,F);
fig = plt.figure()
plt.imshow(Ifil);
plt.show()
