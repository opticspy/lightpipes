.. _Young:

.. Index::
    Two holes interferometer
    Young's interferometer
    BeamMix
    Fresnel
    CircAperture
    Begin
    Intensity

---------------------------
Two holes interferometer.
---------------------------

:download:`Download Python script <./examples/Young.py.txt>` [#f1]_

.. code-block:: python

    #Interference from two holes.
    try:
        import LightPipes
    except ImportError:
        print ("LightPipes not present")
        exit()
    import matplotlib.pyplot as plt
    m=1
    nm=1e-9*m
    um=1e-6*m
    mm=1e-3*m
    cm=1e-2*m
    try:
        LP=LightPipes.Init()
        wavelength=20*um
        size=30.0*mm
        N=1000
        LP.version()
        F=LP.Begin(size,wavelength,N)
        F1=LP.CircAperture(0.15*mm,  -0.6*mm,0, F)
        F2=LP.CircAperture(0.15*mm,  0.6*mm,0, F)    
        F=LP.BeamMix(F1,F2)
        F=LP.Fresnel(30.0*cm,F)
        I=LP.Intensity(2,F)
        plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
        plt.show()
    finally:
        del LightPipes
        
.. figure:: figures/Young.png
    :align:   center
    
    Intensity interference pattern at distance, z = 30 cm, from the two holes.

.. rubric:: Footnotes

.. [#f1] ´.txt´ has been added to the file name to avoid download problems. Remove ´.txt´ before running the script.
