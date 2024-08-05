from LightPipes import *
import matplotlib.pyplot as plt
"""
    Young's experiment.
    Two holes with radii, R, separated by, d, in a screen are illuminated by a plane wave. The interference pattern
    at a distance, z, behind the screen is calculated.
"""
wavelength=5*um
size=20.0*mm
N=500
z=50*cm
R=0.3*mm
d=1.2*mm

F=Begin(size,wavelength,N)
F1=CircAperture(R/2.0,-d/2.0, 0, F)
F2=CircAperture(R/2.0, d/2.0, 0, F)    
F=BeamMix(F1,F2)
F=Fresnel(z,F)
I=Intensity(2,F)

s1 =    r'LightPipes for Python ' + LPversion + '\n'
s2 =    r'Young.py'+ '\n\n'\
        f'size = {size/mm:4.2f} mm' + '\n'\
        f'$\\lambda$ = {wavelength/um:4.2f} $\\mu$m' + '\n'\
        f'N = {N:d}' + '\n'\
        f'd = {d/mm:4.2f} mm distance between the holes' + '\n'\
        f'R = {R/mm:4.2f} mm radius of the holes' + '\n'\
        f'z = {z/mm:4.2f} mm distance to screen' + '\n\n'\
        r'${\copyright}$ Fred van Goor, June 2020'

fig=plt.figure(figsize=(9,9));
ax1 = fig.add_subplot(211);ax1.axis('off')
ax2 = fig.add_subplot(212);ax2.axis('off')

ax1.imshow(I,cmap='rainbow');ax1.set_title('intensity pattern')


ax2.text(0.0,1.0,s1,fontsize=12, fontweight='bold')
ax2.text(0.0,0.5,s2)

plt.show()
