from LightPipes import *
wavelength = 500*nm
size = 25*mm
N = 500
F = Begin(size, wavelength, N)
F = CircAperture(F, 2*mm, x_shift = 5*mm, y_shift = 3*mm)
F = Fresnel(F, 10*m)
Xc,Yc, NXc, NYc = Centroid(F)
print("Xc = {:4.2f} mm, Yc = {:4.2f} mm".format(Xc/mm, Yc/mm))
