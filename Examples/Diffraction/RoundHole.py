import LightPipes
import matplotlib.pyplot as plt
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
	LP=LightPipes.Init()
	
	wavelength=1*um
	size=25.0*mm
	N=300
	
	F=LP.Begin(size,wavelength,N)
	F=LP.CircAperture(5*mm, 0, 0, F)
	#F=LP.CircScreen(5*mm, 0, 0, F)
	#F=LP.RectScreen(5*mm, 5*mm,0,0*mm,0,F)
	F=LP.Forvard(100*cm,F)
	#F=LP.Forvard(10*cm,F)
	#F=LP.Interpol(size*2,N/2,0,0,0,1,F)
	I=LP.Intensity(2,F)
	#plt.plot(I[N/2][:N])
	plt.imshow(I)
	plt.show()
    
finally:
	del LightPipes
