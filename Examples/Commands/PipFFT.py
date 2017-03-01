import LightPipes
import matplotlib.pyplot as plt
import numpy as np
from LightPipes import cm, m, mm, nm, um


LP=LightPipes.Init()
F=LP.Begin(0.01,1e-6,500);
F=LP.CircAperture(0.003,0,0,F);
F=LP.RandomPhase(3,5,F);
F=LP.Fresnel(1,F);
Iunf=LP.Intensity(1,F);
fig = plt.figure()
plt.imshow(Iunf);
F=LP.PipFFT(1,F);
F=LP.CircAperture(0.0001,0,0,F);
F=LP.PipFFT(-1,F);
Ifil=LP.Intensity(1,F);
fig = plt.figure()
plt.imshow(Ifil);
plt.show()
