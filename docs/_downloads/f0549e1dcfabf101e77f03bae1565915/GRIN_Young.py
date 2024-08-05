#! /usr/bin/env python
"""
    GRIN_Young.py
    
    Young's experiment with a GRIN lens.
    
    The propagation of a Gaussian beam propagating in a lens-like medium.
    See for example:
    Herwig Kogelnik
    On the Propagation of Gaussian Beams of Light Through
    Lenslike Media Including those with a Loss or Gain Variation.
    p. 1562 APPLIED OPTICS / Vol. 4, No. 12 / December 1965
    
    SELFOC Micro Lens: https://www.gofoton.com/
    
    cc Fred van Goor, May 2020
"""
from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
if LPversion < "2.0.0":
    print(r'You need to upgrade LightPipes to run this script.' + '\n'+r'Type at a terminal prompt: $ pip install --upgrade LightPipes')
    exit(1)

size=350*um
wavelength=1310*nm
N=200; N2=int(N/2)

#refractive index:
n0=1.5916
sqrtA=0.597/mm
Pitch=0.25
z_pitch=2*np.pi*Pitch/sqrtA
#z=3.5*mm
z=z_pitch
n1=sqrtA**2

#shift of input beam:
x_shift = 100*um
y_shift =0

#step size and number of steps in z-direction:
dz=0.01*mm
NZ=int(z/dz)

X=np.linspace(-size/2,size/2,N)
Z=np.linspace(0,z,NZ)

#fill the refractive index list:
n=np.zeros([N,N])
for i in range(0,N-1):
    x=-size/2+i*size/N
    for j in range(1,N):
        y=-size/2+j*size/N
        #n[i][j]=np.sqrt(n0*n0-n0*n1*(x*x+y*y))
        n[i][j]=n0-1/2*n1*(x*x+y*y)

K=np.pi*2/wavelength
w0=1.0*np.sqrt(2/K/np.sqrt(n0*n1)) #formula 53 in Kogelnik

F=Begin(size,wavelength/n0,N)
#F1=GaussBeam(w0,F,xshift= x_shift, yshift=y_shift)
#F2=GaussBeam(w0,F,xshift=-x_shift, yshift=y_shift)
F1=CircAperture(w0, x_shift,0,F)
F2=CircAperture(w0,-x_shift,0,F)
F=BeamMix(F1,F2)
Iin=Intensity(0,F)
Icross=np.zeros((NZ,N))
Ic=np.zeros(NZ)
for k in range(0,NZ):
    print(k)
    F=Steps(dz,1,n,F)
    I=Intensity(0,F)
    Ic[k]=I[N2][N2]
    Icross[k,:] = I[N2][:]
F=Fresnel(1.25*mm,F)
Iout=Intensity(1,F)

fig, _axs = plt.subplots(nrows=2, ncols=3,figsize=(12.0,6.5))
fig.suptitle('Young\'s interferometer with a GRIN lens')
fig.subplots_adjust(hspace=0.3)
axs = _axs.flatten()

axs[0].contourf(X/um, Z/mm, Icross,cmap='rainbow')
axs[0].grid(color='white', ls='solid')
axs[0].set_xlabel(r'x [$\mu{m}$]')
axs[0].set_ylabel(r'z [mm]')
axs[0].set_title(r'cross section of intensity')

s = r'LightPipes for Python,' + '\n'+ 'GRIN_Young.py' + '\n\n'\
    r'SELFOC GRIN lens(https://www.gofoton.com/)' + '\n'\
    r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/um) + r' $\mu{m}$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$n_0 = {:4.4f}$'.format(n0) + '\n'\
    r'$\sqrt{A} = $' + '{:4.3f}'.format(sqrtA*mm) + r' $mm^{-1}$' + '\n'\
    r'$pitch = {:4.2f}$'.format(Pitch) + '\n'\
    r'$z_{pitch} = $' + '{:4.2f}'.format(z_pitch/mm) + r' $mm$' + '\n'\
    r'$dz = {:4.2f}$'.format(dz/um) + r' $\mu{m}$' + '\n'\
    r'$x_{shift} = $' + '{:4.2f}'.format(x_shift/um) + r' $\mu{m}$' + '\n'\
    r'$y_{shift} = $' + '{:4.2f}'.format(y_shift/um) + r' $\mu{m}$' + '\n'\
    r'$w_0 = {:4.2f}$'.format(w0/um) + r' $\mu{m}$' + '\n'\
    r'${\copyright}$ Fred van Goor, May 2020'
    
axs[1].text(0,-0.2,s)
axs[1].axis('off')

axs[2].imshow(Iin,cmap='rainbow')
axs[2].set_title('Input')
axs[2].tick_params(axis='x', colors=(0,0,0,0))
axs[2].tick_params(axis='y', colors=(0,0,0,0))

axs[3].plot(X/um,Iout[N2],label='Output')
axs[3].plot(X/um,Iin[N2],label='Input')
axs[3].set_xlabel(r'x [$\mu{m}$]')
axs[3].set_ylabel(r'intensity [a.u.]')
axs[3].legend(bbox_to_anchor=(1.05, 1.05))

axs[4].axis('off')

axs[5].imshow(Iout,cmap='rainbow')
axs[5].set_title('Output')
axs[5].tick_params(axis='x', colors=(0,0,0,0))
axs[5].tick_params(axis='y', colors=(0,0,0,0))

plt.show()
