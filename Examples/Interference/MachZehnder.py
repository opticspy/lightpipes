#! /usr/bin/env python
try:
	import LightPipes
except ImportError:
	print ("LightPipes not present")
	exit()

import matplotlib.pyplot as plt
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
	LP=LightPipes.Init()

	wavelength=500*nm
	size=8.0*mm
	N=1000
	R=300*mm
	d1=340*mm
	d2=340*mm
	f=300*mm
	f1=3000*mm
	z=190*mm
	
	f2=1/(1/f-1/f1)

	F=LP.Begin(size,wavelength,N)
	F=LP.CircAperture(R, 0, 0, F)
	#I=LP.Intensity(2,F)
	F1=LP.Forvard(d1,F)
	F2=LP.Forvard(d2-z,F)
	F2=LP.Lens(f1,0,0,F2)
	F2=LP.LensForvard(f2,z,F2)
	F2=LP.Convert(F2)
	size_new=LP.getGridSize()
	#print(size_new/mm)
	F1=LP.Interpol(size_new,N,0,0,0,1,F1)
	F=LP.BeamMix(F1,F2)
	I=LP.Intensity(2,F)
	plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
	plt.show()

finally:
	del LightPipes
