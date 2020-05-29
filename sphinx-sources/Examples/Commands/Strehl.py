from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

wavelength=1.0*um
size=30*mm
N=200
w=25*mm
S=[]
MaxPhase=[]
for i in range(0,20):
    MaxPhase.append(i)
    seed=i
    F=Begin(size,wavelength,N)
    F=RandomPhase(seed,MaxPhase[i],F)
    S.append(Strehl(F))
plt.plot(MaxPhase,S)
plt.title('Strehl ratio of a beam with random phase\n as a function of the amplitude of the phase fluctuations')
plt.ylabel('Strehl ratio')
plt.xlabel('MaxPhase')
plt.show()

