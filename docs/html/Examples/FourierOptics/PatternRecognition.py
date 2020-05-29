from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

f=0.6*m
gridsize=14*mm
wavelength=632.8*nm

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    
def Fouriertransform(F):
    F=Forvard(f,Lens(f,0,0,Forvard(f,F)))
    return F

def MakePhaseFilter(img):
    F=Begin(gridsize,wavelength,N)
    F=SubIntensity(img,F)
    F=Fouriertransform(F)
    phase=np.asarray(np.negative(Phase(F)))
    return phase


img=[
    rgb2gray(mpimg.imread('A.png')),
    rgb2gray(mpimg.imread('B.png')),
    rgb2gray(mpimg.imread('C.png')),
    rgb2gray(mpimg.imread('X.png'))
    ]
ABC=rgb2gray(mpimg.imread('ABC.png'))

choice=['A','B','C']

N=ABC.shape[0]
X=range(N)
Z=range(N)
X, Z=np.meshgrid(X,Z)

#plt.contourf(X,Z,ABC,cmap='gray');plt.axis('off');plt.axis('equal')
#plt.show()

F1=Begin(gridsize,wavelength,N)
F1=MultIntensity(ABC,F1)
F1=Fouriertransform(F1)
I_NOFILTER=Intensity(0,Fouriertransform(F1))
#phase=MakePhaseFilter(img[0])
#plt.contourf(X,Z,phase,cmap='hot');plt.axis('off');plt.axis('equal')
#plt.show()
#phase=MakePhaseFilter(img[0])
#F=MultPhase(phase,F1)
#I=Intensity(1,Fouriertransform(F))
#plt.contourf(X,Z,I,cmap='hot');plt.axis('off');plt.axis('equal')
#plt.show()
fig, axs = plt.subplots(1,4,figsize=(12,5))
fig.suptitle('Pattern recognition\nusing Fourier optics', fontsize=20)
fig.canvas.set_window_title('Pattern recognition example')
axs[0].contourf(X,Z,I_NOFILTER,cmap='hot');
axs[0].axis('off');axs[0].axis('equal');
axs[0].text(50,N,'non-filtered image')

for l in range(3):
    phase=MakePhaseFilter(img[l])
    F=MultPhase(phase,F1)
    I=Intensity(1,Fouriertransform(F))
    plt.contourf(X,Z,I,cmap='hot');plt.axis('off');plt.axis('equal')
    axs[l+1].contourf(X,Z,I,cmap='hot');
    axs[l+1].axis('off');
    axs[l+1].axis('equal');
    axs[l+1].text(100,N,choice[l])

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.01, hspace=None)
plt.show()
