.. _FocLens:

.. Index::
    Focus of a lens
    Steps
    Begin
    CircAperture
    Lens
    Intensity

---------------
Focus of a lens
---------------

:download:`Download Python script <./examples/FocLens.py.txt>` [#f1]_

.. code-block:: python

    #Focus of a lens.
    import LightPipes as lp
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    m=1
    nm=1e-9*m
    um=1e-6*m
    mm=1e-3*m
    cm=1e-2*m
    try:
        LP=lp.Init()
        LP.version()
        wavelength=632.8*nm;
        size=4*mm;
        N=100;
        N2=50;
        R=1.5*mm;
        dz=10*mm;
        f=50*cm;
        n=(1.0 + 0.1j)*np.ones((N,N))
        Icross=np.zeros((100,N))
        X=range(N)
        Z=range(100)
        X, Z=np.meshgrid(X,Z)
        F=LP.Begin(size,wavelength,N);
        F=LP.CircAperture(R,0,0,F);        
        F=LP.Lens(f,0,0,F);
        for i in range(0,100):
            F=LP.Steps(dz,1,n,F);
            I=LP.Intensity(0,F);
            Icross[i][:N]=I[N2][:N]
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot_surface(X, Z, Icross, rstride=1, cstride=1,
                        cmap='rainbow',
                        linewidth=0.0,
                        )
            plt.axis('off')
            plt.show()
    finally:
        del lp

.. figure::  figures\\FocLens.png
      :align:   center

      Focus of a lens.

.. rubric:: Footnotes

.. [#f1] ´.txt´ has been added to the file name to avoid download problems. Remove ´.txt´ before running the script.
