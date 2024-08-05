from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
wavelength=1*um
size=25.0*mm
N=2000
N2=int(N/2)
z=80*cm
d=8*mm
f=100*cm
F=Begin(size,wavelength,N)
F=CircAperture(d/2, 0, 0, F)
F=Fresnel(F,z)
I1=Intensity(F)
F=Lens(F,f)
F=Forvard(f,F)
I=Intensity(0,F)

s1 =    r'LightPipes for Python' + '\n'
s2 =    r'RoundHole.py'+ '\n\n'\
        f'size = {size/mm:4.2f} mm' + '\n'\
        f'$\\lambda$ = {wavelength/um:4.2f} $\\mu$m' + '\n'\
        f'N = {N:d}' + '\n' +\
        f'f = {f/cm:4.2f} cm focal length' + '\n'\
        f'd = {d/mm:4.2f} mm hole diameter' + '\n'\
        f'z = {z/cm:4.2f} cm distance from hole to lens' + '\n'\
        r'${\copyright}$ Fred van Goor, February 2021'

fig=plt.figure(figsize=(11,6))
fig.suptitle("Diffraction from a round hole")
ax1 = fig.add_subplot(221);ax1.axis('off')
ax2 = fig.add_subplot(222);ax2.axis('off')
ax3 = fig.add_subplot(223);ax3.axis('off')
ax4 = fig.add_subplot(224)
ax1.set_title(f'Intensity pattern after {z/cm:4.1f} cm propagation')
ax1.imshow(I1,cmap='jet')
ax2.set_xlim(N2-50,N2+50)
ax2.set_ylim(N2-50,N2+50)
ax2.set_title('Intensity pattern at the focus of the lens')
ax2.imshow(I,cmap='jet')
ax3.text(0.0,1.0,s1,fontsize=12, fontweight='bold')
ax3.text(0.0,0.3,s2)
X=np.linspace(-size/2,size/2,N)
ax4.plot(X/mm,I[N2]); ax4.set_xlabel('x[mm]'); ax4.set_ylabel('Intensity [a.u.]')
ax4.set_xlim(-1,1)
plt.show()
