#! /usr/bin/env python
"""
Script to test the Begin command with dtype option.
"""
from LightPipes import *
import numpy as np
import sys

wavelength = 500*nm
size = 25*mm
N = 3000
N2=int(N/2)
w0=2*mm

print("LightPipes version = ", LPversion)
print("without dtype option:")
F=Begin(size,wavelength,N)
print("type of F:",F._dtype)
print("size of F.field: ",sys.getsizeof(F.field)/1e9," Gbyte")
print("\n")
print("with dtype option:")
F=Begin(size,wavelength,N,dtype=np.complex64)
print("type of F:",F._dtype)
print("size of F.field: ",sys.getsizeof(F.field)/1e9," Gbyte")
