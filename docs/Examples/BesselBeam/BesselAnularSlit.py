from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np

#wavelength HeNe laser:
wavelength=632.8*nm
#grid size:
size=6*mm
#grid dimension:
N=500
N2=int(N/2)
#diameter of the annular slit:
d=2.5*mm
#width of the annular slit:
deltaD=30*um
#focal length and diameter of the lens:
f=305.0*mm; R=3.5*mm;
#distance after the lens where the Bessel beam is calculated:
z=0.001*cm;
#definition of a uniform plane wave:
x=range(-N2,N2)
x=np.asarray(x)*size/N/mm
for i in range(1,10):
    F=Begin(size,wavelength,N);
    #propagation through the annular slit:
    
    F=CircScreen((d-deltaD)/2,0,0,F); F=CircAperture(d/2,0,0,F);
    #calculation of the intensity just after the slit:
    I0=Intensity(2,F);
    
    #Propagation to and through the lens:
    F=Forvard(f,F);
    F=Lens(f,0,0,F);
    F=CircAperture(R,0,0,F);
    #propagation some distance z:
    F=Fresnel(z,F);
    
    #calculation of the intensity at z:
    I=Intensity(0,F);
    print(I[250][250])
    y=np.asarray(I[N2])
    #plotting the results in figure 1:
    plt.subplot(2,5,i)
    #s='z= ' + str(z)
    #plt.title(s)
    #plt.imshow(I,vmin=0,vmax=0.5);
    plt.plot(x,y)
    plt.ylim([0,0.5])

    plt.axis('off'); 
    z=z+10*cm;

plt.show()
