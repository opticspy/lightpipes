.. _InternalReflection:

.. Index::
    Computer practical
    Internal reflection
    Snell's law

Internal reflection and refraction.
===================================

Download Python script: :download:`ReflectRefract.py <./Examples/ComputerPrac/ReflectRefract.py>`

.. figure:: ./figures/Willebrord_Snell.jpg

    *Willebrord Snel van Royen (Leiden, 1580 – 1626), better known as Snellius*



In this experiment we study internal reflection and refraction from the interface between a transparent medium and air.

.. figure:: ./figures/ReflectSetup.png

    *Setup of the reflection / refraction experiment.*
    
**Total internal reflection.**

According to Snell’s law the refraction angle increases when the angle of incidence increases. 
In case the refractive index of the medium is larger than that of the surrounding air, 
there will be an angle of incidence for which the refraction angle reaches its maximum value 
(i.e. :math:`φ_{tran} = 90°`). This angle of incidence is called the critical angle. 
For angles of incidence larger than the critical angle total internal reflection occurs.

**Brewster angle or polarizing angle.**

When a beam of light is reflected from a surface the reflected irradiance depends 
on both the angle of incidence and the direction of the electric field vector of the incident beam. 
It is common to refer to the component of the electric field vector perpendicular 
to the plane of incidence, :math:`E_s` ( s-polarized light or TE-mode, s = ‘senkrecht’ in German) 
and the component in the plane of incidence, :math:`E_p` (p-polarized light or TM-mode, p = ‘parallel’). 
It can be shown that for a particular angle of incidence the :math:`E_p` component is entirely missing 
from the reflected beam. This angle is called the Brewster or polarizing angle. 
The effect occurs for both internal as external reflection.

Both the irradiances from reflection and transmission can be measured with screen 1 and 2 
respectively (CCD cameras). The beam from the HeNe laser is linearly polarized. 
The polarization (or plane of vibration of the electric field) can be adjusted  \
using a 1/4 wave plate and a polarizer. 
The medium has the shape of a half cylinder so that the incident beam is always perpendicular 
to the air-medium interface. With this experiment the refractive index of the medium can be determined. 
Reflections from the cylinder surface can be neglected.

.. figure:: ./figures/ReflectScreenShot.png

    *Screenshot of the reflection - refraction experiment.*

Measurement of the refractive index of the medium.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download Python script: :download:`ReflectRefract.py <./Examples/ComputerPrac/ReflectRefract.py>`

    1.  Derive an expression that yields the refractive index from the measurable quantities.
    2.  Determine the refractive index of the medium.
    3.  For one particular angle of incidence and polarization it is possible to reduce the 
        reflected irradiance to zero. Calculate this angle from the measured index and verify 
        it with an experiment. The polarization is defined as the angle of the plane of 
        vibration of the electric field vector with respect to the plane of incidence.

Questions.
^^^^^^^^^^

    1.  How is the angle of incidence called where no reflection takes place? 
        Give one important application of a window that is positioned at this angle.
        Which component of the reflected beam is missing at this angle?
    2.  Prove that the sum of these angles at internal and external reflection respectively is exactly :math:`90°`.
        A dielectric surface positioned at proper angle of incidence can be used as a polarizer 
        to produce linear polarized light from an un-polarized input beam. 
        Why is such a polarizer seldom used in practice in spite of the fact that the 
        set-up is very cheap and simple compared to other polarizers?

`Literature: Pedrotti, 3rd ed., chapter 2 and chapter 15-2. <https://www.amazon.com/Introduction-Optics-3rd-Frank-Pedrotti/dp/0131499335>`_
