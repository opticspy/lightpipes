.. Index::
    Poisson spot
    Arago spot
    Bessel beam
    edge waves
    annular slit


From Poisson spot to a non-diffractive Bessel beam.
---------------------------------------------------

The waves originating from Huygens point-sources at the edge of the disk can be considered as a
collection of spherical waves which are all in phase because the disk is illuminated by a monochromatic plane wave.
Each spherical wave has the same amplitude as well. As a result these waves interfere constructively 
to a Poisson spot near the axis. It can be shown that the intensity distribution is approximately given by:

:math:`I(r,z) \approx I_0 J_0 ^2 ( \frac{2 \pi  \alpha r}{ \lambda } )`

with:

:math:`\alpha = \frac{a}{r}` is the angle of the wavefront near the axis, 
:math:`2a` is the diameter of the disk

The width of the beam is given by:

:math:`w(z)=\frac{2.44}{ \pi } \frac{ \lambda z}{a}`

and is proportional to the distance, z.

.. plot:: ./Examples/BesselBeam/BesselAnnularSlit1.py

.. toctree::
   :maxdepth: 1
   
   CollimatingEdgeWaves
   BesselBeamWithAnnularSlit
