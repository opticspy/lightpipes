from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

#wavelength HeNe laser:
wavelength=1000.0*nm
#grid size:
size=10*mm
#grid dimension:
N=1000
N2=int(N/2)
ZoomFactor=20
NZ=N2/ZoomFactor
#diameter of the annular slit:
d=1.0*mm
#width of the annular slit:
deltaD=60*um
#focal length and diameter of the lens:
f=500.0*mm; R=1.5*mm;
#distance after the lens where the Bessel beam is calculated:
z_start=0.001*cm; z_end= 150*cm; steps=10; delta_z=(z_end-z_start)/steps
#definition of a uniform plane wave:
x=range(-N2,N2)
x=np.asarray(x)*size/N/mm
Imax=np.zeros(steps)
z=np.zeros(steps)


F=Begin(size,wavelength,N);
#propagation through the annular slit:
F=GaussHermite(0,0,1,size/3.5,F)
F=CircScreen(R,0,0,F)
#F=CircAperture(R+0.1*mm,0,0,F)
#calculation of the intensity just after the slit:
I0=Intensity(2,F);

#Propagation to and through the lens:
#F=Fresnel(f,F);
#F=Lens(f,0,0,F);
for i in range(1,steps): 
   #propagation some distance z:
    F=Fresnel(delta_z,F);
    #F=Interpol(size/4,N,0,0,0,1,F)
    #calculation of the intensity at z:
    I=Intensity(0,F);
    #print(I[250][250])
    #Imax[i]=max(max(I))
    #Imax[i]=I[250][250]
    #Imax[i]=Power(F)
    y=np.asarray(I[N2])
    #plotting the results in figure 1:
    plt.subplot(2,5,i)
    #s='z= ' + str(z)
    #plt.title(s)
    #plt.imshow(I,vmin=0,vmax=0.5);
    #plt.plot(x,y)
    #plt.ylim([0,0.5])

    plt.imshow(I,cmap='jet');plt.axis('off')
    plt.axis([N2-NZ, N2+NZ, N2-NZ, N2+NZ])
    z[i]=z_start+i*delta_z
    #plt.axis('off'); 
plt.show()
#plt.plot(z/cm,Imax)
#plt.xlabel('z [cm]')
#plt.show()
