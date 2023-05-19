#! python3
import numpy as np
import matplotlib.pyplot as plt
from LightPipes import *
"""
    MultiHole.py
    Demonstrates the MultiHole command. Two wavelengths are used to show 
    the principles of a grating.
    
    cc Fred van Goor, June 2020.
"""
wavelength=1000*nm
size=30*mm
N=800
N2=int(N/2)

HoleSeparation=2*mm
z=300*cm
Nholes=6
size_hole=1*mm
HoleDiameter=0.5*mm

Ndiameter=int(HoleDiameter/size*N)
Nhole=int(size_hole/size*N)
Fhole=Begin(size_hole,wavelength,Nhole)
Fhole=CircAperture(Fhole,HoleDiameter/2)

F=Begin(size,wavelength,N)
F=RowOfFields(F,Fhole,Nholes,HoleSeparation)
Iholes=Intensity(F)
X=np.arange(N)
X=(X/N-1/2)*size/mm
F=Lens(F,z)
F=Fresnel(F,z)
Iscreen=Intensity(F)

s= r'LightPipes for Python,' + '\n' +\
  r'MultiHole.py'+ '\n\n'\
  r'size = {:4.2f} mm'.format(size/mm) + '\n' +\
  r'$\lambda$ = {:4.2f} nm'.format(wavelength/nm) + '\n' +\
  r'N = {:d}'.format(N) + '\n' +\
  r'diameter holes: {:4.2f} mm'.format(HoleDiameter/mm) + '\n' +\
  r'separation of the holes: {:4.2f} mm'.format(HoleSeparation/mm) + '\n' +\
  r'number of holes: {:d}'.format(Nholes) + '\n' +\
  r'focal length lens: {:4.2f} cm'.format(z/cm) + '\n\n' +\
  r'${\copyright}$ Fred van Goor, May 2020'
  
fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222);# ax2.set_ylim(bottom=130,top=170)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.imshow(Iholes,cmap='gray',aspect='equal');ax1.axis('off'); ax1.set_title('Screen with holes')
ax2.imshow(Iscreen,cmap='jet',aspect='equal');ax2.axis('off'); ax2.set_title('Intensity distribution at the focus of the lens')
ax3.plot(X,Iscreen[N2]); ax3.set_xlabel('x [mm]'); ax3.set_ylabel('Intensity [a.u.]'); ax3.set_title('Cross section of intensity at the focus')
ax4.text(0,0,s); ax4.axis('off')
plt.show()

