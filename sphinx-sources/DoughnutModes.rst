.. Index::
    Laguerre Gauss modes
    Doughnut mode
    Laser


Laguerre doughnut modes.
------------------------

.. code:: python

    #! /usr/bin/env python
    """
    GaussLaguerre_doughnut.py
        
        Calculates the intensity- and phase distributions of
        Laguerre-Gauss doughnut laser modes.
        
        cc Fred van Goor, May 2020.
    """
    from LightPipes import *
    import matplotlib.pyplot as plt
    if LPversion < "2.0.0":
        print(r'You need to upgrade LightPipes to run this script.' + '\n'+r'Type at a terminal prompt: $ pip install --upgrade LightPipes')
        exit(1)

    wavelength = 500*nm
    size = 15*mm
    N = 200
    w0=3*mm
    i=0

    m_max=6
    fig, axs = plt.subplots(nrows=2, ncols=m_max,figsize=(11.0,5.0))
    s=r'Doughnut laser modes'
    fig.suptitle(s)
    F=Begin(size,wavelength,N)
    n=0
    for m in range(1,m_max+1):
        F=GaussBeam(F, w0, doughnut=True, n=n, m=m)
        I=Intensity(0,F)
        Phi=Phase(F)
        s=f'$LG_{n}$' + f'$_{m}$' + '$_*$'
        axs[0][m-1].imshow(I,cmap='jet'); axs[0][m-1].axis('off'); axs[0][m-1].set_title(s)
        axs[1][m-1].imshow(Phi,cmap='rainbow'); axs[1][m-1].axis('off');
    plt.show()

.. plot:: ./Examples/Laser/GaussLaguerre_doughnut.py


