from LightPipes import *
import matplotlib.pyplot as plt

Field=Begin(20*mm, 1*um, 256)
Field = CircAperture(5*mm, 0, 0, Field)
Field = Forvard(1*m, Field)
I = Intensity(0,Field)

x=[]
for i in range(256):
    x.append((-20*mm/2+i*20*mm/256)/mm)

fig=plt.figure(figsize=(15,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.imshow(I,cmap='rainbow'); ax1.axis('off')
ax2.plot(x,I[128]);ax2.set_xlabel('x [mm]');ax2.set_ylabel('Intensity [a.u.]')
ax2.grid('on')
plt.show()
