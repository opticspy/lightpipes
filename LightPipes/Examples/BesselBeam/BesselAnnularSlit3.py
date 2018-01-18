from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img=mpimg.imread('bessel3.png')
plt.imshow(img); plt.axis('off');plt.title('Bessel beam with annular slit')
plt.show()

wavelength=1000.0*nm
size=10*mm
N=1000

N2=int(N/2)
ZoomFactor=10
NZ=N2/ZoomFactor

a=1.5*mm
f=500*mm
z_start=0.001*cm; z_end= 150*cm;
steps=11;
delta_z=(z_end-z_start)/steps
z=z_start

F=Begin(size,wavelength,N);
F=GaussHermite(0,0,1,size/3.5,F)
F=CircScreen(a,0,0,F)
F=CircAperture(a+0.1*mm,0,0,F)
F=Fresnel(f,F);
F=Lens(f,0,0,F);
for i in range(1,steps): 
    F=Fresnel(delta_z,F);
    I=Intensity(0,F);
    plt.subplot(2,5,i)
    s='z= %3.1f m' % (z/m)
    plt.title(s)
    plt.imshow(I,cmap='jet');plt.axis('off')
    plt.axis([N2-NZ, N2+NZ, N2-NZ, N2+NZ])
    z=z+delta_z
plt.show()
