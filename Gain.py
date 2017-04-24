from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
"""
    G Logan DesAutels, Dan Daniels, John O Bagford and Mike Lander,
    "High power large bore CO2 laser small signal gain coefficient and saturation intensity measurements.",
    J. Opt. A: Pure Appl. Opt. 5 (2003) 96-101
"""
wavelength=10.6*um
size=100*mm
N=100
w0=20*mm
It0=900.0*W/cm/cm; A=math.sqrt(It0)
Isat=133*W/cm/cm; alpha0=0.0064/cm; Lgain=210*cm;

F=Begin(size,wavelength,N)
F=GaussHermite(0,0,A,w0,F)
Iin=Intensity(1,F);Pin=Power(F)
F=Gain(2*Isat,alpha0,Lgain,F);Pout=Power(F)
Iout=Intensity(1,F)
print(Pout)
X=range(-50,50)
plt.plot(X,Iin[50],'k--',label='input')
plt.plot(X,Iout[50],'k',label='output')
plt.legend(loc='upper right', shadow=True)
plt.ylabel('normalized intensity')
plt.xlabel('x [mm]')
plt.show()

