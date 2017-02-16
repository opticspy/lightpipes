import site; site.getsitepackages()
import ctypes
#print("loading libfftw3-3.dll")
ctypes.WinDLL(site.getsitepackages()[1] + "\\fftw3_win64\\libfftw3-3.dll")
#print('libfftw3-3.dll loaded')

