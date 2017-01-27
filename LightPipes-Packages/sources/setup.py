from setuptools import setup
from setuptools.extension import Extension
import numpy

# Test if Cython is available
try:
    from Cython.Distutils import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
     
print ("USE_CYTHON =", USE_CYTHON)
 
# If no Cython, we assume a 'LightPipes.cpp' compiled with: 'cython -t --cplus LightPipes.pyx'
ext = '.pyx' if USE_CYTHON else '.cpp'


sources = [
           'LightPipes' + ext,
           'fresnl.cpp',
           'subs.cpp',
           'lpspy.cpp'
           ]

extensions = [
               Extension(
                        'LightPipes',
                        sources,
                        #extra_compile_args = [''],
                        include_dirs = [ numpy.get_include()],
                        libraries = ['libfftw3-3'],
                        language = "c++",
                        )
             ]
 
# Select Extension
if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)
else:
    # If not using Cython, we have to add 'LightPipes.cpp'
     extensions[0].sources.append('LightPipes.cpp');
    
setup(	name = 'LightPipes',
        package_data = { "LightPipes" : [ "libfftw3-3.dll"]},
        include_package_data=True,
		version = '1.1.0',
		description = 'LightPipes for Python optical toolbox',
		author = 'Fred van Goor',
		author_email = 'Fred511949@gmail.com',
		license = 'MIT',
		classifiers = [
			'Development Status :: 3 - Alpha',
			'Programming Language :: Python :: 3.5',
		],
		url = 'https://GitHub.com/FredvanGoor/LightPipes-for-Python/',
		download_url = 'https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/',
		platforms = ['win64'],
		ext_modules = extensions,
		)
