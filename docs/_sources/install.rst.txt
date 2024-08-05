Installation.
*************

Current version = |release|

Up to version 1.2.0 the LightPipes for Python package, called LightPipes, 
consists of a collection of C++ routines which can be called from a Python script.
From version 2.0.0 we transformed the package into pure Python using the numpy, scipy and pyFFTW
packages. Because of these packages, the speed of the pure python version is about the same
as with the C++ version or even faster because use can be made of multi-processor operation.

All versions of Lightpipes can be operated on Windows (32 and 64 bits),
Linux (32 and 64 bits) and Macintosh (64 bits) computers.
The C++ versions < 2.0.0 packages are for Python versions 2.7, 3.4, 3.5, 3.6 and 3.7.
The pure Python versions will run on all (future) Python 3.+ versions.
It cannot be used with the retired Python 2.7 version. Upgrade to Python 3.

LightPipes for Python is on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_ 
and can be installed if you have `pip <https://pip.pypa.io/en/stable/installing/>`_ 
installed on your computer.
In a terminal window simply type the following commands:
(If you have both Python versions 2.7 and 3.+ installed on your computer use pip3 in stead of pip.)

.. code-block:: bash

    pip(3) install LightPipes
    
or:

.. code-block:: bash

    pip(3) install --upgrade LightPipes

to upgrade the package.
    


To test if the installation was successful start Python and type at the prompt:

    >>> from LightPipes import *
    >>> LPtest()
    LightPipes for Python: test passed.
    >>>
    
The response should be: "LightPipes for Python: test passed."

Most output from LightPipes python scripts should use the `MatPlotLib <https://matplotlib.org/>`_ plotting library.
MatplotLib can be installed by typing in a terminal:

.. code-block:: bash

    pip(3) install matplotlib

Another useful package is `Tkinter <https://docs.python.org/3/library/tk.html>`_ to make graphical user interfaces (GUI). It is installed already with most Python installations.
See http://www.tkdocs.com/tutorial/install.html how to install it on your platform.

Finally, a convenient editor to make Python scripts is `Geany <http://www.geany.org/>`_.

LightPipes  release notes.
==========================

**Version:** 2.1.5 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * ZernikeName2Noll

Bug fixes:
    * In zernikemath.py: line 41 -- 44 changed: _np.math.factorial(..) to: math.factorial(..)
    * In example PhaseRecovery.py: added lines: dta=list(np.float64(data)) and changed np.asfarray(data) to: np.asarray(data)

Fred van Goor, August 5, 2024.

----


**Version:** 2.1.4 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * LensFarfield

Bug fixes:
    * In __init__.py: line 212 changed: fig.canvas.set_window_title to: fig.canvas.manager.set_window_title
    * In user_func.py: line 115: changed: dtype=_np.object to: dtype=object
    * In Power command: core.py, line 892: added "\*Fin.dx\*\*2" to the result
    * In core.py: line 115: replaced 'Centroid' by 'D4Sigma'
    
    
Command changes:
    *  GaussLaguerre: added possibillity of sine, cosine or exponetial phase factor.

Fred van Goor, September, 4, 2023.

----

**Version:** 2.1.3 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * :func:`~LightPipes.AiryBeam1D`: substitudes a 1D Airy beam in the field.
    * :func:`~LightPipes.AiryBeam2D`: substitudes a 2D Airy beam in the field.

Bug fixes:
    * None
    
Command changes:
    *  None

Fred van Goor, May, 4, 2022.

----

**Version:** 2.1.2 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * None

Bug fixes:
    * fixed float to integer conversion errors. IndexErrors were raised in zernikemath.py

Command changes:
    *  Added option in Fresnel and Forvard commands to use the pyFFTW or the numpy Fast Fourier Transform package. Default is FFT in numpy. This allows the user to compare the two FFT methods.
    *  Added a config.py file. Here one can make the usage of pyFFTW permanent.
       Change "_USEPYFFTW = False" to "_USEPYFFTW = True" in that file.
       See: :ref:`using_pyFFTW` for more details.

In this version we also install the package matplotlib as a required installation.
Matplotlib is used in almost all LightPipes applications to present the results.

Fred van Goor, December, 18, 2021.

----

**Version:** 2.1.1 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_


New commands:
    * none

Bug fixes:
    * updated LPtest() command

Command changes:
    *  none

Fred van Goor, October, 7, 2021.

----

**Version:** 2.1.0 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * none

Bug fixes:
    * repaired some warning messages in core.py and zernike.py
    * when LightPipes is installed on an iPad with `pyto <https://pyto.readthedocs.io/en/latest/#>`_ 
      the warning message that the package pyFFTW is not installed has been removed.
      pyFFTW is not pure python and cannot be installed by a user on his iPad.
    * updated LPtest() command

Command changes:
    *  none

Fred van Goor, September, 9, 2021.

----

**Version:** 2.0.9 on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    * none

Bug fixes:
    * none

Command changes:
    *  :func:`~LightPipes.Begin`: type of the complex field array can be set to numpy.complex64 to save memory, thanks to leguyader, issue 62.

Fred van Goor, September, 9, 2021.

----

**Version 2.0.8** on `PyPi <https://pypi.python.org/pypi/LightPipes/>`_

New commands:
    *  :func:`~LightPipes.ABCD`: propagation of a pure Gaussian field using ABCD matrix.
    *  :func:`~LightPipes.GLens`: Lens filter for a pure Gaussian field using ABCD matrix.
    *  :func:`~LightPipes.GForvard`: Free space propagation of a pure Gaussian field using ABCD matrix.
    *  :func:`~LightPipes.Propagate`: Free space propagation of a field choosing the best propagation routine depending on Fresnel number (experimental)
    *  :func:`~LightPipes.Centroid`: returns the centroid coordinates of an intensity distribution.
    *  :func:`~LightPipes.D4sigma`: returns the beam width (:math:`D4\sigma`) of an intensity distribution.

Command changes:
    *  :func:`~LightPipes.Lens`: a check for Pure Gauss beam is performed so use can be made of analytical ABCD propagation if the input field is pure Gaussian, is in the grid-center and is not tilted.
    *  All commands set the "IsPureGauss" flag to False to allow ABCD propagation only when it is possible.

Bug fixes:
    *  A bug in :func:`~LightPipes.Steps` was fixed. Now scalar values of the refractive index can be passed as an argument.

Fred van Goor, March, 13, 2021.

----

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

2) Cannot install LightPipes (version 2.0.0 and higher) on a Raspberry Pi vs 4.0:
    This is caused by the fact that the required  pyFFTW package cannot be installed on a Raspberry Pi (ARM processor)
    Maybe this will be solved in the future.
    
    In the mean time you can install pyFFTW on a Raspberry Pi as follows:
 
    Step1, download FFTW:
    
    Download from the `FFTW Download page <http://www.fftw.org/download.html>`_ the file fftw-3.3.9.tar.gz or newer.
    At a terminal prompt goto your Downloads directory and type:
    
    .. code-block:: bash
    
        cd ~/Downloads
        tar xzf fftw-3.3.9.tar.gz
    
    Step 2, install FFTW:
    
    .. code-block:: bash
    
        cd fftw-3.3.9
        ./configure --enable-threads --enable-shared
        make
        sudo make install
    
    Step 3, install the cython compiler and ATLAS:
    
    .. code-block:: bash
    
        sudo pip3 install cython
        sudo apt-get install libatlas-base-dev
    
    If an error pops up that says something like: "E: Encountered a section with no package header" and/or:
    "E: The package lists or status file could not be parsed or opened", try:
    
    .. code-block:: bash
    
        sudo rm -vf /var/lib/apt/lists/*
        sudo apt-get update
    
    Step 4, install LightPipes for Python:
    
    .. code-block:: bash
    
        sudo pip(3) install lightpipes

    The installation of LightPipes for Python described above has been tested on a Raspberry Pi 4 model B with 8Gbyte memory and with NOOBS 3.5.0 operating system.
    
    It has also been tested with the recommended Raspberry Pi OS (32-bit) operating system installed using the Raspberry Pi Imager v1.4. See: `Raspberry Pi OS (previously called Raspbian) <https://www.raspberrypi.org/downloads/raspberry-pi-os/>`_
    
    With some examples (i.e. LaserModeTransformer.py) an error message popped-up:
    
    "Type Error: Couldn't find foreign struct converter for 'cairo.Context'

    This could be solved by typing:
    
    .. code-block:: bash
    
        sudo apt install python3-gi-cairo
    
    As an alternative you can install the C++ version 1.2.0 of LightPipes when Python 3.7 is installed on the Raspberry Pi.
    Type at a terminal prompt:
    
    .. code-block:: bash
    
        sudo pip(3) install LightPipes==1.2.0
        
.. _using_pyFFTW:
 
Using LightPipes with the pyFFTW package.
=========================================

    Using the pyFFTW package we found that LightPipes propagation routines are faster.
    However, we experienced that with a new Python version it takes a while before new binaries of pyFFTW are available. 
    Because of that we decided from LightPipes version 2.0.7. to skip pyFFTW from the list of required packages and let it be an option. 
    As a consequence the FFT calculations are performed by the FFT of numpy which is slightly slower than pyFFTW.
    For reasonable small grid sizes (less than 1000 x 1000 gridpoints) you will not notice that.
    When pyFFTW becomes available you can install pyFFTW and from that moment pyFFTW can be used and the propagation will be faster.
    See the :func:`~LightPipes.Fresnel` and :func:`~LightPipes.Forvard` commands how to use pyFFTW.
    So for normal installation do:
    
    .. code-block:: bash
    
        sudo pip(3) install LightPipes


    To install pyFFTW do:
    
    .. code-block:: bash
    
        sudo pip(3) install pyFFTW
        
    To install LightPipes with pyFFTW do:
    
    .. code-block:: bash
    
        sudo pip(3) install LightPipes[pyfftw]
        
    If pyFFTW is not installed, LightPipes will fall back to numpy FFT which is slightly slower than pyFFTW.
    A user can force the propagation routines :func:`~LightPipes.Fresnel` and :func:`~LightPipes.Forvard` to use pyFFTW or numpy FFT.
    If pyFFTW is not installed a warning message will be shown and LightPipes falls back to numpy FFT.
    The warning can be suppressed by editing the file config.py in your local python site-packages directory:

    1) Find your python installation directory:
       For windows:
    
        .. code-block:: bash
    
          where python
        
        For Mac or Linux:
        
        .. code-block:: bash
    
          which python
        
    2) You will find config.py in:
    
        .. code-block:: bash
        
          .....\Python3x\Lib\site-packages\LightPipes (windows)
          ...../Python3x/Lib/site-packages/LightPipes (Linux, Mac)
          
          
    3) Open config.py in an editor and change:
    
        .. code-block:: bash
        
          _USE_PYFFTW = False
          
       to:
        
        .. code-block:: bash
        
          _USE_PYFFTW = True       
        
    4) After saving config.py LightPipes always uses pyFFTW, 
    even if you ommit the usepyFFTW = True option in the :func:`~LightPipes.Fresnel` and :func:`~LightPipes.Forvard` commands.
