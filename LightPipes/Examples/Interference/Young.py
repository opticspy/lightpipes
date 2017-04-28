from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

img=mpimg.imread('Young.png')
plt.imshow(img); plt.axis('off')

plt.show()

F=Begin(size,wavelength,N)
F1=CircAperture(R/2.0,-d/2.0, 0, F)
F2=CircAperture(R/2.0, d/2.0, 0, F)    
F=BeamMix(F1,F2)
F=Fresnel(z,F)
I=Intensity(2,F)
plt.imshow(I, cmap='rainbow'); plt.axis('off');plt.title('intensity pattern')
plt.show()
