import LightPipes
import matplotlib.pyplot as plt
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
	LP=LightPipes.Init()
	
	wavelength=5*um
	size=25.0*mm
	N=500
	
	F=LP.Begin(size,wavelength,N)
	F=LP.GaussHermite(0,0,1,size/3,F)
	F=LP.CircScreen(3*mm,0*mm,0*mm,F)
	F=LP.Fresnel(20*cm,F)
	I=LP.Intensity(2,F)
	plt.imshow(I); plt.axis('off'); plt.title("Poisson's spot")
	plt.show()
    
finally:
	del LightPipes
