#Command reference
----------
### Axicon(*phi*, *n1*, *x\_shift*, *y\_shift*, *Field*) ###
propagates the *Field* through an axicon. 
*phi*: top angle in radians;  
*n1*:  refractive index (must be real);  
*x\_shift*, *y\_shift*: shift from the centre. 

### BeamMix(*Field1*, *Field2*) ###
Addition of *Field1* and *Field2*.

### Begin(*grid\_size*, *lambda*, *grid\_dimension*) ###
initialises a uniform field with unity amplitude and zero phase. 
*grid\_size*: the size of the grid in units you choose, 
*lambda*: the wavelength of the field with the same units as the grid size, 
*grid\_dimension*: the dimension of the grid. This must be an even number.

###CircAperture(*R*, *x\_shift*, *y\_shift*, *Field*)
circular aperture. 
*R*=radius, 
*x\_shift*, *y\_shift* = shift from centre.

###CircScreen(*R*, *x\_shift*, *y\_shift*, *Field*)
circular screen. 
*R*=radius, 
*x\_shift*, *y\_shift* = shift from centre. 

###Convert(*Field*)
converts the *field* from a spherical grid to a normal grid.

###Forvard(*z*, *Field*)
propagates the *field* a distance *z* using FFT.

###Forward(*z*, *new\_size*, *new\_number*, *Field*)
propagates the *field* a distance *z*, using direct integration of the Kirchoff-Fresnel integral.

###Fresnel(*z*, *Field*)
propagates the *field* a distance *z*. A convolution method has been used to calculate the diffraction integral

###Gain(*Isat*, *gain*, *length*, *Field*)
Laser saturable gain sheet. 
*Isat*=saturation intensity, 
*gain*= small signal gain, 
*length*=length of gain medium

###GaussAperture(*R*, *x\_shift*, *y\_shift*, *T*, *Field*)
Gauss aperture. 
*R*=radius, 
*x\_shift*, *y\_shift* = shift from centre; 
*T*= centre transmission

###GaussHermite(*n*, *m*, *A*, *w0*, *Field*)
substitutes a TEMm,n mode with waist *w0* and amplitude *A* into the *field*.

###GaussScreen(*R*, *x\_shift*, *y\_shift*, *T*, *Field*)
Gauss screen. 
*R*=radius, 
*x\_shift*, *y\_shift* = shift from centre; 
*T*= centre transmission

###IntAttenuator(*Att*, *Field*)
Intensity Attenuator. Attenuates the *field*-intensity by a factor *Att*

###Intensity(*flag*, *Field*)
calculates the intensity of the *field*. 
*flag*=0: no scaling; 
*flag*=1: normalisation of the intensity; 
*flag*=2: bitmap with gray scales

###Interpol(*new\_size*, *new\_n*, *xs*, *ys*, *phi*, *magn*, *Field*)
interpolates the field to a new grid.
*new\_size*: new grid size;
*new\_n*: new grid dimension;
*xs*, *ys* : the shifts of the field in the new grid;
*phi*: angle of rotation (after the shifts);
*magn*: magnification (last applied)

###Lens(*f*, *x\_shift*, *y\_shift*, *Field*)
propagates the field through a lens.
*f*: focal length;
*x\_shift*, *y\_shift*: transverse shifts of the lens optical axis

###LensForvard(*f*, *z*, *Field*)
propagates the *field* a distance *z* using a variable coordinate system.
*f*: focal length of the input lens:
*z*: distance to propagate

###LensFresnel(*f*, *z*, *Field*)
propagates the *field* a distance *z* using a variable coordinate system.
*f*: focal length of the input lens;
*z*: distance to propagate

###MultIntensity(*Intensity*, *Field*)
multiplies the *field* with an intensity profile stored in the array: *Intensity*  

###MultPhase(*Phase*, *Field*)
multiplies the *field* with a phase profile stored in the array: *Phase*

###Normal(*Field*)
normalizes the *field*.

###Phase(*Field*)
calculates the phase of the *field*

###PhaseUnwrap(*Phase*)
unwraps *phase*.

###PipFFT(*Direction*, *Field*)
Performs a Fourier transform to the *Field*.
*Direction* = 1: Forward transform;
*Direction* = -1: Inverse transform

###Polarizer(*Phi*, *Fx*, *Fy*)
Polarizer. Ouputs a linear polarized field.
*Phi*=polarizer angle,
*Fx*, *Fy*=input fields of horizontal and vertical components. 

###RandomIntensity(*seed*, *Field*)
Random intensity mask.
'*seed*' is an arbitrary number to initiate the random number generator

###RandomPhase(*seed*, *max*, *Field*)
Random phase mask.
'*seed*' is an arbitrary number to initiate the random number generator;
'*max*' is the maximum value of the phase.

###RectAperture(*sx*, *sy*, *x\_shift*, *y\_shift*, *phi*, *Field*)
rectangular aperture. 
*sx*, *sy*: dimensions of the aperture; 
*x\_shift*, *y\_shift*: shift from centre; 
*phi*: rotation angle.

###RectScreen(*sx*, *sy*, *x\_shift*, *y\_shift*, *phi*, *Field*)
rectangular screen. 
*sx*, *sy*: dimensions of the screen; 
*x\_shift*, *y\_shift*: shift from centre; 
*phi*: rotation angle.

###ReflectMultiLayer(*P*, *N0*, *Ns*, *N*, *d*, *Th*, *F*)
MultiLayer Reflector. Reflection of the *field* by a multi-layer mirror. 
*P*=0: s-Polarization; P=1: p-Polarization; 
*N0*=refractive index of incident medium (must be real); 
*Ns*=refractive index of substrate; 
*N*= array with (complex) index of the layers; 
*d*= array with the geometrical thicknesses of the layers; 
*Th*= angle of incidence at first layer; 
*F*= the input field

###Steps(*z*, *N\_steps*, *Refract[N, N]*, *Field*)
Propagates '*Field*' a distance *z* in '*N\_steps*' steps in a medium with a complex refractive index stored in the NxN matrix '*Refract*'. '*N*' is the grid dimension.

###Strehl(*Field*)
calculates the Strehl ratio.

###SubIntensity(*intensity*, *Field*)
substitutes an intensity profile into the field. The profile must be stored in the array: Intens

###SubPhase(*phase*, *Field*)
substitutes a phase profile into the field.The phase profile must be stored in the array: phase.

###Tilt(*tx*, *ty*, *Field*)
introduces tilt in to the *field* distribution. *tx*, *ty* = tilt components in radians.

###TransmitMultiLayer(*P*, *N0*, *Ns*, *N*, *d*, *Th*, *F*)
MultiLayer Transmission. Transmission of the *field* through a multi-layer coated substrate. 
*P*=0: s-Polarization; P=1: p-Polarization; 
*N0*=refractive index of incident medium (must be real); 
*Ns*=refractive index of substrate; 
*N*= array with (complex) index of the layers; 
*d*= array with the geometrical thicknesses of the layers; 
*Th*= angle of incidence at first layer; 
*F*= the input field

###Zernike(*n*, *m*, *R*, *A*, *Field*)
Introduces arbitrary Zernike aberration into the *field*. 
*n* and *m* are the integer orders, (See Born and Wolf, 6th edition p.465, Pergamon 1993). 
*R* is the radius at which the phase amplitude reaches *A* (in radians)
