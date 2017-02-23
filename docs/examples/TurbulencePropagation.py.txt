import LightPipes
import matplotlib.pyplot as plt
import matplotlib.animation as animation

m=1;
nm=1e-9*m;
mm=1e-3*m;
cm=1e-2*m;

wavelength=633*nm;
size=20*cm;
N=512;
LP=LightPipes.Init()

ims=[]
fig = plt.figure()
for frameN in range(1,100):
	F=LP.Begin(size, wavelength, N);
	F=LP.GaussAperture(size/4, 0, 0, 1, F);
	F=LP.Turbulence(size/8,F);
	F=LP.Lens(1000*m,0,0,F);
	F=LP.Forvard(1000*m,F);
	F=LP.Intensity(1,F);
	im=plt.imshow(F); plt.axis('off')
	ims.append([im])
ani = animation.ArtistAnimation(fig, ims, interval=50)
ani.save('turbulence.mp4')
plt.show()

