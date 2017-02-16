::py -2.7 setup.py build_ext
::copy .\fftw3_win64\libfftw3-3.dll .\build\lib.win-amd64-2.7\
::py -2.7 setup.py bdist_wheel

::py -3.5 setup.py build_ext
::copy .\LightPipes.pth .\build\lib.win-amd64-3.5\
py -3.5 setup.py bdist_wheel

::py -3.6 setup.py build_ext
::copy .\fftw3_win64\libfftw3-3.dll .\build\lib.win-amd64-3.6\
::py -3.6 setup.py bdist_wheel

