.. Index::
    Doughnut laser mode
    Interference doughnut mode

Interference of a doughnut laser beam: tilted beams.
----------------------------------------------------

.. code:: python

    #! /usr/bin/env python
    """
        Doughnut_tilt.py
        
        Interference of a non-collinear zero order beam with a  Laguerre-Gauss
        doughnut beam.
        The interferometer could be a Michelson or a Mach Zehnder instrument.
        
        cc Fred van Goor, may 2020
    """
    from LightPipes import *
    import matplotlib.pyplot as plt
    if LPversion < "2.0.0":
        print(r'You need to upgrade LightPipes to run this script.' + '\n'+r'Type at a terminal prompt: $ pip install --upgrade LightPipes')
        exit(1)

    wavelength=632.8*nm #wavelength of HeNe laser
    size=10*mm # size of the grid
    N=300 # number (NxN) of grid pixels
    w0=3*mm # laser beam radius (in waist)
    z1=10*cm # length of arm 1
    z2=8*cm # length of arm 2
    tx=1.0*mrad # tilt of mirror 1

    F=Begin(size,wavelength,N)
    F1=GaussBeam(F,w0,doughnut=True,x_shift=-0.2*mm)
    Phi=Phase(F1)
    F2=GaussBeam(F,w0,tx=tx)
    F1=Forvard(z1,F1)
    F2=Forvard(z2,F2)
    F=BeamMix(F1,F2)
    I=Intensity(0,F)


    #initiate plots:
    fig, axs = plt.subplots(nrows=1, ncols=3,figsize=(11.0,5.0))
    #axs=_axs.flatten()
    s=r'Interference of a doughnut- and a tilted zero-order Gaussian beam.' +'\n'\
    r'Forked interference pattern (Michelson interferometer) due to helical phase of doughnut mode.'
    fig.suptitle(s)
    fig.subplots_adjust(hspace=0.5)

    s=r'Interference pattern'
    axs[0].imshow(I,cmap='jet'); axs[0].axis('off'); axs[0].set_title(s)
    s=r'Phase distribution'+ '\n' + r'of the doughnut beam.'
    axs[1].imshow(Phi,cmap='jet'); axs[1].axis('off'); axs[1].set_title(s)
    s = r'LightPipes for Python,' + '\n' + 'Doughnut-mode-interference-tilt.py' + '\n\n'\
        r'$\lambda = {:4.1f}$'.format(wavelength/nm) + r' $nm$' + '\n'\
        r'$size = {:4.2f}$'.format(size/mm) + r' $mm$' + '\n'\
        r'$N = {:4d}$'.format(N) + '\n'\
        r'$w_0 = {:4.2f}$'.format(w0/mm) + r' $mm$'+ '\n'\
        r'$z_1 = {:4.1f}$'.format(z1/cm) + r' $cm$' + '\n'\
        r'$z_2 = {:4.1f}$'.format(z2/cm) + r' $cm$' + '\n'\
        r'$t_x = ' + '{:4.2f}$'.format(tx/mrad) + r' $mrad$' + '\n'\
        r'${\copyright}$ Fred van Goor, May 2020'

    axs[2].text(-0.18,0.3,s)
    axs[2].axis('off')

    plt.show()

.. plot:: ./Examples/Interference/Doughnut_tilt.py
