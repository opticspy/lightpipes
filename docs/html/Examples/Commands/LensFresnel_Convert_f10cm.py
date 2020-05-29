from LightPipes import *
import matplotlib.pyplot as plt

def TheExample(N):
    fig=plt.figure(figsize=(15,9.5))
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    labda=1000*nm;
    size=10*mm;
    
    f=10*cm
    f1=10*m
    f2=f1*f/(f1-f)
    frac=f/f1
    newsize=frac*size
    w=5*mm;
    F=Begin(size,labda,N);
    F=RectAperture(w,w,0,0,0,F);
    
#1) Using Lens and Fresnel:
    F1=Lens(f,0,0,F)
    F1=Fresnel(f,F1)
    phi1=Phase(F1);phi1=PhaseUnwrap(phi1)
    I1=Intensity(0,F1);
    x1=[]
    for i in range(N):
        x1.append((-size/2+i*size/N)/mm)  
    
#2) Using Lens + LensFresnel and Convert:
    F2=Lens(f1,0,0,F);
    F2=LensFresnel(f2,f,F2);
    F2=Convert(F2);
    phi2=Phase(F2);phi2=PhaseUnwrap(phi2)
    I2=Intensity(0,F2);
    x2=[]

    for i in range(N):
        x2.append((-newsize/2+i*newsize/N)/mm)

    ax1.plot(x1,phi1[int(N/2)],'k--',label='Without spherical coordinates')
    ax1.plot(x2,phi2[int(N/2)],'k',label='With spherical coordinates');
    ax1.set_xlim(-newsize/2/mm,newsize/2/mm)
    ax1.set_ylim(-2,4)
    ax1.set_xlabel('x [mm]');
    ax1.set_ylabel('phase [rad]');
    ax1.set_title('phase, N = %d' %N)
    legend = ax1.legend(loc='upper center', shadow=True)
    
    ax2.plot(x1,I1[int(N/2)],'k--',label='Without spherical coordinates')
    ax2.plot(x2,I2[int(N/2)], 'k',label='With spherical coordinates');
    ax2.set_xlim(-newsize/2/mm,newsize/2/mm)
    ax2.set_ylim(0,100000)
    ax2.set_xlabel('x [mm]');
    ax2.set_ylabel('Intensity [a.u.]');
    ax2.set_title('intensity, N = %d' %N)
    legend = ax2.legend(loc='upper center', shadow=True)
    
    ax3.imshow(I1);ax3.axis('off');ax3.set_title('Without spherical coordinates')
    ax3.set_xlim(int(N/2)-N*frac/2,int(N/2)+N*frac/2)
    ax3.set_ylim(int(N/2)-N*frac/2,int(N/2)+N*frac/2)
    ax4.imshow(I2);ax4.axis('off');ax4.set_title('With spherical coordinates')
    plt.figtext(0.3,0.95,'Spherical Coordinates, f = 10cm lens\nGrid dimension is: %d x %d pixels' %(N, N), fontsize = 18, color='red')

TheExample(100) #100 x 100 grid

TheExample(1000) #1000 x 1000 grid

plt.show()
