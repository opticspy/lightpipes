.. _Michelson:

.. Index::
    Michelson
    interferometer
    GaussHermite
    Lens
    IntAttenuator
    Tilt
    BeamMix
    Forvard
    Begin
    Intensity

----------------
Michelson interferometer.
----------------

:download:`Download Python script <./examples/Michelson.py.txt>` [#f1]_

.. code-block:: python

    #Michelson interferometer
    #! /usr/bin/env python
    try:
        import LightPipes
    except ImportError:
        print "LightPipes not present"
    exit()

    import matplotlib.pyplot as plt
    m=1
    nm=1e-9*m
    um=1e-6*m
    mm=1e-3*m
    cm=1e-2*m
    rad=1
    mrad=1e-3*rad
    
    LP=LightPipes.Init()
    
    wavelength=632.8*nm #wavelength of HeNe laser
    size=10*mm # size of the grid
    N=300 # number (NxN) of grid pixels
    R=3*mm # laser beam radius
    z1=8*cm # length of arm 1
    z2=7*cm # length of arm 2
    z3=3*cm # distance laser to beamsplitter
    z4=5*cm # distance beamsplitter to screen
    Rbs=0.5 # reflection beam splitter
    ty=1*mrad; tx=0.0*mrad # tilt of mirror 1
    f=50*cm # focal length of positive lens
    
    #Generate a weak converging laser beam using a weak positive lens:
    F=LP.Begin(size,wavelength,N)
    F=LP.GaussHermite(0,0,1,R,F)
    F=LP.Lens(f,0,0,F)
    
    #Propagate to the beamsplitter:
    F=LP.Forvard(z3,F)
    #Split the beam and propagate to mirror #2:
    F2=LP.IntAttenuator(1-Rbs,F)
    F2=LP.Forvard(z2,F2)
    
    #Introduce tilt and propagate back to the beamsplitter:
    F2=LP.Tilt(tx,ty,F2)
    F2=LP.Forvard(z2,F2)
    F2=LP.IntAttenuator(Rbs,F2)
    
    #Split off the second beam and propagate to- and back from the mirror #1:
    F10=LP.IntAttenuator(Rbs,F)
    F1=LP.Forvard(z1*2,F10)
    F1=LP.IntAttenuator(1-Rbs,F1)
    
    #Recombine the two beams and propagate to the screen:
    F=LP.BeamMix(F1,F2)
    F=LP.Forvard(z4,F)
    I=LP.Intensity(1,F)
    plt.imshow(I); plt.axis('off');plt.title('intensity pattern')
    plt.show()
    
    Intensity pattern.

.. rubric:: Footnotes

.. [#f1] ´.txt´ has been added to the file name to avoid download problems. Remove ´.txt´ before running the script.
