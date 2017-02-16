from setuptools import setup
from setuptools.extension import Extension
import numpy
from sys import platform
import struct
import shutil
import sys, sysconfig,os

# Test if Cython is available
try:
    from Cython.Distutils import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
     
print ("USE_CYTHON =", USE_CYTHON)
 
# If no Cython, we assume a 'LightPipes.cpp' compiled with: 'cython -t --cplus LightPipes.pyx'
ext = '.pyx' if USE_CYTHON else '.cpp'

# Get the name of the build dirctory:
def distutils_dir_name(dname):
    """Returns the name of a distutils build directory"""
    f = "{dirname}.{platform}-{version[0]}.{version[1]}"
    return f.format(dirname=dname,
                    platform=sysconfig.get_platform(),
                    version=sys.version_info)

build_lib_dir = os.path.join('build', distutils_dir_name('lib'))

print('The library will be build in:',build_lib_dir)

sources = [
           'LightPipes' + ext,
           'fresnl.cpp',
           'subs.cpp',
           'lpspy.cpp'
           ]
           
print(' The platform is:',platform)

if ("linux" in platform): # platform is linux in python 3 or linux in python 2.7
    extensions = [
                   Extension(
                            'LightPipes',
                            sources,
                            #extra_compile_args = [''],
                            include_dirs = [ numpy.get_include()],
                            library_dirs = ['/usr/local/lib/'],
                            libraries = ['fftw3'],
                            language = "c++",
                            )
             ]
             
elif (platform == "win32"):	# platform is windows 32 or 64 bits in python 2.7 or 3
    bits = struct.calcsize("P")*8
    if bits == 32:
        fftw3dir='.\\fftw3_win32'
        fftw3dll='.\\fftw3_win32\\libfftw3-3.dll'
        cmp_arg = '/EHsc'
    else:
        fftw3dir='.\\fftw3_win64'
        fftw3dll='.\\fftw3_win64\\libfftw3-3.dll'
        cmp_arg = ''

    extensions = [
                   Extension(
                            'LightPipes',
                            sources,
                            extra_compile_args = [cmp_arg],
                            include_dirs = [ numpy.get_include()],
                            libraries = [fftw3dir + '\\libfftw3-3'],
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
        version = '1.1.1',
        description = 'LightPipes for Python optical toolbox',
        author = 'Fred van Goor',
        author_email = 'Fred511949@gmail.com',
        license = 'MIT',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        url = 'https://GitHub.com/FredvanGoor/LightPipes-for-Python/',
        download_url = 'https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/',
        platforms = ['win64', 'win32', 'linux'],
        ext_modules = extensions,
        )


shutil.copyfile(fftw3dll, build_lib_dir + '/libfftw3-3.dll')
print('copied libfftw3-3.dll to:', build_lib_dir)
