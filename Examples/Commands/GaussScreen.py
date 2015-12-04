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
    w=0.2*mm
    T=2
    z=1*m
    dx=1.0*mm
    dy=1.0*mm

    F=LP.Begin(size,wavelength,N)
    F=LP.GaussScreen(w,dx,dy,T,F)
    F=LP.Forvard(z,F)
    I=LP.Intensity(2,F)
    plt.imshow(I)
    #plt.plot(I[N/2][:N])
    plt.show()
    
finally:
	del lp
