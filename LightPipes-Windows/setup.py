import os
import numpy
import struct
from os.path import join
from setuptools import setup
from setuptools.extension import Extension


import platform
SYSTEM = platform.system()
print('SYSTEM = {}'.format(SYSTEM))


try:
    import Cython.Distutils
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
print("USE_CYTHON = {}".format(USE_CYTHON))


if USE_CYTHON:
    LIGHTPIPES = 'LightPipes.pyx'
else:
    # assume a 'LightPipes.cpp' compiled with:
    # 'cython -t --cplus LightPipes.pyx'
    LIGHTPIPES = 'LightPipes.cpp'
sources = [
    LIGHTPIPES,
    'fresnl.cpp',
    'subs.cpp',
    'lpspy.cpp'
]


data_files = None
if SYSTEM == 'Linux':
    ext = Extension(
        'LightPipes', sources,
        include_dirs=[numpy.get_include()],
        library_dirs=['/usr/local/lib/'],
        libraries=['fftw3'],
        language="c++",
    )
elif SYSTEM == 'Windows':
    bits = struct.calcsize("P")*8
    if bits == 32:
        fftw3dir = 'fftw3_win32'
    else:
        fftw3dir = 'fftw3_win64'
    data_files = [('lib/site-packages', [join(fftw3dir, 'libfftw3-3.dll')])]
    ext = Extension(
        'LightPipes', sources,
        include_dirs=[numpy.get_include()],
        library_dirs=[fftw3dir],
        libraries=['libfftw3-3'],
        language="c++",
    )
elif SYSTEM == 'Darwin':
    pass
else:
    pass


if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize([ext])
else:
    extensions = [ext]


setup(
    name='LightPipes',
    version='1.1.1',
    description='LightPipes for Python optical toolbox',
    author='Fred van Goor',
    author_email='Fred511949@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://GitHub.com/FredvanGoor/LightPipes-for-Python/',
    download_url='https://github.com/FredvanGoor/LightPipes-for-Python/raw/master/LightPipes-Packages/',
    platforms=['win64', 'win32', 'linux'],
    ext_modules=extensions,
    data_files=data_files,
)
