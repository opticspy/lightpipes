from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

wavelength=1*um
size=5.0*mm

arrow=mpimg.imread('arrow.png')[:,:,0]
N=arrow.shape[0]

F=Begin(size,wavelength,N)
F=SubIntensity(arrow,F)
I0=Intensity(2,F)
plt.imshow(I0)
F=Fresnel(5*cm,F)
I=Intensity(2,F)

fig = plt.figure()
plt.imshow(I)
plt.show()
