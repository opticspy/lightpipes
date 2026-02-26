.. index::
   Poisson spot
   Arago spot
   Diffraction
   Fresnel
   CircScreen
   Begin
   Intensity

Poisson’s Spot
--------------

Poisson’s spot, also known as the Arago spot, is a classical demonstration of the
wave nature of light. When a coherent beam illuminates an opaque circular disk,
a bright point appears at the center of the geometric shadow. This phenomenon
results from constructive interference of the secondary wavelets originating
from the edge of the disk.

Historically, Poisson predicted the existence of this bright spot while
evaluating Fresnel’s wave theory of light. He believed the prediction was absurd
and used it as an argument *against* the wave theory. However, Arago performed
the experiment and observed the spot exactly as predicted. The Poisson/Arago
spot therefore became one of the earliest and strongest confirmations that light
behaves as a wave.

This example demonstrates how to simulate Poisson’s spot using LightPipes.

What this example illustrates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Creation of a uniform plane wave.
- Introduction of an opaque circular obstacle.
- Fresnel propagation over a finite distance.
- Calculation and visualization of the resulting intensity pattern.
- Observation of the central bright spot characteristic of Poisson’s phenomenon.

Physical background
^^^^^^^^^^^^^^^^^^^

According to geometrical optics, the center of the shadow behind an opaque disk
should be completely dark. Fresnel’s wave theory, however, predicts that every
point on the edge of the disk acts as a secondary source. The contributions from
these sources interfere constructively at the center of the shadow, producing a
bright spot. The surrounding ring structure is caused by additional constructive
and destructive interference of the diffracted wavefronts.

Code example
^^^^^^^^^^^^

.. code-block:: python
   :linenos:

    import numpy as np
    from LightPipes import *
    import matplotlib.pyplot as plt

    # Parameters
    wavelength=5*um
    size=25.0*mm
    N=2000
    N2=int(N/2)
    z=20*cm

    # Begin with a plane wave
    F = Begin(size, wavelength, N)

    # Gaussian laser beam
    w0=size/3
    F=GaussBeam(F, w0)

    # Circular opaque disk (obstacle)
    disk_diameter = 6.0 * mm
    F = CircScreen(F,disk_diameter/2)

    # Fresnel propagation
    F = Fresnel(F, z)

    # Intensity at the screen
    I = Intensity(0, F)

    # Coordinates for plotting
    x = np.linspace(-size/2, size/2, N) / mm

    s1 =    r'LightPipes for Python' + '\n'
    s2 =    r'Poisson.py'+ '\n\n'\
            f'size = {size/mm:4.2f} mm' + '\n'\
            f'$\\lambda$ = {wavelength/um:4.2f} $\\mu$m' + '\n'\
            f'N = {N:d}' + '\n' +\
            f'd = {disk_diameter/mm:4.2f} mm disk diameter' + '\n'\
            f'w0 = {w0/mm:4.2f} mm radius Gauss beam' + '\n'\
            f'z = {z/cm:4.2f} cm distance from disk' + '\n'\
            r'${\copyright}$ Fred van Goor, February 2026'


    fig=plt.figure(figsize=(11,6))
    fig.suptitle("The spot of Poisson")
    ax1 = fig.add_subplot(221);ax1.axis('off')
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223);ax3.axis('off')
    ax1.set_xlim(N2-300,N2+300)
    ax1.set_ylim(N2-300,N2+300)
    ax1.imshow(I,cmap='jet')

    ax1.set_title(f'Intensity pattern after {z/cm:4.1f} cm propagation')
    X=np.linspace(-size/2,size/2,N)
    ax2.plot(X/mm,I[N2]); ax2.set_xlabel('x[mm]'); ax2.set_ylabel('Intensity [a.u.]')
    ax2.set_xlim(-1,1); ax2.set_title('The intensity cross-section of the spot')
    ax3.text(0.0,1.0,s1,fontsize=12, fontweight='bold')
    ax3.text(0.0,0.3,s2)
    plt.show()



Expected result
^^^^^^^^^^^^^^^

At a propagation distance of approximately one meter, the intensity pattern shows:

- A bright central spot located exactly at the center of the shadow.
- Concentric diffraction rings surrounding the spot.
- A shadow region whose structure depends on the disk radius, wavelength, and
  propagation distance.

At shorter distances the shadow is more pronounced, while at longer distances
the Poisson spot becomes sharper and more clearly visible.

.. plot:: ./Examples/Diffraction/Poisson.py
