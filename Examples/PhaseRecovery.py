
clear all;
%define some units
m=1; mm=1e-3*m; nm=1e-9*m;

%Parameters used for the experiment:
size=11*mm; %The CCD-sensor has an area of size x size (NB LightPipes needs square grids!)
lambda=632.8*nm; %wavelength of the HeNe laser used
z=2*m; %propagation distancce from near to far field

%Read near and far field (at a distance of z=2 m) from disk:
N=128; %NxN = number of grid elements in measured intensity profiles
fid=fopen('Inear.prn');
Inear=fscanf(fid,'%f',[N N]);
fclose(fid);
fid=fopen('Ifar.prn');
Ifar=fscanf(fid,'%f',[N N]);
fclose(fid);

%Plot the measured intensity profiles:
figure(1);
subplot(3,2,1);imagesc(Inear);title('Measured Intensity near field'); axis equal; axis off;
subplot(3,2,2);imagesc(Ifar); title('Measured Intensity far field');axis equal; axis off;

%size_new=11*mm; %used in interpolation routines
%N_new=128;      %used in interpolation routines

N_iterations=100; %number of iterations

%Define a field with uniform amplitude- (=1) and phase (=0) distribution
%(= plane wave)
F=LPBegin(size,lambda,N);

%The iteration:
for k=1:N_iterations
    F=LPSubIntensity(Ifar,F);%Substitute the measured far field into the field
    %F=LPInterpol(size_new,N_new,0,0,0,1,F);%interpolate to a new grid
    F=LPForvard(-z,F); %Propagate back to the near field
    %F=LPInterpol(size,N,0,0,0,1,F);%interpolate to the original grid
    F=LPSubIntensity(Inear,F);%Substitute the measured near field into the field
    F=LPForvard(z,F); %Propagate to the far field
end

%The recovered far- and near field and their phase- and intensity
%distributions (phases are unwrapped (i.e. remove multiples of PI)):
Ffar_rec=F;
Ifar_rec=LPIntensity(2,Ffar_rec); Phase_far_rec=LPPhaseUnwrap(1,LPPhase(Ffar_rec));
Fnear_rec=LPForvard(-z,F);
Inear_rec=LPIntensity(2,Fnear_rec); Phase_near_rec=LPPhaseUnwrap(1,LPPhase(Fnear_rec));

%Plot the recovered intensity- and phase distributions:
subplot(3,2,3);imagesc(Inear_rec);title('Recovered Intensity near field'); axis equal; axis off;
subplot(3,2,4);imagesc(Ifar_rec); title('Recovered Intensity far field'); axis equal; axis off;
subplot(3,2,5);imagesc(Phase_near_rec); title('Recovered phase near field'); axis equal; axis off;
subplot(3,2,6);imagesc(Phase_far_rec); title('Recovered phase far field'); axis equal; axis off;
