from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import numpy as np

#Convert rgb to gray with weighted average of rgb pixels:
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

#read image from disk and check if it is square:
img=mpimg.imread('arrow.png')
img=rgb2gray(img)
data = np.asarray( img, dtype='uint8' )
Nr=data.shape[0]
Nc=data.shape[1]
if Nc != Nr:
    print ('image must be square')
    exit()
else:
    N=Nc

size=25*mm
wavelength=1*um

R=6*mm
xs=2*mm
ys=0*mm

F=Begin(size,wavelength,N)
F=GaussAperture(R,xs,ys,1,F)
F=MultIntensity(img,F)
I=Intensity(0,F)

plt.imshow(I,cmap='gray'); plt.axis('off'); plt.title('Intensity')
plt.show()


