import platform
import struct
from os.path import join

import numpy
from setuptools import setup
from setuptools.extension import Extension

SYSTEM = platform.system()
print('SYSTEM={}'.format(SYSTEM))


try:
    import Cython.Distutils  # noqa
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
print("USE_CYTHON={}".format(USE_CYTHON))


def _lpfile(*path):
    return join('LightPipes', *path)


if USE_CYTHON:
    LIGHTPIPES = '_LightPipes.pyx'
else:
    # assume a 'LightPipes.cpp' compiled with:
    # 'cython -t --cplus LightPipes.pyx'
    LIGHTPIPES = '_LightPipes.cpp'
sources = [
    _lpfile(LIGHTPIPES),
    _lpfile('fresnl.cpp'),
    _lpfile('subs.cpp'),
    _lpfile('lpspy.cpp')
]

if SYSTEM == 'Windows':
    bits = struct.calcsize("P")*8
    if bits == 32:
        fftw3dir = 'fftw3_win32'
    else:
        fftw3dir = 'fftw3_win64'
    data_files = [('lib/site-packages', [_lpfile(fftw3dir, 'libfftw3-3.dll')])]
    libraries = ['libfftw3-3']
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


if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize([ext])
else:
    extensions = [ext]


setup(
    name='LightPipes',
    packages=['LightPipes'],
    install_requires=["numpy>=1.7.1"],
    version='1.1.0',
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
    url='https://github.com/opticspy/lightpipes',
    download_url='https://github.com/opticspy/lightpipes/releases',
    platforms=['win64', 'win32', 'linux'],
    ext_modules=extensions,
    data_files=data_files,
)