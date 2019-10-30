Installation.
*************

This Python version of Lightpipes can be operated on Windows (32 and 64 bits), Linux (32 and 64 bits) and Macintosh (64 bits) computers.
There exist packages for Python versions 2.7, 3.4, 3.5, 3.6 and 3.7., there is a 3.7 Python version for the Raspberry Pi too (Tested on a RP4 model B with 4Gb memory).
LightPipes for Python is on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_ and can be installed if you have `pip <https://pip.pypa.io/en/stable/installing/>`_ installed on your computer.
In a terminal window simply type:

.. code-block:: bash

    pip install LightPipes

To test if the installation was successful start Python and type at the prompt:

    >>> from LightPipes import *
    >>> LPtest()
    LightPipes for Python: test passed.
    >>>
    
The response should be: "LightPipes for Python: test passed."

Most output from LightPipes python scripts should use the `MatPlotLib <https://matplotlib.org/>`_ plotting library.
MatplotLib can be installed by typing in a terminal:

.. code-block:: bash

    pip install matplotlib

Another useful package is `Tkinter <https://docs.python.org/3/library/tk.html>`_ to make graphical user interfaces (GUI). It is installed already with most Python installations.
See http://www.tkdocs.com/tutorial/install.html how to install it on your platform.

Finally, a convenient editor to make Python scripts is `Geany <http://www.geany.org/>`_.

Known installation problems.
============================

1) Too old version of numpy:
    After installation of LightPipes, using
    
    .. code-block:: bash
    
        sudo pip install LightPipes
    
    for a brandnew MacBook Air computer the following error popped-up after an import-test in python:
    
        >>> import LightPipes
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/Library/Python/2.7/site-packages/LightPipes/__init__.py", line 52, in <module>
        from ._LightPipes import * # noqa
        File "__init__.pxd", line 155, in init LightPipes._LightPipes (LightPipes/_LightPipes.cpp:10911)
        ValueError: numpy.dtype has the wrong size, try recompiling. Expected 88, got 96
    
    Solution:
    
    The version (1.8.0rc1) of the numpy package (installed as part of the macOS Sierra 10.12.6 update) is too old.
    You have to update numpy to the newest version. Use easy_install, not pip for this.
    
    .. code-block:: bash
    
        sudo easy_install -U numpy
    
    (If the cpp-compiler is not installed a window pops up to ask you to install it and the numpy installation is interrupted. Say yes to install the compiler and repeat the numpy installation)
