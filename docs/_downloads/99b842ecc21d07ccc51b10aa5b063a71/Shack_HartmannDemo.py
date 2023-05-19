#! python3
import numpy as np
import matplotlib.pyplot as plt
from LightPipes import *
"""
    Shack_HartmannDemo.py
    Demonstrates a Shack Hartmann sensor.
    
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

X=np.arange(N)
X=(X/N-1/2)*size/mm

F1=Forvard(F,f)
Iscreen1=Intensity(F1,1)

F2=Zernike(F, 2, 0, size/2, 3, norm='True', units='lam'); S=ZernikeName(4) # Defocus
#F2=Zernike(F,3,-1,size/2,2,norm='True',units='lam'); S=ZernikeName(7)# Vertical coma 
F2=Fresnel(F2,f)
Iscreen2=Intensity(F2,1)

s= r'LightPipes for Python,' + '\n' +\
  r'Shack_HartmannDemo.py'+ '\n\n'\
  r'size = {:4.2f} mm'.format(size/mm) + '\n' +\
  r'$\lambda$ = {:4.2f} nm'.format(wavelength/nm) + '\n' +\
  r'N = {:d}'.format(N) + '\n' +\
  r'Diameter lenses: {:4.2f} mm'.format(Dlens/mm) + '\n' +\
  r'separation lenses in x: {:4.2f} mm'.format(x_sep/mm) + '\n' +\
  r'separation lenses in y: {:4.2f} mm'.format(y_sep/mm) + '\n' +\
  r'number of lenses per row: {:d}'.format(Nfields) + '\n' +\
  r'focal lengths of the lenses: {:4.2f} cm'.format(f/cm) + '\n\n' +\
  r'${\copyright}$ Fred van Goor, June 2020'
  
fig=plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222); #ax2.set_ylim(bottom=130,top=170)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.imshow(Ifields,cmap='gray',aspect='equal');ax1.axis('off'); ax1.set_title('Intensity just behind the lens array.')
ax2.imshow(Iscreen1,cmap='jet',aspect='equal');ax2.axis('off'); ax2.set_title('Intensity distribution at the focus of the lenses')
ax3.plot(X,Iscreen1[int(N/2)]); ax3.set_xlabel('x [mm]'); ax3.set_ylabel('Intensity [a.u.]'); ax3.set_title('Cross section of intensity at the focus')
ax4.text(0,0,s); ax4.axis('off')
plt.show()




