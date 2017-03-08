#include "lpspy.h"
#define Pi		3.141592654

#define test_string "LightPipes for Python: test passed."

// 16 January 2017
// changes: added     fftw_free(in_out); in Forvard, Fresnel and PipFFT
// To prevent memory leaks!!
//
// 18 January 2017
// Repaired error in LensForvard, FieldTmp is needed if z1>0.
// Thanks to  guyskk@qq.com
//
// 27 February 2017
// Implemneted 2-D PhaseUnwrap
// 

using namespace std;
complex<double> _j (0.0 , 1.0);
lpspy::lpspy(){
    N = 100;
    lambda = 500e-9;
    size = 30e-3;
    doub1 = 0.0;
    int1 =  0;
}
lpspy::~lpspy(){
}

CMPLXVEC lpspy::Axicon(double phi, double n1, double x_shift, double y_shift, CMPLXVEC Field ){
    double pi2, K, dx, x, x2, y, theta, Ktheta;
    int n2;
    pi2=Pi*2.;
    K=pi2/lambda;
    n2=(int) N/2;
    dx=size/N;
    theta=asin(n1*cos(phi/2)+phi/2-Pi/2);
    Ktheta=K*theta;
    for ( int i=0; i<N; i++)
    {
        x=(i-n2)*dx-x_shift;
        x2=x*x;
        for ( int j=0;j<N; j++)
        {
            double fi;
            y=(j-n2)*dx-y_shift;
            fi=-Ktheta*sqrt(x2+y*y);
            Field.at(i).at(j) = Field.at(i).at(j) * exp(_j * fi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::BeamMix(CMPLXVEC Field1, CMPLXVEC Field ){
    for ( int  i=0; i<N; i++)
    {
        for ( int  j=0;j<N; j++)
        {
            Field.at(i).at(j) +=  Field1.at(i).at(j);
        }
    }
    return Field;
}
CMPLXVEC lpspy::Begin(double Size, double Lambda, int NN){
    CMPLXVEC Field;
    Field.resize(NN, vector<complex<double> >(NN,1.0));
    N=NN;
    size = Size;
    lambda = Lambda;
    int1 = 0;
    doub1 = 0.0;
    return Field;
}
CMPLXVEC lpspy::CircAperture(double R, double x_shift, double y_shift, CMPLXVEC Field ){
    double RR, dx, x, y;
    int i2;
    RR=R*R;
    dx = size/N;
    i2 = (int ) N/2+1;
    for ( int  i=0; i<N; i++)
    {
        for ( int  j=0;j<N; j++)
        {
            x=(i - i2 + 1) * dx - x_shift;
            y=(j - i2 + 1) * dx - y_shift;
            if((x*x + y*y) > RR)
            {
                Field.at(i).at(j) = 0.0;
            
            }
        }
    }
    return Field;
}
CMPLXVEC lpspy::CircScreen(double R, double x_shift, double y_shift, CMPLXVEC Field ){
    double RR, dx, x, y;
    int i2;
    RR=R*R;
    dx = size/N;
    i2 = (int ) N/2+1;
    for ( int  i=0; i<N; i++)
    {
        for ( int  j=0;j<N; j++)
        {
            x=(i - i2 + 1) * dx - x_shift;
            y=(j - i2 + 1) * dx - y_shift;
            if((x*x + y*y) <= RR)
            {
                Field.at(i).at(j) = 0.0;
            }
        }
    }
    return Field;
    }
    CMPLXVEC lpspy::Convert( CMPLXVEC Field ){
    double x,x2,y,dx,pi2,K,f;
    int n2;
    if (doub1 == 0.) return Field;
    f = -1./doub1;
    pi2=3.1415926*2.;
    K=pi2/lambda;
    n2=(int) N/2;
    dx=size/N;
    for (int i=0;i< N; i++){
        x=(i-n2)*dx;
        x2=x*x;
        for (int j=0;j< N; j++){ 
            double fi;
            y=(j-n2)*dx;
            fi=-K*(x2+y*y)/(2.*f);
            Field.at(i).at(j) *= exp(_j * fi);
        }
    }
    doub1 = 0.0;
    return Field;
    }
    CMPLXVEC lpspy::Forvard(double zz, CMPLXVEC Field ){
    fftw_complex* in_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N * N);
    if (in_out == NULL) return Field;
    int ii, ij, n12;
    long ik, ir;
    double z,z1,cc;
    double sw, sw1, bus, abus, pi2, cab, sab, kz, cokz, sikz;
    pi2=2.*3.141592654;
    z=fabs(zz);
    kz = pi2/lambda*z;
    cokz = cos(kz);
    sikz = sin(kz);
    ik=0;
    ii=ij=1;
    for (int i=0;i<N; i++){
        for (int j=0;j<N; j++){
            in_out[ik][0] = Field.at(i).at(j).real()*ii*ij;
            in_out[ik][1] = Field.at(i).at(j).imag()*ii*ij; 
            ik++;
            ij=-ij;
        }
        ii=-ii;
    }
    fftw_plan planF = fftw_plan_dft_2d (N, N, in_out, in_out, FFTW_FORWARD, FFTW_ESTIMATE);
    if (planF == NULL) return Field;
    fftw_plan planB = fftw_plan_dft_2d (N, N, in_out, in_out, FFTW_BACKWARD, FFTW_ESTIMATE);
    if (planB == NULL) return Field;  
    // Spatial filter, (c)  Gleb Vdovin  1986:  
    if (zz>=0.) fftw_execute(planF);
    else fftw_execute(planB);
    if(zz >= 0.){
       z1=z*lambda/2.;
       n12=N/2;
       ik=0;
       for (int i=0;i<N; i++){
           for (int j=0;j<N; j++){ 
               sw=((i-n12)/size);
               sw *= sw;
               sw1=((j-n12)/size);
               sw1 *= sw1;
               sw += sw1; 
               bus=z1*sw;
               ir = (long) bus;
               abus=pi2*(ir- bus);
               cab=cos(abus);
               sab=sin(abus);
               cc=in_out[ik][0]*cab-in_out[ik][1]*sab;
               in_out[ik][1]=in_out[ik][0]*sab+in_out[ik][1]*cab;
               in_out[ik][0]=cc;
               ik++;
           }
       }
    }
    else { 
      z1=z*lambda/2.;
      n12=N/2;
      ik=0;
      for (int i=0;i<N; i++){
        for (int j=0;j<N; j++){ 
            sw=((i-n12)/size);
            sw *= sw;
            sw1=((j-n12)/size);
            sw1 *= sw1;
            sw += sw1; 
            bus=z1*sw;
            ir = (long) bus;
            abus=pi2*(ir- bus);
            cab=cos(abus);
            sab=sin(abus);
            cc=in_out[ik][0]*cab + in_out[ik][1]*sab;
            in_out[ik][1]= in_out[ik][1]*cab-in_out[ik][0]*sab;
            in_out[ik][0]=cc;
            ik++;
        }
      }
    }
    if (zz>=0.) fftw_execute(planB);
    else fftw_execute(planF);
    ik=0;
    ii=ij=1;
    for (int i=0;i<N; i++){    
        for (int j=0;j<N; j++ ){
            Field.at(i).at(j) = complex<double>((in_out[ik][0]*ii*ij * cokz - in_out[ik][1]*ii*ij * sikz)/N/N,\
                                               ( in_out[ik][1]*ii*ij * cokz + in_out[ik][0]*ii*ij * sikz)/N/N );
            ij=-ij;
            ik++;
        }
        ii=-ii;
    }
    fftw_destroy_plan(planF);
    fftw_destroy_plan(planB);
    fftw_free(in_out);
    fftw_cleanup();
    return Field;
    }
CMPLXVEC lpspy::Fresnel(double z, CMPLXVEC Field ){
    int i,j,fn2, fn22,io,jo,no2,ii,ij,iiij;
    long ik, ik1, ik2, ik3, ik4;
    double  RR, dx, pi2, kz, cokz, sikz, FR, FI;
    double cc, fc1, fs1, fc2, fs2, fc3, fs3, fc4, fs4, R1, R2, R3, R4;
    double c4c1, c2c3, c4s1, s4c1, s2c3, c2s1, s4c3, s2c1, c4s3, s2s3, s2s1, c2s3, s4s1, c4c3, s4s3, c2c1, sh;
    pi2=2.*3.141592654;

    dx=size/(N-1.);
   
    kz = pi2/lambda*z;
    cokz = cos(kz);
    sikz = sin(kz);

/*  Allocating a LOT OF MEMORY */

    fn2=N*2;
    fftw_complex* in_outF = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * fn2 * fn2);
    fftw_complex* in_outK = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * fn2 * fn2);
    for (int i = 0;i<fn2*fn2;i++){
        in_outK[i][0]=0.0; in_outK[i][1]=0.0;
        in_outF[i][0]=0.0; in_outF[i][1]=0.0;
        }
    if (in_outF == NULL) return Field;
    if (in_outK == NULL) return Field;
    fftw_plan planFF = fftw_plan_dft_2d (fn2, fn2, in_outF, in_outF, FFTW_FORWARD, FFTW_ESTIMATE);
    if (planFF == NULL) return Field;
    fftw_plan planFB = fftw_plan_dft_2d (fn2, fn2, in_outF, in_outF, FFTW_BACKWARD, FFTW_ESTIMATE);
    if (planFB == NULL) return Field; 
    fftw_plan planKF = fftw_plan_dft_2d (fn2, fn2, in_outK, in_outK, FFTW_FORWARD, FFTW_ESTIMATE);
    if (planKF == NULL) return Field;
    fftw_plan planKB = fftw_plan_dft_2d (fn2, fn2, in_outK, in_outK, FFTW_BACKWARD, FFTW_ESTIMATE);
    if (planKB == NULL) return Field;

    sh= +.5;
    fn22=N+1;
    no2=N/2;
    RR=sqrt(1./(2.0*lambda*z))*dx*2.0;    

    ii=ij=1;
    ik=0;
    for (i=fn22-no2;i <= fn22+no2-1; i++){
       io=i-fn22;
       R1=RR*(io - .5 + sh);
       R3=RR*(io + .5 + sh);
       for (j=fn22-no2;j <= fn22+no2-1; j++){
          iiij=ii*ij;
          jo=j-fn22;
          ik1=(i-1)*fn2+j-1;
          /* Fresnel staff  */
          R2=RR*(jo - .5 + sh);
          R4=RR*(jo + .5 + sh);
          fresnl(R1,&fs1, &fc1);
          fresnl(R2,&fs2, &fc2);
          fresnl(R3,&fs3, &fc3);
          fresnl(R4,&fs4, &fc4);

          c4c1=fc4*fc1;
          c2s3=fc2*fs3;
          c4s1=fc4*fs1;
          s4c1=fs4*fc1;
          s2c3=fs2*fc3;
          c2s1=fc2*fs1;
          s4c3=fs4*fc3;
          s2c1=fs2*fc1;
          c4s3=fc4*fs3;

          s2s3=fs2*fs3;
          s2s1=fs2*fs1;
          c2c3=fc2*fc3;
          s4s1=fs4*fs1;
          c4c3=fc4*fc3;
          c4c1=fc4*fc1;
          s4s3=fs4*fs3;
          c2c1=fc2*fc1;
          
          in_outK[ik1][0]=0.5*(c4s3+s4c3-c4s1-s4c1-c2s3-s2c3+c2s1+s2c1)*iiij;
          in_outK[ik1][1]=0.5*(-c4c3+s4s3+c4c1-s4s1+c2c3-s2s3-c2c1+s2s1)*iiij;

          /* Field staff */ 
          in_outF[ik1][0] = Field.at(i - no2 - 1).at(j - no2 - 1).real()*iiij;
          in_outF[ik1][1] = Field.at(i - no2 - 1).at(j - no2 - 1).imag()*iiij;

          ik++;
          ij=-ij;
       }
       ii=-ii;
    }

    fftw_execute(planKF);
    fftw_execute(planFF);

    ik=0;
    ii=ij=1;
    for(i=1; i<=fn2; i++){
       for(j=1; j<=fn2; j++){
          iiij=ii*ij;
          cc = in_outK[ik][0]*in_outF[ik][0]-in_outK[ik][1]*in_outF[ik][1];
          in_outF[ik][1] = (in_outK[ik][0]*in_outF[ik][1]+in_outF[ik][0]*in_outK[ik][1])*iiij;
          in_outF[ik][0]=cc*iiij;
          ik++;
          ij=-ij;
       } 
       ii=-ii;
    }
    fftw_execute(planFB);
    ik=0;
    ii=ij=1;
    for(i=fn22-no2; i<=fn22+no2-1; i++){
       for(j=fn22-no2; j<=fn22+no2-1; j++){
          ik1=(i-1)*fn2+j-1;
          ik2=(i-2)*fn2+j-1;
          ik3=(i-2)*fn2+j-2;
          ik4=(i-1)*fn2+j-2;
          iiij=ii*ij;
          FR = 0.25*(in_outF[ik1][0]-in_outF[ik2][0]+in_outF[ik3][0]-in_outF[ik4][0])*iiij;
          FI = 0.25*(in_outF[ik1][1]-in_outF[ik2][1]+in_outF[ik3][1]-in_outF[ik4][1])*iiij;
          Field.at(i - no2 - 1).at(j- no2 - 1) = complex<double>( (FR * cokz - FI * sikz)/fn2/fn2, (FI * cokz + FR * sikz)/fn2/fn2);
          ik++;
          ij=-ij;
       }
       ii=-ii;
    }
    fftw_destroy_plan(planFF);
    fftw_destroy_plan(planFB);
    fftw_destroy_plan(planKF);
    fftw_destroy_plan(planKB);
    fftw_free(in_outF);
    fftw_free(in_outK);
    fftw_cleanup();
    return Field;
}
CMPLXVEC lpspy::Gain( double Isat, double gain, double L, CMPLXVEC Field ){
    double Io, Ii, ampl;;
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            Ii = norm(Field.at(i).at(j));
            if (Isat == 0.0) Io = Ii;
            else Io =  Ii*exp(gain*L/(1 + 2.0 * Ii/Isat));
            if (Ii == 0.0) ampl = 0.0;
            else ampl = sqrt(Io/Ii);
            Field.at(i).at(j) *= ampl;
        }
    }
    return Field;
}
CMPLXVEC lpspy::GaussAperture( double w, double x_shift, double y_shift, double R, CMPLXVEC Field ){
    int n2;
    double x,y,dx,w2,cc,SqrtR,x2,y2;
    n2=(int)N/2;
    w2=w*w*2;
    SqrtR=sqrt(R);
    dx = size/N;
    for (int i=0;i< N; i++){
        x=(i-n2)*dx-x_shift;
        x2=x*x;
        for (int j=0;j< N; j++){
            y=(j-n2)*dx-y_shift;
            y2=y*y;
            cc=SqrtR*exp(-(x2+y2)/w2);
            Field.at(i).at(j) *= cc;
        }
    }
    return Field;
}
CMPLXVEC lpspy::GaussScreen( double w, double x_shift, double y_shift, double T, CMPLXVEC Field ){
    int n2;
    double x,y,dx,w2,cc,x2,y2;
    n2=(int)N/2;
    w2=w*w;
    dx = size/N;
    for (int i=0;i< N; i++){
        x=(i-n2)*dx-x_shift;
        x2=x*x;
        for (int j=0;j< N; j++){
            y=(j-n2)*dx-y_shift;
            y2=y*y;
            cc=sqrt(1-(1-T)*exp(-(x2+y2)/w2));
            Field.at(i).at(j) *= cc;
        }
    }
    return Field;
}
CMPLXVEC lpspy::GaussHermite( int n, int m, double A, double w0, CMPLXVEC Field ){
    int    n2;
    double sqrt2w0,sqrt2xw0,sqrt2yw0,w02,x,y,dx,x2,y2;

    sqrt2w0=sqrt(2.0)/w0;
    w02=w0*w0;
    n2=N/2;
    dx=size/N;

    for (int i=0;i< N; i++){
        x=(i-n2)*dx;
        x2=x*x;
        sqrt2xw0=sqrt2w0*x;
        for (int j=0;j< N; j++){
            y=(j-n2)*dx;
            y2=y*y;
            sqrt2yw0=sqrt2w0*y;
            Field.at(i).at(j) = complex<double> (A*exp(-(x2+y2)/w02)*H(m,sqrt2xw0)*H(n,sqrt2yw0) , 0.0);
        }
    }
    return Field;
}
CMPLXVEC lpspy::GaussLaguerre( int p, int m, double A, double w0, CMPLXVEC Field ){
    int    n2, ma;
    double r,rho,theta,w02,x,y,dx,x2,y2;

    w02=w0*w0;
    n2=N/2;
    dx=size/N;
    ma=abs(m);
    for (int i=0;i< N; i++){
        x=(i-n2)*dx;
        x2=x*x;
        for (int j=0;j< N; j++){
            y=(j-n2)*dx;
            y2=y*y;
            r=sqrt(x2+y2);
            if (r==0.0)
                if (y>0.0) theta=Pi/2;
                else theta=-Pi/2;
            else theta=acos(y/r);
            rho=2*(x2+y2)/w02;
            Field.at(i).at(j) = complex<double>( A*pow((rho/2),ma/2)*Laguerre1(p,m,rho)*exp(-rho/2)*cos(m*theta) , 0.0 );
        }
    }
    return Field;
}
CMPLXVEC lpspy::Lens( double f, double x_shift, double y_shift, CMPLXVEC Field ){
    double x,x2,y,dx,pi2,K;
    int n2;
    if (doub1 != 0.) printf("error in Lens: Spherical coordinates! Use Convert first\n");
    pi2=3.1415926*2.;
    K=pi2/lambda;
    n2=(int) N/2;
    dx=size/N;
    for (int i=0;i< N; i++){
        x=(i-n2)*dx-x_shift;
        x2=x*x;
        for (int j=0;j< N; j++){ 
            double fi;
            y=(j-n2)*dx-y_shift;
            fi=-K*(x2+y*y)/(2.*f);
            Field.at(i).at(j) *= exp(_j * fi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::LensForvard(double f, double z, CMPLXVEC Field ){
    CMPLXVEC FieldTmp;
    double z1,f1,ampl_scale;
    double LARGENUMBER = 10000000.;
    f1=0.;
    if (doub1 !=0. ) f1=1./doub1;
    else f1 = LARGENUMBER * size*size/lambda;
    if( (f+f1) != 0.) f=(f*f1)/(f+f1);
    else f = LARGENUMBER * size*size/lambda;
    if ((z-f) == 0 ) z1 = LARGENUMBER;
    else z1= -z*f/(z-f);

    FieldTmp=Forvard(z1,Field);

    ampl_scale= (f-z)/f ;
    size *= ampl_scale;
    doub1= -1./(z-f);

    if (z1>=0.){
        for (int i=0;i<N; i++){
            for (int j=0;j<N; j++){	
                Field.at(i).at(j) = FieldTmp.at(i).at(j)/ampl_scale;
            }
        }
    }
    else{
        for (int i=0;i<N; i++){
            for (int j=0;j<N; j++){
                int i_i, j_i;
                i_i = N-i-1;
                j_i = N-j-1;
                Field.at(i).at(j) = FieldTmp.at(i_i).at(j_i) / ampl_scale;
            }
        }
    }
    return Field;
}
CMPLXVEC lpspy::LensFresnel(double f, double z, CMPLXVEC Field ){
    double z1,f1,ampl_scale;
    double LARGENUMBER = 10000000.;
    double TINY_NUMBER = 1.0e-100;
    if (f == z) f += TINY_NUMBER;
    f1=0.;
    if (doub1 !=0. ) f1=1./doub1;
    else f1 = LARGENUMBER * size*size/lambda;
    if( (f+f1) != 0.) f=(f*f1)/(f+f1);
    else f = LARGENUMBER * size*size/lambda;

    z1= -z*f/(z-f);
    if (z1 < 0.0){
            cout << "error in LensFresnel: Behind focus" << endl;
            return Field;
    }

    Field=Fresnel(z1,Field);

    ampl_scale= (f-z)/f ;
    size *= ampl_scale;
    doub1= -1./(z-f);

    for (int i=0;i<N; i++){
        for (int j=0;j<N; j++){	
            Field.at(i).at(j) /= ampl_scale;
        }
    }
    return Field;
}
CMPLXVEC lpspy::IntAttenuator( double R, CMPLXVEC Field ){
    double r;
    r=sqrt(R);
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){ 
            Field.at(i).at(j) *= r;
        }
    }
    return Field;
}
CMPLXVEC lpspy::MultIntensity( vector<vector<double> > Intens, CMPLXVEC Field ){
    double Intens2;
    if ((int)Intens.at(0).size() != N || (int)Intens.size() != N){
        printf( "Error in MultIntensity(Intens, Fin): array 'Intens' must be square and must have %d x %d elements\n",N,N);
        return Field;
    }
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            Intens2=sqrt(Intens.at(j).at(i));
            Field.at(i).at(j) *= Intens2;
        }
    }
    return Field;
}
CMPLXVEC lpspy::MultPhase( vector<vector<double> > Phase, CMPLXVEC Field ){
    double phi;
    if ((int)Phase.at(0).size() != N || (int)Phase.size() != N){
        printf( "Error in MultPhase(Phase, Fin): array 'Phase' must be square and must have %d x %d elements\n",N,N);
        return Field;
    }
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            phi=Phase.at(j).at(i);
            Field.at(i).at(j) *= exp(_j * phi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::Normal( CMPLXVEC Field ){
    double sum, dx, dx2, asum;
    sum=0;
    dx =size/N;
    dx2 = dx*dx;
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            sum += norm(Field.at(i).at(j)) * dx2;
        }
    }
    if (sum == 0.0){
        printf("Error in 'Normal(Fin)': Zero beam power!");
        return Field;
    }
    asum=sqrt(1./sum);
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
           Field.at(i).at(j) *= asum;
        }
    }   	
    return Field;
}
CMPLXVEC lpspy::Interpol( double new_size, int new_number, double x_shift, double y_shift, double angle, double magnif, CMPLXVEC Fin ){
    CMPLXVEC Fout;
    Fout.resize(new_number, vector<complex<double> > (new_number));
    double dx_new, dx_old, x_new, x_old, size_old,
       y_new, y_old, lower, upper, ss, cc, x0, y0;
    int i_old, j_old, old_number, on21, nn21;

    size_old = size;
    old_number = N;
    dx_new=new_size/(new_number-1); 
    dx_old=size_old/(old_number-1);
    angle *= Pi/180.;

    on21=(int) old_number/2+1;
    nn21=(int) new_number/2+1;
    lower= (1-on21)*dx_old;
    upper=  (old_number-on21)*dx_old;
    cc=cos(angle);
    ss=sin(angle);	
    for (int i=0;i< new_number; i++){
        for (int j=0;j< new_number; j++){
            x0=(i-nn21+1)*dx_new-x_shift;
            y0=(j-nn21+1)*dx_new-y_shift;
            x_new=(x0*cc+y0*ss)/magnif;
            y_new=(-x0*ss+y0*cc)/magnif; 
            i_old=(int) floor(x_new/dx_old+on21);
            x_old=(i_old-on21)*dx_old; 
            j_old=(int) floor(y_new/dx_old+on21);
            y_old=(j_old-on21)*dx_old;
            if((x_new > lower) && (x_new < upper) && (y_new >lower) && (y_new < upper)){
                Fout.at(i).at(j)= complex<double> (
                    Inv_Squares(x_old, y_old, dx_old,
                        Fin.at(i_old-1).at(j_old-1).real(),
                        Fin.at(i_old).at(j_old-1).real(),
                        Fin.at(i_old-1).at(j_old).real(),
                        Fin.at(i_old).at(j_old).real(),
                        x_new, y_new)/magnif , 
                    Inv_Squares(x_old, y_old, dx_old,
                        Fin.at(i_old-1).at(j_old-1).imag(),
                        Fin.at(i_old).at(j_old-1).imag(),
                        Fin.at(i_old-1).at(j_old).imag(),
                        Fin.at(i_old).at(j_old).imag(),  
                        x_new, y_new)/magnif );
            }
            else{
                Fout.at(i).at(j)= complex<double>(0.0, 0.0);
            }
        }
    }
    N=new_number;
    size=new_size;
    return Fout;
}
vector<vector<double> > lpspy::Intensity(int flag, CMPLXVEC Field ){
    vector<vector<double> > I;
    I.resize(N, vector<double> (N));
    for (int  i=0; i<N; i++)
    {
        for (int  j=0;j<N; j++)
        {
            I.at(i).at(j) = norm(Field.at(j).at(i));	
        }
    }
    if (flag == 0) return I;
    double Imax=0.0;
    for (int  i=0;i<N ; i++){
      for (int  j=0;j<N ; j++){
        if (I.at(i).at(j) > Imax ) Imax=I.at(i).at(j);
      }
    }
    if (Imax == 0.0){
      printf(" in Intensity: cannot normalize because of zero beam power.\n");
      return I;
    }
    double InvImax=1/Imax;
    for (int  i=0;i<N ; i++){
        for (int  j=0;j<N; j++){
            I.at(i).at(j) *= InvImax;
            if (flag == 2 ) I.at(i).at(j) *= 255.0;
        }
    }
    return I;
}
vector<vector<double> > lpspy::Phase(CMPLXVEC Field ){
    vector<vector<double> > Phi;
    Phi.resize(N, vector<double> (N));
    for (int  i=0; i<N; i++)
    {
        for (int  j=0;j<N; j++)
        {
            Phi.at(i).at(j)=arg(Field.at(j).at(i));
        }
    }
    return Phi;
}
vector<vector<double> > lpspy::PhaseUnwrap(vector<vector<double> > Phi ){
    double *x, *y;
    x=(double*)calloc(N*N,sizeof(double));
	if (x == NULL){
        printf("Error in 'PhaseUnwrap(Phi)': unsufficient memory!");
		return Phi;
    }
    y=(double*)calloc(N*N,sizeof(double));
	if (y == NULL){
        printf("Error in 'PhaseUnwrap(Phi)': unsufficient memory!");
        free(x);
		return Phi;
    }    
    int ik=0;
	for(int i=0; i<N; i++){
		for (int j=0; j<N; j++){
		  x[ik]=Phi[i][j];
		  ik++;
		}
	}
	phaseunwrap(x, y ,N, N);
	ik=0;
	for(int i=0; i<N; i++){
		for (int j=0; j<N; j++){
		  Phi[i][j]=y[ik];
		  ik++;
		}
	}
    free(x);
    free(y);
    return Phi;
}
CMPLXVEC lpspy::PipFFT( int ind, CMPLXVEC Field ){
    int i,j;  
    int  ii, ij, iiij;
    long ik;
    fftw_complex* in_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N * N);
    if (in_out == NULL) return Field;
    fftw_plan planF = fftw_plan_dft_2d (N, N, in_out, in_out, FFTW_FORWARD, FFTW_ESTIMATE);
    if (planF == NULL) return Field;
    fftw_plan planB = fftw_plan_dft_2d (N, N, in_out, in_out, FFTW_BACKWARD, FFTW_ESTIMATE);
    if (planB == NULL) return Field;
    ik=0;
    for (i=0;i<N; i++){
        for (j=0;j<N; j++){
            in_out[ik][0] = (double) Field.at(i).at(j).real();
            in_out[ik][1] = (double) Field.at(i).at(j).imag(); 
            ik++;
        }
    }
    int1 += ind;
    if ( int1 != 0 ){ 
        ik=0;
        ii=ij=1;
        for (i=0;i<N; i++){
            for (j=0;j<N; j++){
                iiij=ii*ij;
                in_out[ik][0] *= iiij;
                in_out[ik][1] *= iiij; 
                ik++;
                ij=-ij;
            }
            ii=-ii;
        }
    }
    if (ind == 1)  fftw_execute(planF);
    if (ind == -1) fftw_execute(planB);
    if(int1 == 0){
        ik=0;
        ii=ij=1;
        for (i=0;i<N; i++){    
            for (j=0;j<N; j++ ){
                iiij=ii*ij;
                in_out[ik][0] *= iiij;
                in_out[ik][1] *= iiij;
                ik++;
                ij=-ij;
            }
            ii=-ii;
        }
    }
    ik=0;
    for (i=0;i< N; i++){
        for (j=0;j< N; j++){
            Field.at(i).at(j) = complex<double>(in_out[ik][0] , in_out[ik][1]);
            ik++;
        }
    }
    fftw_destroy_plan(planF);
    fftw_destroy_plan(planB);
    fftw_free(in_out);
    fftw_cleanup();
    return Field;	
}
double lpspy::Power( CMPLXVEC Field ){
    double sum;
    sum=0.0;
    for (int i=0; i< N ;i++){
        for (int j=0;j < N ;j++){
            sum += norm(Field.at(i).at(j));
        }
    }
    return sum;
}
CMPLXVEC lpspy::RectAperture(double sx, double sy, double x_shift, double y_shift, double angle, CMPLXVEC Field ){
    double dx,x,y,x0,y0,cc,ss;
    int i2;
    dx =size/N;
    i2=N/2+1;
    angle *= -Pi/180.;
    cc=cos(angle);
    ss=sin(angle);
    if(angle==0.0){
        for (int i=0;i<N ;i++){
            for (int j=0;j<N ;j++){
                x=(i-i2+1)*dx-x_shift;
                y=(j-i2+1)*dx-y_shift;
                if(fabs(x) > sx/2. || fabs(y) > sy/2. ) {
                    Field.at(i).at(j) = 0.0;
                }
            }
        }
    }
    else{
        for (int i=0;i<N ;i++){
            for (int j=0;j<N ;j++){
                x0=(i-i2+1)*dx-x_shift;
                y0=(j-i2+1)*dx-y_shift;
                x=x0*cc+y0*ss;
                y=-x0*ss+y0*cc; 
                if(fabs(x) > sx/2. || fabs(y) > sy/2. ){
                    Field.at(i).at(j) = 0.0;
                }
            }
        }
    }
    return Field;
}
CMPLXVEC lpspy::RectScreen(double sx, double sy, double x_shift, double y_shift, double angle, CMPLXVEC Field ){
    double dx,x,y,x0,y0,cc,ss;
    int i2;
    dx =size/N;
    i2=N/2+1;
    angle *= -Pi/180.;
    cc=cos(angle);
    ss=sin(angle);
    if(angle==0.0){
        for (int i=0;i<N ;i++){
            for (int j=0;j<N ;j++){
                x=(i-i2+1)*dx-x_shift;
                y=(j-i2+1)*dx-y_shift;
                if(fabs(x) <= sx/2. && fabs(y) <= sy/2. ) {
                    Field.at(i).at(j) = 0.0;
                }
            }
        }
    }
    else {
        for (int i=0;i<N ;i++){
            for (int j=0;j<N ;j++){
                x0=(i-i2+1)*dx-x_shift;
                y0=(j-i2+1)*dx-y_shift;
                x=x0*cc+y0*ss;
                y=-x0*ss+y0*cc; 
                if(fabs(x) <= sx/2. && fabs(y) <= sy/2. ) {
                    Field.at(i).at(j) = 0.0;
                }
            }
        }
    }
    return Field;
}
CMPLXVEC lpspy::RandomIntensity(double seed, double noise_level, CMPLXVEC Field ){
    double rnd_int;
    srand((unsigned int)seed);	
    for (int i=0;i<N ;i++){
        for (int j=0;j<N ;j++){
            rnd_int=((double)rand())/((double) RAND_MAX);
            Field.at(i).at(j) += rnd_int * noise_level;
        }
    }
    return Field;
}
CMPLXVEC lpspy::RandomPhase(double seed, double max, CMPLXVEC Field ){
    double fi;
    srand((unsigned int)seed);	
    for (int i=0;i<N ;i++){
        for (int j=0;j<N ;j++){
            fi=( ((double)rand())/((double) RAND_MAX) - 0.5 )*max;
            Field.at(i).at(j) *= exp(_j * fi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::Steps(double z, int nstep, CMPLXVEC refr, CMPLXVEC Field ){
    double  delta, delta2, Pi4lz, AA, band_pow, K, dist, fi,i_left, i_right;
    std::complex<double> uij, uij1, uij_1, ui1j, ui_1j, medium;
    int i, j, jj, ii;
    int  istep;
    vectors v; //the structure vectors is used to pass a lot of variables to function elim
    if (doub1 !=0.){
        printf("error in 'Steps(z,nsteps, refr, Fin)': Spherical coordinates. Use Fout=Convert(Fin) first.\n");
        return Field;
    }
    v.a.resize(N+3);
    v.b.resize(N+3);
    v.c.resize(N+3);
    v.u.resize(N+3);
    v.u1.resize(N+3);
    v.u2.resize(N+3);
    v.alpha.resize(N+3);
    v.beta.resize(N+3);
    v.p.resize(N+3);

    K=2.*Pi/lambda;
    z=z/2.;
    Pi4lz = 4.*Pi/lambda/z;
    std::complex<double> imPi4lz (0.0,Pi4lz);
    delta=size/((double)(N-1.));
    delta2 = delta*delta;

/* absorption at the borders is described here */
    AA= -10./z/nstep; /* total absorption */
    band_pow=2.;   /* profile of the absorption border, 2=quadratic*/
/* width of the absorption border */
    i_left=N/2+1.0-0.4*N;
    i_right=N/2+1.0+0.4*N;
/* end absorption */

    for ( i=1; i <= N; i++){
        v.u2.at(i) = 0.0;
        v.a.at(i) = std::complex<double>( -1./delta2 , 0.0 );
        v.b.at(i) = std::complex<double>( -1./delta2 , 0.0 );
    }
    medium= 0.0;
    dist =0.;

/*  Main  loop, steps here */
    for(istep = 1; istep <= nstep ; istep ++){
        dist=dist + 2.*z;

/*  Elimination in the direction i, halfstep  */
        for (i=0; i< N; i++){
            for( j=0; j< N; j++){
                double  fi;
                fi=0.25*K*z*(refr.at(i).at(j).real()-1.0);
                Field.at(i).at(j) *= exp(_j * fi);
            }
        }

        for(jj=2; jj <= N-2; jj += 2){
            j=jj;
            for (i=2; i <= N-1; i++){

                uij=Field.at(i-1).at(j-1);
                uij1=Field.at(i-1).at(j);
                uij_1=Field.at(i-1).at(j-2);
                v.p.at(i) = -1.0/delta2 * (uij_1 + uij1 -2.0 * uij) + imPi4lz * uij;           
            }
            for ( i=1; i <= N; i++){
                
                if (refr.at(i-1).at(j-1).imag() == 0.0) medium = std::complex<double> (medium.real() , 0.0);				
                else medium = std::complex<double>(medium.real() , -2.0 * Pi * refr.at(i-1).at(j-1).imag() / lambda);                              

                v.c.at(i) = std::complex<double>( -2.0 / delta2, Pi4lz + medium.imag() );
 
///* absorption borders are formed here */
                if(  i <= i_left){
                    double iii=i_left-i+1;
                    v.c.at(i) = std::complex<double> (v.c.at(i).real() , v.c.at(i).imag() - (AA*K)*pow((double) iii/ ((double)(i_left)),band_pow));
                }

                if(  i >= i_right){ 
                    double iii=i-i_right+1;
                    double im=N-i_right+1;
                    v.c.at(i) = std::complex<double> (v.c.at(i).real() , v.c.at(i).imag() - (AA*K)*pow((double) iii/ ((double)(im)),band_pow));
                }
///* end absorption */
            }

            elim(v,N);
            for ( i=1; i<= N; i++){
                Field.at(i-1).at(j-2) = v.u2.at(i);
                v.u2.at(i)=v.u.at(i);
            }
            j=jj+1;
            for ( i=2; i <= N-1; i++){
                uij=Field.at(i-1).at(j-1);
                uij1=Field.at(i-1).at(j);
                uij_1=Field.at(i-1).at(j-2);
                v.p.at(i) = -1.0/delta2 * (uij_1 + uij1 -2.0 * uij) + imPi4lz * uij;
            }
            for ( i=1; i <= N; i++){
                if (refr.at(i-1).at(j-1).imag() == 0.0) medium = std::complex<double>( medium.real() , 0.0 );
                else medium = std::complex<double>(medium.real() ,  -2.*Pi*refr.at(i-1).at(j-1).imag()/lambda);
                v.c.at(i) = std::complex<double>(-2.0/delta2, Pi4lz + medium.imag());

///* absorption borders are formed here */
                if( i <= i_left){
                    double iii=i_left-i+1;
                    v.c.at(i) = std::complex<double>( v.c.at(i).real() , v.c.at(i).imag() - (AA*K)*pow((double) iii/ ((double)(i_left)),band_pow) );
                }

                if( i >= i_right){ 
                    double iii=i-i_right;
                    double im=N-i_right+1;
                    //c.at(i).imag(c.at(i).imag() - (AA*2.0*K)*pow((double) iii/ ((double)(im)),band_pow)); /* Gleb's original */
                    v.c.at(i) = std::complex<double>(  v.c.at(i).real() , v.c.at(i).imag() - (AA*K)*pow((double) iii/ ((double)(im)),band_pow) );
                }
///* end absorption */
            }
            elim(v,N);
            for ( i=1; i <= N; i++){
                Field.at(i-1).at(j-2) = v.u2.at(i);
                v.u2.at(i)=v.u.at(i);
            }
        }
        for ( i=1; i <= N; i++){
            Field.at(i-1).at(N-1) = v.u2.at(i);
        }
        for ( i=0; i < N; i++){
            for( j=0; j < N; j++){
                fi=0.5*K*z*(refr.at(i).at(j).real()-1.0);
                Field.at(i).at(j) *= exp(_j * fi);
            }
        }

/* Elimination in the j direction is here, halfstep */

        for ( i=1; i <= N; i++){
            v.u2.at(i)=0.0;
        }
        for(ii=2; ii <= N-2; ii += 2){
            i=ii;
            for ( j=2; j <= N-1; j++){
                uij=Field.at(i-1).at(j-1);
                ui1j=Field.at(i).at(j-1);
                ui_1j=Field.at(i-2).at(j-1);
                v.p.at(j) = -1.0/delta2 * (ui_1j + ui1j -2.0 * uij) + imPi4lz * uij;
            }
            for ( j=1; j <= N; j++){
                if (refr.at(i-1).at(j-1).imag() == 0.0) medium =std::complex<double>(medium.real() , 0.0);
                else medium= std::complex<double>( medium.real() , -2.0 * Pi * refr.at(i-1).at(j-1).imag() / lambda );
                v.c.at(j) = std::complex<double>( -2.0 / delta2 , Pi4lz + medium.imag() );	


/* absorption borders are formed here */
                if( j <= i_left){
                    size_t iii=(long)i_left-j;
                    v.c.at(j) = std::complex<double>( v.c.at(j).real() , v.c.at(j).imag() - (AA*K)*pow((double) iii/ ((double)(i_left)),band_pow) );
                }

                if( j >= i_right){ 
                    size_t iii=j-(long)i_right;
                    double im=N-i_right+1;
                    v.c.at(j) = std::complex<double>( v.c.at(j).real() , v.c.at(j).imag() - (AA*K)*pow((double) iii/ ((double)(im)),band_pow) );
                }
//* end absorption */
            }
            elim(v,N);

            for ( j=1; j<= N; j++){
                Field.at(i-2).at(j-1) = v.u2.at(j);
                v.u2.at(j)=v.u.at(j);
            }
            i=ii+1;
            for ( j=2; j <= N-1; j++){
                uij=Field.at(i-1).at(j-1);
                ui1j=Field.at(i).at(j-1);
                ui_1j=Field.at(i-2).at(j-1);
                v.p.at(j) = -1.0/delta2 * (ui_1j + ui1j -2.0 * uij) + imPi4lz * uij;
            }
            for ( j=1; j <= N; j++){
                if (refr.at(i-1).at(j-1).imag() == 0.0) medium = std::complex<double>( medium.real() , 0.0);
                    else medium = std::complex<double>( medium.real() , -2.*Pi*refr.at(i-1).at(j-1).imag()/lambda );
                    v.c.at(j) = std::complex<double>( -2.0/delta2 , Pi4lz + medium.imag() );
/* absorption borders are formed here */
                if( j <= i_left){
                    size_t  iii=(long )i_left-j;
                    v.c.at(j) = std::complex<double>( v.c.at(j).real(), v.c.at(j).imag() - (AA*K)*pow((double) iii/ ((double)(i_left)),band_pow) );
                }

                if( j >= i_right){ 
                    size_t  iii=j-(long )i_right;
                    double im=N-i_right+1;
                    v.c.at(j) = std::complex<double>( v.c.at(j).real() , v.c.at(j).imag() - (AA*K)*pow((double) iii/ ((double)(im)),band_pow) );
                }
/* end absorption */
            }

            elim(v,N);
            for ( j=1; j <= N; j++){
                Field.at(i-2).at(j-1) = v.u2.at(j);
                v.u2.at(j)=v.u.at(j);
            }
        }

        for ( j=2; j <= N; j++){
            Field.at(i-1).at(j-2) = v.u2.at(j);
        }

///* end j */ 

        }
        for ( i=0; i < N; i++){
            for(j=0; j < N; j++){
                fi=0.25*K*z*(refr.at(i).at(j).real()-1.0);
                Field.at(i).at(j) *=  exp(_j * fi);
            }
        }
    return Field;
    
    
}
double lpspy::Strehl( CMPLXVEC Field ){
    double sum,sum1r,sum1i,sum1;

    sum=sum1r=sum1i=0.0;
    for (int i=0; i< N ;i++){
        for (int j=0;j < N ;j++){
            sum += abs(Field.at(i).at(j));
            sum1r += Field.at(i).at(j).real();
            sum1i += Field.at(i).at(j).imag();
        }
    }
    sum1=(sum1r*sum1r+sum1i*sum1i);
    if (sum == 0){
        cout<<"error in Strehl: Zero beam power"<<endl;
        return sum;
    }
    return sum1/sum/sum;
}
CMPLXVEC lpspy::SubIntensity( vector<vector<double> > Intens, CMPLXVEC Field ){
    double Intens2, phi;
    if ((int)Intens.at(0).size() != N || (int)Intens.size() != N){
        printf( "Error in SubIntensity(Intens, Fin): array 'Intens' must be square and must have %d x %d elements\n",N,N);
        exit(1);
    }
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            phi=arg(Field.at(i).at(j));
            Intens2=sqrt(Intens.at(j).at(i));
            Field.at(i).at(j) = Intens2 * exp(_j * phi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::SubPhase( vector<vector<double> > Phase, CMPLXVEC Field ){
    double Intens2, phi;
    if ((int)Phase.at(0).size() != N || (int)Phase.size() != N){
        printf( "Error in SubPhase(Phase, Fin): array 'Phase' must be square and must have %d x %d elements\n",N,N);
        exit(1);
    }
    for (int i=0;i< N; i++){
        for (int j=0;j< N; j++){
            phi=Phase.at(j).at(i);
            Intens2=abs(Field.at(i).at(j));
            Field.at(i).at(j) = Intens2 * exp(_j * phi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::Tilt(double tx, double ty, CMPLXVEC Field ){
    int n2;
    double fi, K, dx, x, y;
    dx =size/N;
    n2=N/2;
    K=2*Pi/lambda;
    for (int i=0;i<N; i++){
        x=(i-n2)*dx;
        for (int j=0;j<N; j++){
            y=(j-n2)*dx;
            fi= -(tx*x+ty*y)*K;
            Field.at(i).at(j) *= exp(_j * fi);
        }
    }
    return Field;
}
CMPLXVEC lpspy::Zernike(int n, int m, double R, double A, CMPLXVEC Field ){
    int  n2, ncheck, ind;
    double rho, phi, fi, K, dx, x, y, Nnm;
    ind=0;
    for(ncheck=n; ncheck >= -n; ncheck -= 2)
    if (ncheck == m ) ind=1;
    if (ind == 0){
        cout << "error in 'Zernike(n ,m, R, A, Fin)': n must be larger than zero, |m| <= n and n-|m| must be even."<<endl;
        return Field;
    }
    K=2*Pi/lambda;
    n2=N/2;
    dx=size/N;
    if (m == 0) Nnm=sqrt((double)n+1);
    else Nnm=sqrt(2.0*(n+1));
    for (int i=0;i< N; i++){
        x=(i-n2)*dx;
        for (int j=0;j< N; j++){
            y=(j-n2)*dx;
            rho=sqrt((x*x+y*y)/(R*R));
            phi=phase(y,x) + Pi;
            fi= -A*K*Nnm*zernike(n,m,rho,phi);
            Field.at(i).at(j) *= exp(_j * fi);
        }
    }
    return Field;
}
void lpspy::test(){
    cout << test_string << endl;
}


double lpspy::getGridSize(){
    return size;
}
void lpspy::setGridSize(double newSize){
    size = newSize;
}
double lpspy::getWavelength(){
    return lambda;
}
void lpspy::setWavelength(double newWavelength){
    lambda = newWavelength;
}
int lpspy::getGridDimension(){
    return N;
}
