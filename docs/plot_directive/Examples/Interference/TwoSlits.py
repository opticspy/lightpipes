import numpy as np
from LightPipes import *
import matplotlib.pyplot as plt

# Parameters
wavelength = 633 * nm
size = 25 * mm
N = 500
z = 1.0 * m

# Slit parameters
slit_width = 0.10 * mm
slit_height = 15 * mm
slit_distance = 0.8 * mm   # center-to-center separation

# Begin with a plane wave
F = Begin(size, wavelength, N)

# Two rectangular slits
F1 = RectAperture(F, slit_width, slit_height, slit_distance/2)
F2 = RectAperture(F, slit_width, slit_height, -slit_distance/2)

# Coherent addition
F=BeamMix(F1,F2)

# Fresnel propagation to the screen
F = Fresnel(F, z)

# Intensity at the screen
I = Intensity(0, F)

# Coordinates for plotting
x = np.linspace(-size/2, size/2, N) / mm

plt.figure(figsize=(6, 5))
plt.imshow(I, extent=[x[0], x[-1], x[0], x[-1]], cmap='inferno')
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.title("Young's Double-Slit Interference at z = 1 m")
plt.colorbar(label='Normalized intensity')
plt.show()

