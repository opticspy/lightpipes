=======
Support
=======

You can get help with LightPipes for Python in several ways:
Visit our Github_ site
               

Help for a specific `command` can be obtained at the Python prompt by typing:

.. code-block:: bash
            
    >>> help(LightPipes.Init.command)
            
For example, to display the help for the Begin command, type:

    >>> import LightPipes
    >>> LP=LightPipes.Init()
    >>> help(LP.Begin)

The response is:

.. code-block:: bash

    Help on built-in function Begin:

    Begin(...) method of LightPipes.Init instance
        F = Begin(GridSize, Wavelength, N)
            Creates a plane wave (phase = 0.0, amplitude = 1.0)

        Args::

            GridSize: size of the grid
            Wavelength: wavelength of the field
            N: N x N grid points (N must be even)

        Returns::

            F: N x N square array of complex numbers (1+0j).

        Example::

            >>> import LightPipes
            >>> LP = LightPipes.Init()
            >>> F = LP.Begin(0.03,500e-9,4)
            >>> print(F)
            [[(1+0j), (1+0j), (1+0j), (1+0j)],
             [(1+0j), (1+0j), (1+0j), (1+0j)],
             [(1+0j), (1+0j), (1+0j), (1+0j)],
             [(1+0j), (1+0j), (1+0j), (1+0j)]]

.. _Github: https://github.com/FredvanGoor/LightPipes-for-Python