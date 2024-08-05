from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

wavelength=5*um
size=25.0*mm
N=2000
N2=int(N/2)
d=6*mm
w0=size/3
z=20*cm
F=Begin(size,wavelength,N)
F=GaussBeam(F, w0)
F=CircScreen(F,d/2)
F=Fresnel(F,z)
I=Intensity(F,1)

s1 =    r'LightPipes for Python' + '\n'
s2 =    r'Poisson.py'+ '\n\n'\
        f'size = {size/mm:4.2f} mm' + '\n'\
        f'$\\lambda$ = {wavelength/um:4.2f} $\\mu$m' + '\n'\
        f'N = {N:d}' + '\n' +\
        f'd = {d/mm:4.2f} mm disk diameter' + '\n'\
        f'w0 = {w0/mm:4.2f} mm radius Gauss beam' + '\n'\
        f'z = {z/cm:4.2f} cm distance from disk' + '\n'\
        r'${\copyright}$ Fred van Goor, February 2021'

fig=plt.figure(figsize=(11,6))
fig.suptitle("The spot of Poisson")
ax1 = fig.add_subplot(221);ax1.axis('off')
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223);ax3.axis('off')
ax1.set_xlim(N2-300,N2+300)
ax1.set_ylim(N2-300,N2+300)
ax1.imshow(I,cmap='jet')

ax1.set_title(f'Intensity pattern after {z/cm:4.1f} cm propagation')
X=np.linspace(-size/2,size/2,N)
ax2.plot(X/mm,I[N2]); ax2.set_xlabel('x[mm]'); ax2.set_ylabel('Intensity [a.u.]')
ax2.set_xlim(-1,1); ax2.set_title('The spot of Poisson')
ax3.text(0.0,1.0,s1,fontsize=12, fontweight='bold')
ax3.text(0.0,0.3,s2)
plt.show()
