from LightPipes import *
import matplotlib.pyplot as plt

GridSize = 10*mm
GridDimension = 128
lambda_ = 500*nm #lambda_ is used because lambda is a Python build-in function.

R=2.5*mm #Radius of the aperture
xs=1*mm; ys=1*mm#shift of the aperture

Field = Begin(GridSize, lambda_, GridDimension)
Field=CircAperture(R,xs,ys,Field)
I=Intensity(0,Field)

plt.imshow(I); plt.axis('off')
plt.show()
