from LightPipes import *
import matplotlib.pyplot as plt
LPtest()
N=5
F=Begin(30*mm,500*nm,5)
print(F.field)
# w0=1*mm
# z=100*cm
# xshift, yshift=0*mm, 0*mm
# #F=SuperGaussAperture(w0,0,0,1,20,F)
# F1=GaussBeam(w0,F,doughnut=True,l=12)
# phase=Phase(F1)

# F=GaussBeam(w0,F)
# F=PhaseSpiral(F,m=2,xshift=xshift,yshift=yshift)

# F=Fresnel(z,F)

# plt.imshow(Intensity(0,F),cmap='jet')
# #plt.imshow(Phase(F,unwrap=True,units='rad')); plt.colorbar()
# plt.show()
