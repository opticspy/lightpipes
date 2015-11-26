#Installation of LightPipes for Python on a Macintosh.

Tested on a MAC with a 64 bit Intel processor and Yosemite 10.6 OSX.

###1. Installation of Python:

1.	*Python 2.7* is already pre-installed in Yosemite 10.6. Otherwise download from the official *Python* site: [https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/). The *LightPipes* package is made for *Python* version 2.7, so download *Python* 2.7. (Not version 3)

###2. Installation of Python packages:

1.	The packages *setuptools* and *pip* are already installed in Yosemite 10.6. Otherwise go to [https://pythonhosted.org/setuptools/setuptools.html](https://pythonhosted.org/setuptools/setuptools.html) and [https://pip.pypa.io/en/latest/installing.html](https://pip.pypa.io/en/latest/installing.html)  respectively and follow the instructions on these sites.
2.	For *LightPipes* you might need the *Numpy* package. For graphics: *matplotlib* package.
3.	Open a terminal window and install *Numpy* by typing at the prompt:

	**pip install numpy** (takes a while…)

4.	Install *matplotlib* by typing at the prompt:

	**pip install matplotlib**

5.	Check the installed packages: Type:

	**pip list**

	The response should be like:

		matplotlib(1.4.2)
		numpy(1.9.0)
		pip(1.5.6)
		pyparsing(2.0.3)
		python_dateutil(2.2)
		pytz(2014.7)
		setuptools(7.0)
		six(1.8.0)

6.	Your system is now ready for LightPipes for Python.

###3. Install LightPipes for Python:

1.	Open the terminal and type (copy/paste) at the prompt:


	**easy_install LightPipes**

	(newest version)

	or, from GitHub:


	**easy\_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/LightPipes-1.0.0-py2.7-macosx-10.6-intel.egg**
	
	or, from the downloaded and extracted zip-file:

	**easy_install install\_directory\LightPipes-Packages\LightPipes-1.0.0-py2.7-macosx-10.6-intel.egg**

	where install\_directory is the directory in which you put the zip-file.

2.	This will download the installation and installs LightPipes for Python.
3.	Check by typing:

	**pip list**

	The list should now contain something like:

		lightpipes (1.0.0).

4.	You could un-install LightPipes by typing:

	**pip uninstall LightPipes**

###4. Installation of a very nice editor Geany:
Not available for the mac. Use ‘IDLE’ for editing python documents.

###5. Make your first LightPipes script file:
1.	Start IDLE, open a new document and type (or copy/paste)  the following script: 

		import LightPipes
		import matplotlib.pyplot as plt
		m=1
		nm=1e-9*m
		um=1e-6*m
		mm=1e-3*m
		cm=1e-2*m

		try:
		    LP=LightPipes.Init()
		    
		    wavelength=20*um
		    size=30.0*mm
		    N=1000

		    F=LP.Begin(size,wavelength,N)
		    F1=LP.CircAperture(0.15*mm, 0, -0.6*mm, F)
		    F2=LP.CircAperture(0.15*mm, 0, 0.6*mm, F)    
		    F=LP.BeamMix(F1,F2)
		    F=LP.Fresnel(10*cm,F)
		    I=LP.Intensity(2,F)
		    plt.imshow(I)
		    plt.show()
		    
		finally:
		   del LightPipes

2.	Save the document as Young.py, open a terminal window and type at the prompt:

	**python Young.py**

	Or still in IDLE, do ‘Run’, ‘Run Module’. Or push the F5 button.

3.	After a few seconds a window with the output appears:

![](../img/twoholesPattern.png)

###6. Explanation of the commands

		Import LightPipes  							imports the LightPipes library (from ‘LightPipes.pyd’)

		import matplotlib.pyplot as plt				imports matplotlib for the graphics
		LP=LightPipes.Init()						initiates LightPipes 
													(make a new instance of LightPipes called ‘LP’)
													for a grid-size, grid-dimension and wavelength defined by the Begin command.

		wavelength=20*um							Define the wavelength, grid-size and grid-dimension.
		size=30.0*mm
		N=1000

		F=LP.Begin(size,wavelength,N)				The simulation of Young’s experiment:
		F1=LP.CircAperture(0.15*mm, 0, -0.6*mm, F)	A plane wave hits a screen with two holes.
		F2=LP.CircAperture(0.15*mm, 0, 0.6*mm, F)	The interference pattern is observed at a distance of 10 cm.
		F=LP.BeamMix(F1,F2)
		F=LP.Fresnel(10*cm,F)
		I=LP.Intensity(2,F)

		plt.imshow(I)								Plot and show the output interference pattern
		plt.show()	

		del LightPipes								Be sure that everything is cleaned-up after execution
													(this is normally not necessary but is good practice)

Enjoy LightPipes for Python!

Fred van Goor, 11/24/2015 11:49:43 AM
