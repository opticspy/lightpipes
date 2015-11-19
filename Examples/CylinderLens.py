try:
	import LightPipes
except ImportError:
	print "LightPipes not present"
	exit()

import matplotlib.pyplot as plt
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m
pi=3.141592654

try:
	LP=LightPipes.Init()
	wavelength=1000*nm;
	size=10*mm;
	N=500;
	Radius=4.5*mm;
	fx=0.75*m;fy=1e300
	K=2*pi/wavelength
	F=LP.Begin(size,wavelength,N);
	F=LP.CircAperture(Radius,0,0,F);
	I0=LP.Intensity(2,F);
	plt.figure(1);
	plt.subplot(2,1,1);plt.axis('off')
	plt.imshow(I0);
	F=LP.CylLens(fx,fy,0,0,F)
	#F=LP.Zernike(2,-2,4.5*mm,20/K,F);
	#F=LP.Zernike(2,0,4.5*mm,-10/K,F);
	F=LP.Forvard(fx,F);
	#F=LP.Interpol(size,N,0,0,45,1,F);
	I2=LP.Intensity(2,F);
	plt.subplot(2,1,2);plt.axis('off')
	plt.imshow(I2);
	plt.show()
finally:
	del LightPipes

