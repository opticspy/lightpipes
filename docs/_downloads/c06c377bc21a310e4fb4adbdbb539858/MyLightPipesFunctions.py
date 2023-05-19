from LightPipes import *
from MyFunctions.MyLightPipesFunctions import CylindricalLens
import matplotlib.pyplot as plt
import numpy as np
"""
    Script to test the user-defined CylindricalLens command.
"""
size=15*mm
wavelength=1*um
N=500
R=4.5*mm
f=1.89*m
angle=90*deg
x_shift=0*mm
y_shift=0*mm

Field = Begin(size, wavelength, N)
Field = CircAperture(R, 0, 0, Field)
I0 = Intensity(1,Field)
Field=CylindricalLens(Field,f,angle=angle,x_shift=x_shift,y_shift=y_shift)
#Field=CylindricalLens(Field,F)
Field = Fresnel(f, Field)
I1 = Intensity(1,Field)
I1=np.array(I1)
x=np.linspace(-size/2.0,size/2.0,N)/mm

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

s1 =r'LightPipes for Python'
s2 =r'MyLightPipesFunctions.py' + '\n'\
    r'User defined function test: CylindricalLens' + '\n\n'\
    r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$R = {:4.2f}$'.format(R/mm) + r' $mm$'+ '\n'\
    r'$f = {:4.1f}$'.format(f/cm) + r' $cm$' + '\n'\
    r'$\alpha = {:4.1f}$'.format(angle/deg) + r' $deg$' + '\n'\
    r'$x_{shift} = ' + '{:4.2f}$'.format(x_shift/mm) + r' $mm$' + '\n'\
    r'$y_{shift} = ' + '{:4.2f}$'.format(y_shift/mm) + r' $mm$'

ax1.imshow(I0,cmap='gray'); ax1.axis('off')
ax2.imshow(I1,cmap='jet'); ax2.axis('off')
ax3.text(0.0,1.0,s1,fontsize=12, fontweight='bold');ax3.text(0.0,0.0,s2); ax3.axis('off')
ax4.plot(x,I1[int(N/2)],x,list(zip(*I1))[int(N/2)])

ax4.set_xlabel('x [mm]');ax4.set_ylabel('Intensity [a.u.]')
plt.show()
