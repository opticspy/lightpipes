.. _Fresneldiffraction:

.. Index::
    Computer practical
    Fresnel diffraction
    Fresnel zones
    Fresnel
    Forvard
    CircAperture
    Begin
    Intensity

Fresnel diffraction.
====================

Download Python script: :download:`FresnelPlane.py <./Examples/ComputerPrac/FresnelPlane.py>`

.. figure:: ./figures/Augustin_Fresnel.jpg

    *Auguste Fresnel, (Broglie, 1788 – Ville-d'Avray, 1827)*

Suppose that a monochromatic beam of light falls on a screen with a round
hole in it. At a certain distance from the hole a diffraction pattern
can be observed on a second screen. The structure of the pattern depends
on the wavelength, :math:`λ`, and the phase distribution of the incoming wavefront
and also on the diameter, :math:`d`, of the hole and the distance, :math:`z`, from
the hole to the screen.

Here we study the case that :math:`\frac{A}{\lambda}` is larger than the distance to
the screen: :math:`\frac{A}{\lambda}>z`, where :math:`A=\frac{\pi}{4}d^2` is the area of the hole.
In this so-called near field- or Fresnel diffraction regime a monochromatic plane or spherical wave 
that illuminates the hole will produce a diffraction pattern in the form of a set of concentric rings. 
The irradiance at the optical axis will be a minimum or a maximum when, at constant wavelength and hole 
diameter, the distance from the hole to the observation screen is reduced from inifinity to zero.

The rings appear after passing the critical distance
(also called the Rayleigh length) :math:`z_R =\frac{A}{\lambda}`.
If :math:`z > z_R` no rings but a smooth irradiance distribution in the form
of a squared Bessel function is observed of which the shape
(but not the beam diameter) remains constant while increasing z.
This far-field is also called Fraunhofer diffraction (Pedrotti chapter 11).

Whether a maximum or a minimum appears on the optical axis can be
understood using the Fresnel zone theory (Pedrotti, 13-4).
If the number of half-lambda zones ‘seen’ by the observer is odd a
maximum is observed, an even number of zones produces a minimum irradiance.
The number of Fresnel zones is indicated by the Fresnel number, :math:`N_F=\frac{z_R}{z}`.

In these experiments the distances where a maximum or minimum intensity
on the optical axis appear are measured. From these measurements the
wavelength of the light can be determined if the hole diameter is known.

+--------------------------------------+--------------------------------------+
|.. figure:: ./figures/FresnelLab1.jpg |.. figure:: ./figures/FresnelLab2.jpg |
+--------------------------------------+--------------------------------------+

    *The experimental set-up in the lab is simple:
    it consists of a (HeNe) laser, a beam expander or a strong lens to
    produce a plane or a spherical wave, a screen with the hole
    and a CCD camera. All the components are mounted on an optical
    rail to adjust and measure distances easily.*

In this exercise two incoming wavefronts are considered: a plane wave
and a spherical wave.

Fresnel diffraction, plane wavefront.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ./figures/FresnelPlaneSetup.png

    *Setup of the Fresnel diffraction experiment. A plane wave enters a round hole in a screen.*

.. figure:: ./figures/FresnelPlaneScreenShot.png
    
   *Screenshot of the Fresnel diffraction experiment with a plane input wave.*

Download Python script: :download:`FresnelPlane.py <./Examples/ComputerPrac/FresnelPlane.py>`

    1. Show that at the optical axis maximum and minimum irradiances are observed for distances :math:`z_m` if:
    
        .. math::
       
            \frac{1}{z_m}=\frac{4\lambda}{d^2}m
       
       minima for: :math:`m = even = 2, 4, 6, …`
       
       maxima for: :math:`m= odd = 1, 3, 5, …`
    2. Measure these positions for a number of values of the diameter, :math:`d`, of the hole.
    3. Determine the value of the wavelength of the light from the measurements.

.. _FresnelSpherical:

Fresnel diffraction, spherical wavefront.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ./figures/FresnelSphericalSetup.png

    *Setup of the Fresnel diffraction experiment. A spherical wave from a point source enters a round hole in a screen.*

.. figure:: ./figures/FresnelSphericalScreenShot.png

    *Screenshot of the Fresnel diffraction experiment with a spherical input wave.*
    
Download source code: :download:`FresnelSpherical.py <./Examples/ComputerPrac/FresnelSpherical.py>`

    1. Modify the equations for the positions of maximum and minimum
       irradiance on the optical axis behind the screen with the hole
       for the spherical wave and show that in this case these distances
       are given by:
       
        .. math::
       
            \frac{1}{z_1} + \frac{1}{z_{2m}}=\frac{4\lambda}{d^2}m
       
       minima for: :math:`m = even = 2, 4, 6, …`
       
       maxima for: :math:`m= odd = 1, 3, 5, …`
    2. Measure these positions for a number of values of the diameter, :math:`d`, of the hole and for the position, :math:`z_1`, of the point source.
    3. Determine the value of the wavelength of the light from the measurements.

Questions about Fresnel diffraction.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    1. What happens if the beam of light is not monochromatic but contains
       a large number of wavelengths?
    2. Look at the formula(s) you derived to explain the observations.
       Can you talk about some sort of imaging? Define an expression for 
       a 'focal length'. Hint: have a look at the pinhole  camera (Pedrotti 3-4).
    3. Find out what is meant with the "Fresnel Number".
       What is the irradiance on the optical axis when this number is odd and when it is even?
    4. Can you consider a diffraction pattern as an interference phenomenon? Why?

`Literature: Pedrotti, 3rd ed., chapter 13. <https://www.amazon.com/Introduction-Optics-3rd-Frank-Pedrotti/dp/0131499335>`_
