import LightPipes
import matplotlib.pyplot as plt
#from scipy import misc
import matplotlib.image as mpimg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
	LP=LightPipes.Init()
	wavelength=1*um
	size=5.0*mm
	dz=10*mm
	N=100
 
	mask=mpimg.imread('mask1.png')[:,:,0]

	F=LP.Begin(size,wavelength,N)
	F=LP.SubIntensity(mask,F)
	I0=LP.Intensity(2,F)
	plt.imshow(I0)
	F=LP.Fresnel(0.5*m,F)
	I=LP.Intensity(2,F)

	fig = plt.figure()
	plt.imshow(I)
	plt.show()
finally:
	del LightPipes
