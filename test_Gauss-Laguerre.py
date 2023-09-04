#! /usr/bin/env python
"""
Test script: test GaussLaguerre(Fin, w0, p = 0, l = 0, A = 1.0, sincos = 1 )command.

    *Substitutes a Laguerre-Gauss mode (beam waist) in the field.*

        :math:`F_{p,l}(x,y,z=0) = A \\left(\\rho\\right)^{\\frac{|l|}{2} }L^p_l(\\rho)e^{-\\frac{\\rho}{2}}\\cos(l\\theta)`,
        
        with: :math:`\\rho=\\frac{2(x^2+y^2)}{w_0^2}`
        
        :math:`\\theta=atan(y/x)`
    
        if :math:`sincos = 0` replace :math:`cos(l\\theta)` by :math:`exp(-il\\theta)`
        
        if :math:`sincos = 2` replace :math:`cos(l\\theta)` by :math:`sin(l\\theta)`

    :param Fin: input field
    :type Fin: Field
    :param w0: Gaussian spot size parameter in the beam waist (1/e amplitude point)
    :type w0: int, float
    :param p: mode index (default = 0.0)
    :param l: mode index (default = 0.0)
    :type p: int, float
    :type l: int, float
    :param A: amplitude (default = 1.0)
    :type A: int, float
    :param sincos: 0 = exp, 1 = cos, 2 = sin (default = 1)
    :type sincos: int, float
    :return: output field (N x N square array of complex numbers).
    :rtype: `LightPipes.field.Field`
    :Example:

    >>> F = GaussLaguerre(F, 3*mm) # Fundamental Gauss mode, LG0,0 with a beam radius of 3 mm
    >>> F = GaussLaguerre(F, 3*mm, m=3) # Idem, LG3,0
    >>> F = GaussLaguerre(F, 3*mm, m=3, n=1, A=2.0) # Idem, LG3,1, amplitude 2.0
    >>> F = GaussLaguerre(F, 3*mm, 3, 1, 2.0) # Idem
    
    .. seealso::
    
        * :ref:`Examples: Laguerre Gauss modes.<Laguerre Gauss modes.>`
        
    Reference::
    
        A. Siegman, "Lasers", p. 642
"""

from LightPipes import *
import matplotlib.pyplot as plt

wavelength = 500*nm
size = 12*mm
N = 100
w0=1*mm
z=500*cm
p=0
l=10
A=1
ecs=0
F=Begin(size,wavelength,N)
F0=GaussLaguerre(F, w0, p, l, 2, ecs=ecs)
#Old style:
#F0=GaussLaguerre(p, l, A, w0, F)
I0=Intensity(F0,0)
F1=Forvard(F0,z)
I1=Intensity(F1)
Phi0=Phase(F0)
Phi1=Phase(F1)

s1 = "LightPipes for Python"
s2 =r'test_GaussLaguerre.py' + '\n\n'\
    f'p={p} l ={l}\n'\
    f'ecs={ecs}\n'\
    r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
    r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
    r'$N = {:4d}$'.format(N) + '\n'\
    r'$z = {:4.2f}$'.format(z/cm) + r' $cm$' + '\n'\
    r'$w_0 = {:4.2f}$'.format(w0/mm) + r' $mm$' + '\n'\
    r'beam power at source = ${:4.2f}$'.format(Power(F0)) + '\n'\
    r'output beam power at z = ${:4.2f}$'.format(Power(F1)) + '\n'\
    r'${\copyright}$ Fred van Goor, August 2023'

fig=plt.figure(figsize=(11,6))

fig.subplots_adjust(hspace=0.4)
ax1 = fig.add_subplot(231);ax1.set_title('intensity at z=0')#;ax1.axis('off')
ax2 = fig.add_subplot(232);ax2.set_title('intensity at z')#;ax2.axis('off')

ax3 = fig.add_subplot(233);ax3.axis('off')
ax4 = fig.add_subplot(234);ax4.set_title('phase at z=0') #;ax5.axis('off')
ax5 = fig.add_subplot(235);ax5.set_title('phase at z')#;ax4.axis('off')

ax1.imshow(I0,cmap='jet')
ax2.imshow(I1,cmap='jet')
ax3.text(0,1.0,s1, fontsize=15,va='top')
ax3.text(0,0.8,s2, va = 'top')
ax4.imshow(Phi0,cmap='jet')
ax5.imshow(Phi1,cmap='jet')

plt.show()
