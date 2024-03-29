import numpy as np
from LightPipes import *
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
 
'''
Generation of an Airy beam.
===========================
LightPipes for Python, Fred van Goor, 11-1-2022

A non-diffracting Airy beam can be generated by substituting a cubic phase distribution
in a laser beam. After a 2D Fourier transform with a positive lens the 
Airy beam will exist.
With the parameters below, the Airy beam exists from z = 0 cm to z= 30 cm.
Ref: 
G.A. Siviloglou, J. Broky, A. Dogariu and D.N. Christodoulides, PRL 99,213901(2007)
T. Latychevskaia, D. Schachtler, and H.W. Fink, Applied Optics Vol. 55, Issue 22, pp. 6095-6101 (2016)
'''

wavelength = 650*nm #wavelength 
N=624
size=N*32.0*um
dN1=N//2-40
dN2=N//2+40
beta=117/m #
w0=10*mm #beam waist laser
f=80*cm #focal length of Fourier lens
k=2*np.pi/wavelength

#Generate input beam
F0=Begin(size,wavelength,N)
F0=GaussHermite(F0,w0)

#Cubic Phase Plate (CPP):
X,Y = F0.mgrid_cartesian
c = 2 * np.pi * beta
c3 = (c**3)/3
CPP=c3*(X**3 + Y**3) + np.pi
F0=SubPhase(F0,CPP)
phase=Phase(F0)

#initiate figure 1:
fig1, axs1 = plt.subplots(nrows=3, ncols=1,figsize=(5.0,6.0))
figure1 = mpimg.imread('figure1.jpg')
imagebox = OffsetImage(figure1, zoom=0.15)
ab = AnnotationBbox(imagebox, (0.4, 0.6),frameon=False)
s1=r'Generation of an Airy beam.'+'\n\n'
s2=r'References:'+ '\n'\
   r'(1) G.A. Siviloglou, J. Broky, A. Dogariu and D.N. Christodoulides, Phys. Rev. Lett, 99,213901(2007)'+'\n'\
   r'(2) T. Latychevskaia, D. Schachtler, and H.W. Fink, Appl. Optics, 55, 6095-6101(2016)'+'\n\n'
s3 = r'LightPipes for Python,' + '\n' + 'AiryBeam.py' + '\n\n'\
    r'Parameters from ref 2:' + '\n'\
    r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$w_0 = {:4.2f}$'.format(w0/mm) + r' $mm$'+ '\n'\
    r'$f = {:4.2f}$'.format(f/cm) + r' $cm$'+ '\n'\
    r'$\beta = {:4.2f}$'.format(beta/m) + r' $m^{-1}$'+ '\n'\
    r'${\copyright}$ Fred van Goor, January 2022'+ '\n'
axs1[0].text(0.,1.3,s1,fontsize=15, verticalalignment='top')
axs1[0].text(0.,1.0,s2+s3,fontsize=5, verticalalignment='top');axs1[0].axis('off')
axs1[1].add_artist(ab);axs1[1].axis('off')
axs1[1].text(0.0,1.1,'figure  1 from reference 2',fontsize=5, verticalalignment='top')
s=r'Phase distribution SLM'
axs1[2].imshow(phase,cmap='gray'); axs1[2].axis('off'); axs1[2].set_title(s)

#Fourier transform lens:
F0=Lens(F0,f)

#Propagate a distance f:
F0=Fresnel(F0,f)

def AiryBeam(z):
	'''
	Propagates the Airy beam a distance z from the focal point..
	returns a tuple:
	Position of the maximum intensity,
	The intensity distribution at a distance z,
	The peak intensity of the Airy beam at z.
	'''
	F=Fresnel(F0,z)
	I=Intensity(F)
	#Find the coordinates of the maximum intensity:
	result = np.where(I == np.amax(I))
	Coordinates = list(zip(result[0], result[1]))
	for Coord in Coordinates:
		Xmax=X[Coord[0],Coord[1]]; Ymax=Y[Coord[0],Coord[1]]
		print(Xmax/mm,Ymax/mm) #Xmax should be equal to Ymax   
	return Xmax,Ymax,I,I[result][0]

def xmax(z):
	'''
	Returns:
	The theoretical deflection at z,
	The peak intensity of the Airy beam at a distance z,
	according to Latychevskaia et al.
	'''
	c=z*f/(f+z)
	zdivc=(f+z)/f
	xmax=(1.0188*(beta*wavelength*f)-c**2/(4*k**2*(beta*wavelength*f)**3))*zdivc
	return xmax, (f/(f+z))**2

zstart=0*cm
zend=31*cm
z=np.arange(zstart,zend,1*cm)
n=z.shape[0]
deflection=np.zeros(n)
Imax=np.zeros(n)

#initiate figure 2:
fig2, axs2 = plt.subplots(nrows=4, ncols=2,figsize=(6.0,6.0))
fig2.suptitle('simulation with data Latychevskaia et al.')
fig2.subplots_adjust(hspace=0.8)
for i in range(0,n):
	Xmax,Ymax,I,_Imax=AiryBeam(z[i])

	if z[i] == 0*cm:
		axs2[0,0].imshow(I,cmap='jet')
		s=r'$z = {:2.1f}$'.format(z[i]/cm) + r'$cm$'
		axs2[0,0].imshow(I,cmap='jet'); axs2[0,0].axis('off'); axs2[0,0].set_title(s)
		axs2[0,0].set_xlim(dN1,dN2)
		axs2[0,0].set_ylim(dN2,dN1)

	if z[i]== 10*cm:
		s=r'$z = {:2.1f}$'.format(z[i]/cm) + r'$cm$'
		axs2[1,0].imshow(I,cmap='jet'); axs2[1,0].axis('off'); axs2[1,0].set_title(s)
		axs2[1,0].set_xlim(dN1,dN2)
		axs2[1,0].set_ylim(dN2,dN1)

	if z[i]== 20*cm:
		s=r'$z = {:2.1f}$'.format(z[i]/cm) + r'$cm$'
		axs2[2,0].imshow(I,cmap='jet'); axs2[2,0].axis('off'); axs2[2,0].set_title(s)
		axs2[2,0].set_xlim(dN1,dN2)
		axs2[2,0].set_ylim(dN2,dN1)

	if z[i]== 30*cm:
		s=r'$z = {:2.1f}$'.format(z[i]/cm) + r'$cm$'
		axs2[3,0].imshow(I,cmap='jet'); axs2[3,0].axis('off'); axs2[3,0].set_title(s)
		axs2[3,0].set_xlim(dN1,dN2)
		axs2[3,0].set_ylim(dN2,dN1)

	deflection[i]=Xmax
	Imax[i]=_Imax

gs = axs2[0,1].get_gridspec()
for ax in axs2[0:,-1]:
	ax.remove()
ax1=fig2.add_subplot(gs[0:2,1])
ax1.plot(z/cm,-deflection/mm,'ro',z/cm,-xmax(z)[0]/mm)
ax1.set_xlabel('z/cm'); ax1.set_ylabel('deflection/mm')
ax1.legend(('simulated with LightPipes for Python', 'theory ref 2'),
           shadow=True, loc=(0.1, 0.8), handlelength=1.5, fontsize=5)
           
ax2=fig2.add_subplot(gs[2:,1])           
ax2.plot(z/cm,Imax/Imax[0],'ro',z/cm,xmax(z)[1])
ax2.set_xlabel('z/cm'); ax2.set_ylabel('Peak intensity')

#Experimental data from ref 2, figure 2f:
#In pixels, as good as possible....
X_Exp=np.array([122,151,184,213,245,276,308,336,366,397,429,458,491,520,551,582])
Y_Exp=np.array([106,139,177,216,198,207,247,266,289,327,336,354,350,360,360,366])
Imax_Exp=1.0-1.0/(428-106)*(Y_Exp-106)
z_Exp=30*cm/(582-122)*(X_Exp-122)
ax2.plot(z_Exp/cm,Imax_Exp,'+')
ax2.legend(('simulated with LightPipes for Python', 'theory ref 2', 'experiment ref 2'),
           shadow=True, loc=(0.25, 0.8), handlelength=1.5, fontsize=5)

plt.show()
