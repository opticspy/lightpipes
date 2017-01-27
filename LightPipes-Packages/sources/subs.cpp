#include "subs.h"
#define Pi        3.141592654
#define UNWRAP(ol,co,ne)\
	val = ol;\
	if ((val - co) >= hfactor)\
		while ((val - co) >= hfactor) val -=  factor;\
	else if ((val - co) <= -hfactor)\
		while ((val - co) <= -hfactor) val +=  factor;\
	*ne = val;
double Y1getter(double a)
{
	return a;
}
double H(int n,double x){
       int k;
       double p1,p2,p3;
       p1=1.0;
       p2=0.0;
       if (n == 0 )return 1.0;
          for (k=1;k <=n; k++){
             p3=p2;
             p2=p1;
             p1=2*x*p2-2*(k-1)*p3;
          }
       return p1;
}

double Laguerre1(int p,int m,double rho){
    if (p==0) return 1.0;
    else
        if (p==1) return -1*rho+1+m;
        else
            return (2*p+m-1-rho)/p*Laguerre1(p-1,m,rho) - (p+m-1)/p*Laguerre1(p-2,m,rho);
}

double Laguerre(int p,int m, double rho){
    double L0,L1,LaguerreL;
    int i;
    L1=0.0;
    LaguerreL=1.0;
    for (i=1;i<p+1;i++)
    {
        L0=L1;
        L1=LaguerreL;
        LaguerreL=((2*i-1+m-rho)*L1-(i-1+m)*L0)/i;
    }
    return LaguerreL;
}
            
int factorial(int num){
 if (num==1)
  return 1;
 if (num==0)
     return 1;
 return factorial(num-1)*num;
} 
    
//double C(int p, int m){
    //double pi;
    //pi = 3.1415926;
    //return sqrt(2/(pi*factorial(p)*factorial(m)))*factorial(min(p,m));
//}    
    
 /*
*         Inverse square interpolation : 
*         given square (x,y) (x+dx,y) (x,y+dx) (x+dx,y+dx) 
*         with values   z     zx       zy        zxy 
*         the program returns value for Z for arbitrary 
*         x1 and y1 inside the rectangle.
*/
double Inv_Squares(double x, double y, double dx, double z, double zx, double zy, double zxy, double x1, double y1){
    double tol;
    double s1,s2,s3,s4,xlow,xhigh,ylow,yhigh, sum;
//	char msg[50];
    tol=1e-6*dx;
    if(x1< x-tol || x1>x+dx+tol || y1<y-tol || y1>y+dx+tol){
//		cout<<"Out of Range error."<<endl;
    }

    xlow=x1-x;
    xhigh=x+dx-x1;
    ylow=y1-y;
    yhigh=y+dx-y1;

    if(xlow< -tol || xhigh< -tol || ylow < -tol || yhigh < -tol ){ 
//		cout<<"Out of Range error."<<endl;
    }


    if (fabs(xlow) < tol) return z+ylow*(zy-z)/dx;
    if (fabs(ylow) < tol) return z+xlow*(zx-z)/dx;
    if (fabs(xhigh) < tol) return zx+ylow*(zxy-zx)/dx;
    if (fabs(yhigh) < tol) return zy+xlow*(zxy-zy)/dx;

    s1=1./(xlow*ylow);
    s2=1./(xhigh*ylow);
    s3=1./(xlow*yhigh);
    s4=1./(xhigh*yhigh);


    sum=s1+s2+s3+s4;
    s1=s1/sum;
    s2=s2/sum;
    s3=s3/sum;
    s4=s4/sum;

    return z*s1+zx*s2+zy*s3+zxy*s4;

}
/***************************************************************/
/* Zernike polynomial 

   +-m
  R    as in Born and Volf, p. 465, sixth edition, Pergamon
     n

The implementation have not been optimized for speed.
 
*/
double zernike(int n, int m, double rho, double phi){
	int s, int_sign, mm;
    double sum, product, Factorial(int nn);
    mm=(int) abs(m);
    sum=0;
	product = 1.0;
    int_sign=1;
    for (s=0; s<= (int)((n-mm)/2); s++)
	{
		if(n-2*s != 0) product=pow( rho, (double)(n-2*s) );
		else product =1.0;
		product *= Factorial(n-s)*int_sign;
		product /= Factorial(s)*Factorial(((n+mm)/2)-s)*Factorial(((n-mm)/2)-s);
		sum += product;
		int_sign = -int_sign;
    }
    if(m>=0) return sum*cos(m*phi);
	else return -sum*sin(m*phi);  
}



/* Factorial function */
double Factorial(int n){
    double product;

    if (n<0) {
		fprintf(stderr,"factorial: argument is negative, exiting \n");
		exit(1);
    }
    if (n==0) return 1.;
    else{ 
		product =1;
		while(n>=1){
			product *= n;
			--n;
		}
		return product;
    }
}


double phase(double y,double x){
    if (x !=0.) return atan2 (y,x);
    else if (y>=0) return Pi/2.;
    else return Pi+Pi/2;
}


/*****************************************************************/
/*****************        END of Zernike     *********************/ 
int phaseunwrap(double* ibuffer, double* obuffer,int xsize, int ysize) {
	register short i, j;
	double  *p, *q, *newpix;
	register short hxsize, hysize;
	double comval,oldpix;
	double hfactor, val;
	double factor=2.0*Pi;

	p = ibuffer;
	q = obuffer;

	hxsize = xsize>>1;
	hysize = ysize>>1;
	hfactor = Pi;
/* position p in centre of image */
	p += hysize*xsize + hxsize;
	q += hysize*xsize + hxsize;
/* central pixel */
      *q =*p;
/* first shell of pixels */
	comval = *q;
	oldpix = *(p - xsize);
	newpix = q - xsize;
	UNWRAP(oldpix,comval,newpix);        /* north */

	comval = (*(q - xsize) + *q)/2;
	oldpix = *(p + 1);
	newpix = q + 1;
	UNWRAP(oldpix,comval,newpix);        /* east */

	comval = (*(q + 1) + *q)/2;
	oldpix = *(p + xsize);
	newpix = q + xsize;
	UNWRAP(oldpix,comval,newpix);        /* south */

	comval = (*(q + xsize) + *q)/2;
	oldpix = *(p - 1);
	newpix = q - 1;
	UNWRAP(oldpix,comval,newpix);        /* west */

	comval = (*(q - xsize) + *(q - 1) + *q) / 3;
	oldpix = *(p - xsize - 1);
	newpix = q - xsize - 1;
	UNWRAP(oldpix,comval,newpix);        /* north-west */

	comval = (*(q - xsize) + *(q + 1) + *q) / 3;
	oldpix = *(p - xsize + 1);
	newpix = q - xsize + 1;
	UNWRAP(oldpix,comval,newpix);        /* north-east */

	comval = (*(q + xsize) + *(q + 1) + *q) / 3;
	oldpix = *(p + xsize + 1);
	newpix = q + xsize + 1;
	UNWRAP(oldpix,comval,newpix);        /* south-east */

	comval = (*(q + xsize) + *(q - 1) + *q) / 3;
	oldpix = *(p + xsize - 1);
	newpix = q + xsize - 1;
	UNWRAP(oldpix,comval,newpix);        /* south-west */
/* next shells */
	i = 1;
	while (++i < hxsize) {
	/* north */
		comval = (*(q - (i-1)*xsize - i + 1) + *(q - (i-1)*xsize -
i + 2))/2;
		oldpix = *(p - i*xsize - i + 1);
		newpix = q - i*xsize - i + 1;
		UNWRAP(oldpix,comval,newpix);
		j = i-1;
	    while (--j > -i) {
			comval = (*(q - i*xsize - j - 1) + *(q -
(i-1)*xsize - j) + *(q - (i-1)*xsize - j - 1)) / 3;
			oldpix = *(p - i*xsize - j);
			newpix = q - i*xsize - j;
			UNWRAP(oldpix,comval,newpix);
		}
	/* south */
		comval = (*(q + (i-1)*xsize + i - 1) + *(q + (i-1)*xsize +
i - 2))/2;
		oldpix = *(p + i*xsize + i - 1);
		newpix = q + i*xsize + i - 1;
		UNWRAP(oldpix,comval,newpix);
		j = i-1;
		while (--j > -i) {
			comval = (*(q + i*xsize + j + 1) + *(q +
(i-1)*xsize + j) + *(q + (i-1)*xsize + j + 1)) / 3;
			oldpix = *(p + i*xsize + j);
			newpix = q + i*xsize + j;
			UNWRAP(oldpix,comval,newpix);
		}
	/* east */
		comval = (*(q + i - 1 - (i-1)*xsize) + *(q + i - 1 -
(i-2)*xsize))/2;
		oldpix = *(p + i - (i - 1)*xsize);
		newpix = q + i - (i - 1)*xsize;
		UNWRAP(oldpix,comval,newpix);
		j = i-1;
		while (--j > -i) {
			comval = (*(q + i - (j+1)*xsize) + *(q + i - 1 -
(j+1)*xsize) + *(q + i - 1 - j*xsize)) / 3;
			oldpix = *(p + i - j*xsize);
			newpix = q + i - j*xsize;
			UNWRAP(oldpix,comval,newpix);
		}
	/* west */
		comval = (*(q - i + 1 + (i-1)*xsize) + *(q - i + 1 +
(i-2)*xsize))/2;
		oldpix = *(p - i + (i - 1)*xsize);
		newpix = q - i + (i - 1)*xsize;
		UNWRAP(oldpix,comval,newpix);
		j = i-1;
		while (--j > -i) {
			comval = (*(q - i + (j+1)*xsize) + *(q - i + 1 +
(j+1)*xsize) + *(q - i + 1 + j*xsize)) / 3;
			oldpix = *(p - i + j*xsize);
			newpix = q - i + j*xsize;
			UNWRAP(oldpix,comval,newpix);
		}
	/* north-west */
		comval = (*(q - (i-1)*xsize - i) + *(q - i*xsize - i + 1) +
*(q - (i-1)*xsize - i + 1)) / 3;
		oldpix = *(p - i*xsize - i);
		newpix = q - i*xsize - i;
		UNWRAP(oldpix,comval,newpix);
	/* north-east */
		comval = (*(q - (i-1)*xsize + i) + *(q - i*xsize + i - 1) +
*(q - (i-1)*xsize + i - 1)) / 3;
		oldpix = *(p - i*xsize + i);
		newpix = q - i*xsize + i;
		UNWRAP(oldpix,comval,newpix);
	/* south-east */
		comval = (*(q + (i-1)*xsize + i) + *(q + i*xsize + i - 1) +
*(q + (i-1)*xsize + i - 1)) / 3;
		oldpix = *(p + i*xsize + i);
		newpix = q + i*xsize + i;
		UNWRAP(oldpix,comval,newpix);
	/* south-west */
		comval = (*(q + (i-1)*xsize - i) + *(q + i*xsize - i + 1) +
*(q + (i-1)*xsize - i + 1)) / 3;
		oldpix = *(p + i*xsize - i);
		newpix = q + i*xsize - i;
		UNWRAP(oldpix,comval,newpix);
	}
/* upper line and left column */
	/* upper line*/
	comval = (*(q - (hxsize-1)*xsize - hxsize + 1) + *(q -
(hxsize-1)*xsize - hxsize + 2))/2;
	oldpix = *(p - hxsize*xsize - hxsize + 1);
	newpix = q - hxsize*xsize - hxsize + 1;
	UNWRAP(oldpix,comval,newpix);
	j = hxsize-1;
	while (--j > -hxsize) {
		comval = (*(q - hxsize*xsize - j - 1) + *(q -
(hxsize-1)*xsize - j) + *(q - (hxsize-1)*xsize - j - 1)) / 3;
		oldpix = *(p - hxsize*xsize - j);
		newpix = q - hxsize*xsize - j;
		UNWRAP(oldpix,comval,newpix);
	}
	/* left line */
	comval = (*(q - hxsize + 1 + (hxsize-1)*xsize) + *(q - hxsize + 1 +
(hxsize-2)*xsize))/2;
	oldpix = *(p - hxsize + (hxsize - 1)*xsize);
	newpix = q - hxsize + (hxsize - 1)*xsize;
	UNWRAP(oldpix,comval,newpix);
	j = hxsize-1;
	while (--j > -hxsize) {
		comval = (*(q - hxsize + (j+1)*xsize) + *(q - hxsize + 1 +
(j+1)*xsize) + *(q - hxsize + 1 + j*xsize)) / 3;
		oldpix = *(p - hxsize + j*xsize);
		newpix = q - hxsize + j*xsize;
		UNWRAP(oldpix,comval,newpix);
	}
/* upper left corner */
	comval = (*(q - (hxsize-1)*xsize - hxsize) + *(q - hxsize*xsize -
hxsize + 1) + *(q - (hxsize-1)*xsize - hxsize + 1)) / 3;
	oldpix = *(p - hxsize*xsize - hxsize);
	newpix = q - hxsize*xsize - hxsize;
	UNWRAP(oldpix,comval,newpix);

return 0;
}
/***********************************************************************
*  elim. Called by LPSteps
***********************************************************************/
void elim(vectors &v, int N){
	int i;
	std::complex<double> cc;
/* initial condition, everything is going to be zero at the edge */
	v.alpha.at(2) = 0.0;
	v.beta.at(2) = 0.0;

	v.alpha.at(N) = 0.0;
	v.beta.at(N) = 0.0;

//* forward elimination */
	for(i=2;i <= N-2; i++){
		cc=v.c.at(i) - v.a.at(i) * v.alpha.at(i);
		v.alpha.at(i+1) = v.b.at(i) / cc;
		v.beta.at(i+1)=( v.p.at(i) + v.a.at(i) * v.beta.at(i) ) / cc;
	}
	i=N;
	cc = v.c.at(i) - v.a.at(i) * v.alpha.at(i);
	v.beta.at(N+1) = ( v.p.at(i) + v.a.at(i) * v.beta.at(i) )/cc;
//* edge amplitude =0 */
	v.u.at(N) = v.beta.at(N+1);
//* backward elimination        */
	for(i=N-1; i >= 1; i--){
		v.u.at(i)=v.alpha.at(i+1) * v.u.at(i+1) + v.beta.at(i+1);
	}
}
