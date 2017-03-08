=======
Support
=======

You can get help with LightPipes for Python in several ways:
Visit our Github_ site

.. _Github: https://github.com/opticspy/lightpipes

Help for a specific `command` can be obtained at the Python prompt and from the command reference.


For example, to display the help for the `Begin` command, type at the Pythom prompt:

    >>> from LightPipes import *
    >>> help(Begin)
    

The response is:

.. code-block:: bash

    Help on built-in function Begin:

    Begin(...) method of LightPipes._LightPipes.Init instance
    F = Begin(GridSize, Wavelength, N)
        Creates a plane wave (phase = 0.0, amplitude = 1.0)

    Args::

        GridSize: size of the grid
        Wavelength: wavelength of the field
        N: N x N grid points (N must be even)

    Returns::

        F: N x N square array of complex numbers (1+0j).

    Example:

    :ref:`Diffraction from a circular aperture <Diffraction>`

Example::

    >>> from LightPipes import *
    >>> F = Begin(0.03,500e-9,4)
    >>> print(F)
    [[(1+0j), (1+0j), (1+0j), (1+0j)],
    [(1+0j), (1+0j), (1+0j), (1+0j)],
    [(1+0j), (1+0j), (1+0j), (1+0j)],
    [(1+0j), (1+0j), (1+0j), (1+0j)]]


