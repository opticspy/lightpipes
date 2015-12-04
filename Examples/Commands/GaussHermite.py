import LightPipes as lp
import matplotlib.pyplot as plt
m=1
nm=1e-9*m
um=1e-6*m
mm=1e-3*m
cm=1e-2*m

try:
    LP=lp.Init()
    
    wavelength=500*nm
    size=5.0*mm
    N=100
    w0=0.2*mm
    A=1
    z=1*m
 
    F=LP.Begin(size,wavelength,N)
    F=LP.GaussHermite(2,3,A,w0,F)
    F=LP.Fresnel(z,F)
    I=LP.Intensity(2,F)
    plt.imshow(I)
    plt.show()
    
finally:
	del lp
