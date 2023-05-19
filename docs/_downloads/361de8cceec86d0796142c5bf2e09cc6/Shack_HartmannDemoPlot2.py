#! python3
import numpy as np
import matplotlib.pyplot as plt
from LightPipes import *
"""
    Shack_HartmannDemoPlot2.py
    Demonstrates a Shack Hartmann sensor (Plot detailed figure).
    
    cc Fred van Goor, May 2020.
"""
wavelength=632.8*nm
size=5*mm
N=2000

x_sep=0.5*mm
y_sep=0.5*mm
size_field=1.0*x_sep
sy=0*mm
f=4*cm
Dlens=0.45*mm
Nfields=9
size=(Nfields+1)*x_sep

F=Begin(size,wavelength,N)
Nfield=int(size_field/size*N)
Ffield=Begin(size_field,wavelength,Nfield)
Ffield=CircAperture(Ffield,Dlens/2)
Ffield=Lens(Ffield,f)

F=FieldArray2D(F,Ffield,Nfields,Nfields,x_sep,y_sep)
Ifields=Intensity(F)

F1=Forvard(F,f)
Iscreen1=Intensity(F1,1)

F2=Zernike(F, 2, 0, size/2, 3, norm='True', units='lam'); S=ZernikeName(4) # Defocus
#F2=Zernike(F,3,-1,size/2,2,norm='True',units='lam'); S=ZernikeName(7)# Vertical coma 
F2=Fresnel(F2,f)
Iscreen2=Intensity(F2,1)

fig2=plt.figure(figsize=(8,8))
tick_step=200
plt.imshow(Iscreen1+Iscreen2,cmap='jet',aspect='equal');plt.axis('on');plt.xticks(np.arange(0, N, tick_step));plt.yticks(np.arange(0, N, tick_step))
plt.grid(color='white', ls='dotted',linewidth='0.6')
plt.title(r'Intensity distribution without- (at grid points) and with Zernike aberration:'+'\n'+S)
plt.show()



