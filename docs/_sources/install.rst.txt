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

    pip install matplotlib

Another useful package is `Tkinter <https://docs.python.org/3/library/tk.html>`_ to make graphical user interfaces (GUI). It is installed already with most Python installations.
See http://www.tkdocs.com/tutorial/install.html how to install it on your platform.

Finally, a convenient editor to make Python scripts is `Geany <http://www.geany.org/>`_.

LightPipes  release notes.
==========================

**Version:** |release| (under development)

New commands:
    * none

Bug fixes:
    * none

Command changes:
    *  :func:`~LightPipes.Begin`: type of the complex field array can be set to numpy.complex64 to save memory, thanks to leguyader, issue 62.

Fred van Goor, March, 27, 2021.

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

Fred van Goor, 13 march 2021.

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
    
        sudo pip3 install lightpipes

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
    
        sudo pip3 install LightPipes==1.2.0
        
  
3) Cannot install LightPipes because pyFFTW does not install:
    With a new Python version it takes a while before new binaries of pyFFTW are available. Because of that we decided from LightPipes version 2.0.7. to skip pyFFTW from the list of required packages and let it be an option. As a consequence the FFT calculations are performed by the FFT of numpy which is slightly slower than pyFFTW.
    For reasonable small grid sizes (less than 1000 x 1000 gridpoints) you will not notice that.
    When pyFFTW becomes available you can install pyFFTW and from that moment LightPipes will use pyFFTW and will be faster.
    So for normal installation do:
    
    .. code-block:: bash
    
        sudo pip3 install LightPipes
        
    To install pyFFTW do:
    
    .. code-block:: bash
    
        sudo pip3 install pyFFTW
        
    To install LightPipes with pyFFTW do:
    
    .. code-block:: bash
    
        sudo pip3 install LightPipes[pyfftw]
        
    If pyFFTW is not installed, LightPipes will show a warning to advise the user to install pyFFTW for maximum performance.
    You can suppress this warning (and all others!) by using the python option -Wignore, so do:
    
    .. code-block:: bash
    
        python -Wignore YourLightPipesScript.py
        
    The warning can also be suppressed by editing the file propagators.py in your local python site-packages directory.

    1) Find your python installation directory:
       For windows:
    
        .. code-block:: bash
    
          where python
        
        For Mac or Linux:
        
        .. code-block:: bash
    
          which python
        
    2) You will find propagators.py in:
    
        .. code-block:: bash
        
          .....\Python3x\Lib\site-packages\LightPipes (windows)
          ...../Python3x/Lib/site-packages/LightPipes (Linux, Mac)
        
    3) Open propagators.py in an editor and change line 14 in:
    
        .. code-block:: bash
        
          _USE_PYFFTW = False
        
    4) After saving propagators.py LightPipes uses numpy-FFT and the warning will be suppressed.
       Of course _USE_PYFFTW must be put back to True after you have successfully installed pyFFTW.
