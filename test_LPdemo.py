from LightPipes import *
import matplotlib.pyplot as plt
import sys
import platform

m=1
mm=1e-3*m
cm=1e-2*m
um=1e-6*m
wavelength=20*um
size=30.0*mm
N=500

F=Begin(size,wavelength,N)
F1=CircAperture(0.15*mm, -0.6*mm,0, F)
F2=CircAperture(0.15*mm, 0.6*mm,0, F)    
F=BeamMix(F1,F2)
F=Fresnel(10*cm,F)
I=Intensity(0,F)

fig=plt.figure(figsize=(13,6))
fig.subplots_adjust(hspace=0.1)
ax1 = fig.add_subplot(121)
ax1.set_title('Interference pattern of a two holes interferometer')
ax1.axis('off')
ax2 = fig.add_subplot(122)
ax2.axis('off')
ax1.imshow(I,cmap='rainbow')

s=  '\n\nLightPipes for Python demo' + '\n'\
    'Python script of a two-holes interferometer:'+ '\n\n'\
    'from LightPipes import *'+'\n'\
    'import matplotlib.pyplot as plt'+'\n'\
    'import sys'+'\n'\
    'import platform'+'\n'\
    'wavelength=20*um'+'\n'\
    'size=30.0*mm'+'\n'\
    'N=500'+'\n\n'\
    'F=Begin(size,wavelength,N)'+'\n'\
    'F1=CircAperture(0.15*mm, -0.6*mm,0, F)'+'\n'\
    'F2=CircAperture(0.15*mm, 0.6*mm,0, F)'+'\n'\
    'F=BeamMix(F1,F2)'+'\n'\
    'F=Fresnel(10*cm,F)'+'\n'\
    'I=Intensity(0,F)'+'\n\n'\
    '# plot ...'+ '\n'\
    'fig=plt.figure(figsize=(13,6))'+'\n'\
    'fig.subplots_adjust(hspace=0.1)'+'\n'\
    'ax1 = fig.add_subplot(121)'+'\n'\
    'ax1.set_title("Interference pattern of a two holes interferometer")'+'\n'\
    'ax1.axis("off")'+'\n'\
    'ax2 = fig.add_subplot(122)'+'\n'\
    'ax2.axis("off")'+'\n'\
    'ax1.imshow(I,cmap=rainbow")'+'\n'\
    'plt.show()'+'\n\n'\
    'Executed with python version: '+ '\n\n' + sys.version +'\n'\
    'on a ' + platform.system() + ' ' + platform.release() +' '+ platform.machine() +' machine'
    
ax2.text(-0.1,0.0,s)#, va = 'bottom')
#print('Executed with python version: ' + sys.version)
#print('on a ' + platform.system() + ' ' + platform.release() + ' ' + platform.machine() +' machine')
plt.show()
