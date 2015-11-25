#Installation of LightPipes for Python on a UNIX machine

Tested 32 and a 64 bit machines with linux MINT 17.

##1	Installation of Python:

1. Python 2.7 is already pre-installed in linux MINT. Otherwise download from the official Python site: [https://www.python.org/](https://www.python.org/). The *LightPipes* package is made for Python version 2.7, so download Python 2.7. (**Not version 3**)

##2.	Installation of Python packages:

1.	The packages *setuptools* and *pip* could be pre-installed. Otherwise go to [https://pythonhosted.org/setuptools/setuptools.html](https://pythonhosted.org/setuptools/setuptools.html)  and [https://pip.pypa.io/en/latest/installing.html](https://pip.pypa.io/en/latest/installing.html) respectively and follow the instructions on these sites or use the software manager of (for example) MINT to install them (recommended).
2.	For LightPipes you may need the *Numpy* package. For graphics the *matplotlib* package.
3.	Open a terminal window and install *Numpy* by typing at the prompt:

	**pip install numpy** (takes a while…)

	or use the software manager.

4.	Install *matplotlib* by typing at the prompt:

	**pip install matplotlib** 

	or use the software manager (recommended).

5.	Check the installed packages. Type:

	**pip list**

6.	 The response should be like:
	 
		matplotlib(1.4.2)
		numpy(1.9.0)
		pip(1.5.6)
		pyparsing(2.0.3)
		python_dateutil(2.2)
		pytz(2014.7)
		setuptools(7.0)
		six(1.8.0)

7.	Your system is now ready for *LightPipes for Python*.

##3.	Install LightPipes for Python:

1.	Open a terminal and type (copy/paste) at the prompt:

	**easy_install LightPipes**

	(newest version)

	**easy\_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/LightPipes-1.0.0-py2.7- linux-x86_64.egg**

	for the 64-bits version or:

	**easy\_install https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/LightPipes-1.0.0-py2.7- linux-i686.egg**

	for the 32-bits version.
2. This will download the installation and installs *LightPipes for Python*.
3. Type:

	**pip list**

4.	*LightPipes(1.0.0)* or similar should be in the list now.
5.	You could uninstall LightPipes by typing:

	**pip uninstall LightPipes**

##4.	Installation of a very nice editor ‘Geany’:

1.	*Geany* is a very useful editor for editing program files including *Python* scripts.
2.	Download from: [http://www.geany.org/Download/Releases](http://www.geany.org/Download/Releases) *geany-1.2.6setup.exe*.
3.	Execute: *geany-1.2.6setup.exe*.
4.	Choose the default settings- and install directory.

##5.	Make your first LightPipes script file.

1.	Start *Geany*, open a new document and type (or copy/paste)  the following script:

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

2.	Save the document as ‘Young.py’, and push in *Geany*  the execute button or open a terminal window and type at the prompt:

	**python Young.py**

3.	After a few seconds a window with the output appears:

![](../../img/twoholesPattern.png)


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
