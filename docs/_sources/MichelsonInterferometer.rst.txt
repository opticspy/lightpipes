Michelson interferometer.
-------------------------

In a Michelson interferometer an incoming wave is split in two by a beamsplitter. The two beams are reflected by mirrors and united at the same beamsplitter, which generally results in interference. The interference pattern observed depends on the incoming beam, whether or not the mirrors are tilted and on the difference of the distances of the mirrors to the beamsplitter.
In this experiment we demonstrate a Michelson interferometer with unequal mirror distances and one of the mirrors tilted.

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

.. plot:: ./Examples/Interference/Michelson.py

You can modify the source Python script by, for example, insertion of a lens in one of the arms and remove the mirror tilt. The resulting interference pattern will be a set of concentric circles.

.. figure::  _static/MichelsonWithLens.png
    :align:   center

    *Interference pattern when a f=100cm lens is inserted in one of the arms and with the mirror tilt removed.*
    
Also the Michelson interferometer can be used to study the effect of phase aberrations. Place a phase aberrator, for example a Zernike aberration, in one of the arms.

.. figure::  _static/MichelsonWithAberration.png
    :align:   center
    
    *Interference pattern when aberration is inserted in one of the arms.*
