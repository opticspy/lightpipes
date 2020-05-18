
from setuptools import setup

exec(open('./LightPipes/_version.py').read())

setup(
    name='LightPipes',
    packages=['LightPipes'],
    install_requires = ['numpy', 'pyFFTW', 'scipy'],
    version = __version__,
    description='LightPipes for Python optical toolbox',
    author='Fred van Goor',
    author_email='Fred511949@gmail.com',
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
      #  'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/opticspy/lightpipes',
    download_url='https://github.com/opticspy/lightpipes/releases',
    platforms=['windows', 'linux', 'Mac OSX'],
)
