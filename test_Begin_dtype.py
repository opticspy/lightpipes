#! /usr/bin/env python
"""
Script to test the Begin command with dtype option.
"""
from LightPipes import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import patches
import numpy as np
import sys

wavelength = 500*nm
size = 25*mm
N = 30000
N2=int(N/2)
w0=2*mm

F=Begin(size,wavelength,N,dtype=np.complex64)
print("type of F:",F._dtype)
print("size of F.field: ",sys.getsizeof(F.field)/1e9," Gbyte")
