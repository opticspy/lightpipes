import platform
import struct
from os.path import join

import numpy
from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize

SYSTEM = platform.system()
print('SYSTEM = {}'.format(SYSTEM))


def _lpfile(*path):
    return join('LightPipes', *path)


sources = [
    _lpfile('_LightPipes.pyx'),
    _lpfile('fresnl.cpp'),
    _lpfile('subs.cpp'),
    _lpfile('lpspy.cpp')
]

if SYSTEM == 'Windows':
    bits = struct.calcsize("P")*8
    if bits == 32:
        fftw3dir = 'fftw3_win32'
        libraries = ['./LightPipes/fftw3_win32/libfftw3-3']
    else:
        fftw3dir = 'fftw3_win64'
        libraries = ['./LightPipes/fftw3_win64/libfftw3-3']
    data_files = [('lib/site-packages/LightPipes', [_lpfile(fftw3dir, 'libfftw3-3.dll')])]
    library_dirs = [fftw3dir]
else:  # Linux, Darwin
    data_files = None
    libraries = ['fftw3']
    library_dirs = ['/usr/local/lib/']

ext = Extension(
    'LightPipes._LightPipes',
    sources=sources,
    include_dirs=[numpy.get_include()],
    library_dirs=library_dirs,
    libraries=libraries,
    language="c++",
)
extensions = cythonize([ext])
exec(open('./LightPipes/_version.py').read())

setup(
    name='LightPipes',
    packages=['LightPipes'],
    #install_requires=["numpy>=1.11.3"],
    #version='1.1.2',
    version = __version__,
    description='LightPipes for Python optical toolbox',
    author='Fred van Goor',
    author_email='Fred511949@gmail.com',
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/opticspy/lightpipes',
    download_url='https://github.com/opticspy/lightpipes/releases',
    platforms=['win64', 'win32', 'linux'],
    ext_modules=extensions,
    data_files=data_files,
)
