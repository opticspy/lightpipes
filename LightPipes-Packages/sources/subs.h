#include <iostream>
#include <math.h>
#include <complex>
#include <vector>
/***********************************************************************
*  structure vectors is used to pass by reference a lot of variables to
*  elim and LPSteps.
***********************************************************************/
struct vectors{
	std::vector<std::complex<double> > a, b, c, alpha, beta, u, p, u1, u2;
};
double Y1getter(double a);
double H(int n,double x);
double Laguerre1(int p,int m,double rho);
double Laguerre(int p, int m, double rho);
int factorial(int num);
double Inv_Squares(double x, double y, double dx, double z, double zx, double zy, double zxy, double x1, double y1);
double zernike(int n, int m, double rho, double phi);
double Factorial(int n);
double phase(double y,double x);
int phaseunwrap(double* ibuffer,double* obuffer,int xsize, int ysize);
void elim(vectors &v,int N);
