from LightPipes import *
import matplotlib.pyplot as plt
print(type(True))
LPtest()
N=5
F=Begin(20*mm,1500*nm,500)
print(type(F))
w0=3*mm
z=100*cm
xshift, yshift=1*mm, -1*mm
F=SuperGaussAperture(F, w0, n=20)
#F=CircScreen(F,w0)
#F=CircScreen(w0,xshift,yshift,F)
#F=CircScreen(F,y_shift=yshift,R=w0,x_shift=xshift)
#F=CircScreen(F,w0,xshift,yshift)
#help(CircScreen)

F=GaussHermite(F,w0,m=2,n=3,A=2)
#F=GaussHermite(2,3,2,w0,F)

#F=GaussLaguerre(F, w0, p=3, l=0, A=1.0)
#F=GaussLaguerre(3,0,1.0,w0,F)

#F=GaussBeam(F,w0,doughnut=True, m=1)
print(type(Strehl))
#F=GaussBeam(F,w0)
F1=PhaseSpiral(F,m=2)
phase=Phase(F1)
#phase=1.2345*rad
F=MultPhase(F,phase)
F=Fresnel(z,F)
I=Intensity(F)
print(type(I))
plt.imshow(I,cmap='jet')
#plt.imshow(Phase(F,unwrap=True,units='rad')); plt.colorbar()
plt.show()
