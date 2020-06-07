import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('./LightPipes/_version.py').read())

setuptools.setup(
    name='LightPipes',
    packages=['LightPipes'],
    install_requires = ['numpy', 'pyFFTW', 'scipy'],
    version = __version__,
    description='LightPipes for Python optical toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Fred van Goor',
    author_email='Fred511949@gmail.com',
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/opticspy/lightpipes',
    download_url='https://github.com/opticspy/lightpipes/releases',
)
