Laser simulation, stable laser resonator.
-----------------------------------------

A typical laser consists of two (concave or convex) mirrors separated some distance and a gain medium mostly based on
stimulated emission. One (or both) of the mirrors is partly transmissive and when the 
mirrors are well aligned and the losses are below some maximum the radiation field inside the 
resonator will grow starting from noise by spontaneous emission as a function of the number of round trips. The laser intensity will be structured in 
a number of resonator modes depending on the wavelength, the curvatures of and the distance between the mirrors 
and especially the diameter of an intra-cavity aperture.

.. figure:: ./_static/stab_laser.png

   Laser resonator with gain.



In the python script below a number of parameters can be adjusted which allows the study of several 
important features of a laser. In the movie we show Q-switching to generate short high intensity pulses 
by changing the reflectivity of the outcoupling mirror, operation on high-order transversal modes by opening 
the aperture, changing the resonator g-parameters to study the stability criterion, 
injection of a high-order Gauss-Hermite mode and the effect of thin wires inside the resonator.

.. raw:: html

    <iframe width="560" height="315" src="_static/laser.m4v" frameborder="0" allowfullscreen></iframe>

:download:`(Download source code) <./Examples/Laser/laser_simulation.py>`

.. .. literalinclude:: ../Examples/Laser/laser_simulation.py
..     :caption: laser_simulation.py
..     :name: laser-simulation


