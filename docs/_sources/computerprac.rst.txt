.. _computerprac:

Computer practical.
===================

.. _ComputerPracIntro:

.. Index::
     computer practical
     computer experiments

Introduction to computer practical.
***********************************

The computer optics laboratory offers a number of experiments that can be done on the computer using simulations of real optical problems. The computer lab is part of the `introduction to optics <https://www.utwente.nl/onderwijs/bachelor/opleidingen/technische-natuurkunde/studieprogramma/tweede-jaar/#module-6-golven-interferentie-en-waarschijnlijkheid>`_ (in Dutch!) course given during the second year `Applied Physics <https://www.utwente.nl/en/education/bachelor/programmes/applied-physics/>`_ (TN) Bachelor study of the faculty of Science and Technology (TNW) of the `University of Twente <http://www.utwente.nl/en/>`_.

.. image:: ./_static/UT_Logo_0072_Black_EN.png
    :align: center
    :target: http://www.utwente.nl/en/

Optics can be learned traditionally through theory by following lectures and in practice by performing experiments in the laboratory. With these simulations a third method is added: experiments on the student’s computer. Although the simulations are very realistic, computer experiments can never take the place of real experiments in the optics laboratory. Doing physics as opposed to thinking about doing physics should be done in the real laboratory where the student experiences real experimental problems that cannot be simulated even by the most advanced programs. The advantages of simulations are, however, that the student can do the experiment any time he wants in his own place. Also no costly laboratory equipment and stringent time schedules are needed.
With these simulations the student will learn many things about the topic’s theory and how the experiment can be performed in the real laboratory.

Each experiment has a number of exercises to be done and questions to be answered. The experiments are done by changing one or more parameters and by measuring characteristic data usually with the mouse. The student is asked to derive an expression for the parameter (wavelength, some radius, thickness, etc.) to be determined from the measurements. Each simulation will generate a random number, which will give the parameter to be measured. The formula relating this number to the parameter is very complicated and only known to the lecturer. The student must write this number on his report so he/she can easily check the answers.

The simulations make use of an optical toolbox (`LightPipes <http://www.okotech.com/>`_) with several commands for propagation, apertures, lenses, etc. The toolbox is written by Gleb Vdovin and is modified for this purpose by me. The toolbox is linked to each simulation program. It makes use of advanced propagation routines for solving the Fresnel-Kirchoff integral in two dimensions. The result is a very realistic optical simulation program for studying physical optics.

+------------------------------------------------+------------------------------------------------------+
|.. figure:: ./figures/FresnelSphericalSetup.png | .. figure:: ./figures/FresnelSphericalScreenShot.png |
+------------------------------------------------+------------------------------------------------------+

*Screenshot of one of the simulation programs (Fresnel diffraction with spherical wavefront as input).*

+--------------------------------------+---------------------------------------+
|.. figure:: ./figures/FresnelLab1.jpg | .. figure:: ./figures/FresnelLab2.jpg |
+--------------------------------------+---------------------------------------+

*Fresnel diffraction pattern as observed in the* `real optics lab <http://edu.tnw.utwente.nl/optprac/>`_

The Python script file of each experiment can be downloaded and executed if you properly prepared your Python installation including the installation of the necessary packages, see: :ref:`Prepare your computer.`
The experiments should be done in the order given by the :ref:`assignments<Assignments.>` and when possible repeated in the real laboratory.

Enjoy playing with optics!

Fred van Goor

.. _preparepc:

Prepare your computer.
**********************

To do the computer practical you have to prepare your computer. You must 
install Python and some other stuff before you can run the programs.

1. Go to the Python website, `http://www.python.org, <https://www.python.org/>`_ and Install Python on your computer. 
2. You will need the download tool `pip <https://pypi.python.org/pypi/pip>`_. It is already installed with 
   your Python installation, but you need to upgrade it.
   `Install and/or upgrade the download tool 'pip'. <https://pip.pypa.io/en/stable/>`_
3. Install the `matplotlib <http://www.matplotlib.org>`_ plot package. Open a terminal and type at the prompt:
   
   Windows: **pip install matplotlib**
   
   Linux and mac: **sudo pip install matplotlib**
4. Install the LightPipes for Python optical toolbox. Open a terminal and type at the prompt:
   
   Windows: **pip install LightPipes**
   
   Linux and mac: **sudo pip install LightPipes**
   
5. A nice and convenient environment to run and edit the Python scripts is `Geany <http://www.geany.org>`_.

.. _assignments:

Assignments.
************

.. toctree::
   :maxdepth: 1
   
   SphericalWavefront
   Reflect
   TwoHoles
   NewtonRings
   FabryPerot
   FresnelDiffraction

