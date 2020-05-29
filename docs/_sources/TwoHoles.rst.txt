.. _TwoHoles:

.. Index::
    Computer practical
    Two holes interferometer
    Young's experiment

Two holes interferometer.
=========================

Download Python script: :download:`TwoHoles.py <./Examples/ComputerPrac/TwoHoles.py>`

.. figure:: ./figures/Young_Thomas_Lawrence.jpg

    *Thomas Young (Milverton, 1773 – London, 1829)*

When a screen with two small holes (or slits) is illuminated by a monochromatic beam 
of light an interference pattern can be observed on a screen some distance from the holes. 
This experiment is also called Young's experiment.

.. figure:: ./figures/twoholeslab.jpg
 
    *Fringes from a Young’s interferometer as observed in the lab. From left to right the distance between the CCD camera and the holes is increased. It can be seen that the two spherical waves emitted from the holes overlap and interfere better at larger distances.*

Two experiments can be performed:

Measurement of the wavelength.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ./figures/TwoHoles.png

    *Screenshot of the two holes experiment.*

Download Python script: :download:`TwoHoles.py <./Examples/ComputerPrac/TwoHoles.py>`

.. figure:: ./figures/twoholessetup.png

    *Young's experiment.*
    
    1.  Derive an expression that relates the distance between the fringes that can be observed 
        on the screen to the wavelength of the light illuminating the holes, 
        the distance to the observation screen, z, and the separation, d, of the two holes.
    2.  Measure the wavelength of the light beam. Vary the values of values of 
        d and z for this. Remember to choose values for d and z such that the theory is valid. 
        Use the cross-hair that becomes visible when the mouse is positioned above the 
        interference pattern. Estimate the experimental error you have to make 
        (the main source of experimental errors will be, in this case, the read out of the 
        mouse-position on the interference pattern.)

Measurement of the thickness of a thin film that covers one of the holes.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the second experiment a thin film is positioned in front of one of the holes. 
As depicted in the figure below the lower part of the incoming plane wave will travel 
along a longer optical path and will have a retarded phase compared to the upper part. 
As a consequence the theory of the Young’s interferometer must be modified taking into 
account the extra phase. With the film, maximum and minimum irradiance at the screen will 
now occur at different places and as a result the fringes are shifted. From the shift of 
the fringe pattern the film thickness can be determined if the refractive index of the 
film is known.

.. figure:: ./figures/twoholes_with_filmsetup.png

    *Young's experiment with thin film before one of the holes.*
    
    1.  A thin, transparent film with refractive index 1.5 can be positioned before one of the holes. 
        Modify the theory to take into account the extra phase shift caused by the film.
    2.  With this experiment you cannot determine the exact thickness of the film, 
        but you can find a discrete set of thicknesses the film can have. 
        Report the minimum thickness that this film can have.
    3.  What values of the thickness of the film are possible too?

Questions about Young's experiment.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    1.  What condition must be fulfilled for the distance, :math:`z`, to the screen, the wavelength 
        of the light, and the size of the holes for the theory that you used?
    2.  What happens to the fringes if the beam of light is not monochromatic but contains a 
        large number of wavelengths? How many fringes will be visible for white light?

You should be able to answer the following questions at the end of the course (Try to answer 
them now if you can!):

    3.  In relation with question 1: What type of diffraction are we talking about here?
    4.  What will happen with the fringes if the spatial coherency of the beam is poor? 
        (This means that there is no relation between the phases of the wavefront just before 
        the two holes)
    5.  Suppose that the coherent (laser) light is replaced by quasi monochromatic light 
        such as a line from a mercury lamp. How can you prepare this light such that you can observe fringes?
    6.  With the mercury lamp of the previous question, what will happen to the fringes if 
        the thin film before one of the holes is replaced by a thick glass plate?

`Literature: Pedrotti, 3rd ed., chapter 7-2. <https://www.amazon.com/Introduction-Optics-3rd-Frank-Pedrotti/dp/0131499335>`_
