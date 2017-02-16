::py -2.7 setup.py build_ext
::copy .\fftw3_win32\libfftw3-3.dll .\build\lib.win32-2.7\
py -2.7 setup.py bdist_wheel

