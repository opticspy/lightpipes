from LightPipes import *
import matplotlib.pyplot as plt

GridSize = 10*mm
GridDimension = 256
lambda_ = 1000*nm #lambda_ is used because lambda is a Python build-in function.

R=2.5*mm #Radius of the aperture
xs=1*mm; ys=1*mm#shift of the aperture

Field = Begin(GridSize, lambda_, GridDimension)
Field=CircScreen(0.7*mm,1*mm,1.5*mm,Field)
Field=RectScreen(1*mm,1*mm,-1.5*mm,-1.5*mm,-0.002,Field)
Field=RectScreen(1*mm,3.5*mm,-2*mm,2.5*mm,30,Field)
Field=GaussAperture(4*mm,0,0,1,Field)
I=Intensity(0,Field)

plt.imshow(I); plt.axis('off')
plt.show()
