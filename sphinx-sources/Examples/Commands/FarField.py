from LightPipes import *
import matplotlib.pyplot as plt

labda=1000*nm;
size=10*mm;
N=256;
f1=10*m
f2=1.111111*m
z=1*m
w=5*mm;


F=Begin(size,labda,N);
F=RectAperture(w,w,0,0,0,F);
F=Lens(f1,0,0,F);
F=LensFresnel(f2,z,F);
F=Convert(F);
phi=Phase(F);#phi=PhaseUnwrap(phi)
I=Intensity(0,F);
x=[]
for i in range(N):
    x.append((-size/2+i*size/N)/mm)

plt.plot(x,phi[int(N/2)]);
plt.xlabel('x [mm]');
plt.ylabel('Intensity');
#plt.imshow(I)
plt.show()
