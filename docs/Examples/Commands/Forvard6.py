from LightPipes import *
import matplotlib.pyplot as plt

Field=Begin(100*mm, 1*um, 256)
Field = CircAperture(25*mm,0, 0, Field)
I0=Intensity(0,Field)
Field = Forvard(30*m, Field)
I1 = Intensity(0,Field)
Field = Forvard(-30*m, Field)
I2 = Intensity(0,Field)

x=[]
for i in range(512):
    x.append((-20*mm/2+i*20*mm/512)/mm)

fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
ax1.imshow(I0,cmap='rainbow'); ax1.axis('off'); ax1.set_title('Initial field')
ax2.imshow(I1,cmap='rainbow'); ax2.axis('off'); ax2.set_title('Propagated to the near field')
ax3.imshow(I2,cmap='rainbow'); ax3.axis('off'); ax3.set_title('Propagated back')
plt.show()
