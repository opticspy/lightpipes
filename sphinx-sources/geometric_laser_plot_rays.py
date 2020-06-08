import matplotlib.pyplot as plt
import numpy as np

def Z1(L,R1,R2):
    A=1-2*L/R2
    B=2*L-2*L*L/R2
    C=4*L/(R1*R2)-2/R1-2/R2
    D=1+4*L*L/(R1*R2)-4*L/R1-2*L/R2
    m=(A+D)/2
    g1=1-L/R1
    g2=1-L/R2
    g=g1*g2
    if g1*g2>=0.0 and g1*g2<=1.0:
        #print('confined, g1*g2 = %f'%g)
        return(A-D)/(2*C)
    else:
        #print('not confined, g1*g2 = %f It must be: 0<=g1*g2<=1'%g)
        return 0

def ZR(L,R1,R2):
    A=1-2*L/R2
    B=2*L-2*L*L/R2
    C=4*L/(R1*R2)-2/R1-2/R2
    D=1+4*L*L/(R1*R2)-4*L/R1-2*L/R2
    m=(A+D)/2
    g1=1-L/R1
    g2=1-L/R2
    if g1*g2>=0.0 and g1*g2<=1.0:
        return np.sqrt(1-m*m)/C
    else:
        return 0

def R0(L,R1,R2,c,rays):
    y0=np.zeros([rays])
    theta0=np.zeros([rays])
    Z_1=Z1(L,R1,R2)
    Z_R=ZR(L,R1,R2)
    for ray in range(0,rays):
        alpha=ray/rays*2*np.pi
        y0[ray]=2*c*(Z_1*np.cos(alpha)-Z_R*np.sin(alpha))
        theta0[ray]=2*c*np.cos(alpha)
    return (y0,theta0)

def w(z,L,R1,R2,c):
    Z_1=Z1(L,R1,R2)
    Z_R=ZR(L,R1,R2)
    return c*np.sqrt(2*((z+Z_1)*(z+Z_1)+Z_R*Z_R))

def plotrays(L,R1,R2,c,rnd,rays):
    n=2*rnd
    y=np.zeros([rays,n+1])
    theta=np.zeros([rays,n+1])
    z=np.zeros([n+1])
    zze=np.zeros(100)
    zzo=np.zeros(100)
    We=np.zeros(100)
    Wo=np.zeros(100)
    sec_moments=False
    for iz in range(0,100):
        zze[iz]=iz/100*L
        zzo[iz]=(100-iz)/100*L
        We[iz]=w(zze[iz],L,R1,R2,c)
        Wo[iz]=w(zzo[iz],L,R1,R2,c)
    z[0]=0.0
    (y0,theta0)=R0(L,R1,R2,c,rays)
    plt.rcParams["figure.figsize"] = (10,6)    
    for ray in range(0,rays):
        y[ray][0]=y0[ray]
        theta[ray][0]=theta0[ray]
        for i in range(1,n+1):
            if i % 2 ==0:
                R=R1 #i=even
                if sec_moments:
                    plt.plot((zze+(i-2)*L)/L/2,We,(zze+(i-2)*L)/L/2,-We,color='black', linestyle='dashed')
            else:
                R=R2 #i=odd
                if sec_moments:
                    plt.plot((-zzo+(i+1)*L)/L/2,Wo,(-zzo+(i+1)*L)/L/2,-Wo,color='black', linestyle='dashed')
            y[ray][i]=y[ray][i-1]+L*theta[ray][i-1]
            theta[ray][i]=-2/R*y[ray][i-1]+(1-2*L/R)*theta[ray][i-1]
            z[i]=(z[i-1]+L)

        plt.plot(z[0:n+1]/L/2,y[ray][0:n+1], color='red')

    for i in range(0,n+1):
        plt.plot([0,0],[-2*c,2*c],[i/2,i/2],[-2*c,2*c],color='black', linestyle='dashed')
        if i % 2 ==0:
            s=' R1' #i=even
        else:
            s=' R2' #i=odd
        plt.text(i/2,2*c,s)
        
    
    plt.title('confined rays')
    plt.xlabel('roundtrip #')
    plt.ylabel('y[a.u.]')
    plt.show()
    
L = 1 # resonator length
R1 = 1.1 # radius mirror 1
R2 = 5.0 # radius mirror 2
c = 1 # the unknown constant (related to the wavelength)
roundtrips = 2 # number of roundtrips to be plotted
rays = 40 # number of rays

plotrays(L,R1,R2,2,roundtrips,rays)
