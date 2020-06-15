from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
"""
    LightPipes for Python
    *********************
    
    LaserModeTransformer.py

    Demonstrates the transformation of a Hermite Gauss resonator mode
    into a Laguerre Gauss mode with a pair of cylindrical lenses.
    
    Reference: 
    M.W. Beijersbergen, L. Allen, H.E.L.O. van der Veen and J.P. Woerdman,
    Astigmatic laser mode converters and transfer of orbital angular momentum,
    Optics Comm. 96 (1993) 123.
    
    cc Fred van Goor, June 2020.
"""
labda=632.8*nm
size=5*mm
N=500

dz=-30*mm # tune position lens f2
d1=525*mm
d2=306*mm
d3=225*mm + dz #225*mm
d4=176*mm - dz #176*mm
d5=27*mm #27*mm

df2=12*mm # tune focal length of f2
R1=600*mm
R2=437*mm
f1=20*mm
f2=160*mm +df2 #160*mm
f3=19*mm
f4=19*mm
f5=20*mm
angle=45.0*deg
m_=3
n_=0

L=d1+d2
g1=1-L/R1
g2=1-L/R2
w0=np.sqrt(labda*L/np.pi)
w0*=(g1*g2*(1-g1*g2))**0.25
w0/=(g1+g2-2*g2)**0.5
d5=f4*np.sqrt(2)
fM2=-R2/(1.5-1) #lensmakers formula with refractive index = 1.5, focal length outcoupler

F=Begin(size,labda,N)
F=GaussBeam(F,w0,m=m_,n=n_) # Hermite Gauss beam in waist
F=Forvard(F,d2) # propagate d2
F=Lens(F,fM2) #outcoupler as lens
F=Forvard(F,d3) #propagate d3
I0=Intensity(F) # intensity input beam
F=Lens(F,f2) # lens f2
F=Forvard(F,d4) # propagate d4
F=CylindricalLens(F,f3,angle=angle) # cylindrical lens f3
F=Forvard(F,d5) # propagate d5
F=CylindricalLens(F,f4,angle=angle) # cylindrical lens f4
F=Lens(F,f5) # lens f5
F=Forvard(F,200*mm) # propagate to have sufficient large beam size
I1=Intensity(F) #intensity output beam

s1 =    r'LightPipes for Python,' + '\n'\
        r'LaserModeTransformer.py'+ '\n\n'\
        f'size = {size/mm:4.2f} mm' + '\n'\
        f'$\lambda$ = {labda/nm:4.2f} nm' + '\n'\
        f'N = {N:d}' + '\n' +\
        f'm = {m_:d}, n = {n_}' + '\n'\
        f'w0 = {w0/mm:4.3f} mm' + '\n'\
        f'd1 = {d1/mm:4.1f} mm' + '\n'\
        f'd2 = {d2/mm:4.1f} mm' + '\n'\
        f'd3 = {d3/mm:4.1f} mm (225 mm)' + '\n'\
        f'd4 = {d4/mm:4.1f} mm (176 mm)'+ '\n'\
        f'd5 = {d5/mm:4.1f} mm (27 mm)' + '\n\n'\
        r'${\copyright}$ Fred van Goor, June 2020'
  
s2 =    f'f1 = {f1/mm:4.1f} mm' + '\n'\
        f'f2 = {f2/mm:4.1f} mm (160 mm)' + '\n'\
        f'f3 = {f3/mm:4.1f} mm' + '\n'\
        f'f4 = {f4/mm:4.1f} mm' + '\n'\
        f'f5 = {f5/mm:4.1f} mm' + '\n'\
        f'R1 = {R1/mm:4.1f} mm' + '\n'\
        f'R2 = {R2/mm:4.1f} mm' + '\n\n'

  
s3 =    r'Reference:' + '\n'\
        r'M.W. Beijersbergen, L. Allen, H.E.L.O. van der Veen and J.P. Woerdman,'+ '\n'+\
        r'Astigmatic laser mode converters and transfer of orbital angular momentum,' + '\n'\
        r'Optics Comm. 96 (1993) 123.'

fig=plt.figure(figsize=(11,6))
ax1 = fig.add_subplot(221);ax1.axis('off')
ax2 = fig.add_subplot(222);ax2.axis('off')
ax3 = fig.add_subplot(223);ax3.axis('off')
ax1.imshow(I0,cmap='jet');ax1.set_title(f'input intensity, HG$_{m_}$$_{n_}$')
ax2.imshow(I1,cmap='jet');ax2.set_title('output intensity')
ax3.text(0.0,0.0,s1);ax3.text(0.5,0.0,s2);ax3.text(1.0,0.0,s3)

plt.show()
