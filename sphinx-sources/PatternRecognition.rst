Pattern recognition.
--------------------

In this example we demonstrate the recognition of objects using Fourier optics.
The light, originating from a collection of objects, is focused with a positive lens. A second lens is positioned with its primary focal point in the focus of
the first lens. When we place a screen behind the second lens at its secondary focus an inverted image of the collection of objects is projected on the
screen, as shown in figure 1. The object to be recognized is present once or several times in the collection. As objects we choose
transparencies with the characters A, B, and C.

.. figure:: ./Examples/FourierOptics/setup1.png

    *Fig. 1 Imaging a transparency with objects*
    
Each object will contribute to the phase distribution in the secondary focus of the first lens. If the fluctuations in the wavefront coming from one of the
objects is compensated by a phase plate prepared for that sort of object, see figure 2, placed in the focus, the beam coming from those objects will propagate as a
diverging spherical wave to the second lens and will be focused in a diffraction limited point on the screen. The position of that point will indicate the
presence and the position of the object. This will only be the case when the object, for which the phase plate was positioned in the focus, is actually present in the collection.

.. figure:: ./Examples/FourierOptics/setup2.png

    *Fig. 2 Making a phase mask of the Fourier transform of an object*
    

.. figure:: ./Examples/FourierOptics/setup3.png

    *Fig. 3 Placing the phase mask in the focus of the first lens.*

.. plot:: ./Examples/FourierOptics/PatternRecognition.py


*Fig. 4 Results of the pattern recognition simulation.*

