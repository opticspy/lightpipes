#include "fresnl.h"
#include "subs.h"
#include <complex>
#include <vector>
#include "fftw3.h"

#define CMPLXVEC vector<vector<complex<double> > >

namespace std {
class lpspy {
    public:
        int  N;
        int int1;
        double size, lambda, doub1;
        lpspy();
        ~lpspy();
        CMPLXVEC Axicon(double phi, double n1, double x_shift, double y_shift, CMPLXVEC Fin);
        CMPLXVEC BeamMix(CMPLXVEC Fin1, CMPLXVEC Fin2 );
        CMPLXVEC Begin(double size, double lambda, int NN);
        CMPLXVEC CircAperture(double R, double x_shift, double y_shift, CMPLXVEC Fin);
        CMPLXVEC CircScreen(double R, double x_shift, double y_shift, CMPLXVEC Fin);
        CMPLXVEC Convert( CMPLXVEC Fin );
        CMPLXVEC Forvard(double z, CMPLXVEC Fin);
        CMPLXVEC Fresnel(double z, CMPLXVEC Fin);
        CMPLXVEC Gain( double Isat, double gain, double L, CMPLXVEC Fin );
        CMPLXVEC GaussAperture( double w, double x_shift, double y_shift, double R, CMPLXVEC Fin );
        CMPLXVEC GaussScreen( double w, double x_shift, double y_shift, double T, CMPLXVEC Fin );
        CMPLXVEC GaussHermite( int n, int m, double A, double w0, CMPLXVEC Fin );
        CMPLXVEC GaussLaguerre( int p, int m, double A, double w0, CMPLXVEC Fin );
        CMPLXVEC IntAttenuator( double R, CMPLXVEC Fin );
        vector<vector<double> > Intensity(int flag,CMPLXVEC Fin );
        CMPLXVEC Interpol( double new_size, int new_number, double x_shift, double y_shift, double angle, double magnif, CMPLXVEC Fin );
        CMPLXVEC Lens( double f, double x_shift, double y_shift, CMPLXVEC Fin );
        CMPLXVEC LensForvard(double f, double z, CMPLXVEC Fin );
        CMPLXVEC LensFresnel(double f, double z, CMPLXVEC Fin );
        CMPLXVEC MultIntensity( vector<vector<double> > Intens, CMPLXVEC Fin );
        CMPLXVEC MultPhase( vector<vector<double> > Phase, CMPLXVEC Fin );
        CMPLXVEC Normal( CMPLXVEC Fin );
        vector<vector<double> > Phase(CMPLXVEC Fin );
        vector<vector<double> > PhaseUnwrap(vector<vector<double> > Phi );
        CMPLXVEC PipFFT( int ind, CMPLXVEC Fin );
        double   Power( CMPLXVEC Fin );
        CMPLXVEC RandomIntensity(double seed, double noise_level, CMPLXVEC Fin );
        CMPLXVEC RandomPhase(double seed, double max, CMPLXVEC Fin );
        CMPLXVEC RectAperture(double sx, double sy, double x_shift, double y_shift, double angle, CMPLXVEC Fin );
        CMPLXVEC RectScreen(double sx, double sy, double x_shift, double y_shift, double angle, CMPLXVEC Fin );        
        CMPLXVEC Steps(double z, int nstep, CMPLXVEC refr, CMPLXVEC Fin );
        double   Strehl( CMPLXVEC Fin );
        CMPLXVEC SubIntensity( vector<vector<double> > Intens, CMPLXVEC Fin );
        CMPLXVEC SubPhase( vector<vector<double> > Phase, CMPLXVEC Fin );
        CMPLXVEC Tilt(double tx, double ty, CMPLXVEC Fin );
        CMPLXVEC Zernike(int n, int m, double R, double A, CMPLXVEC Fin );
        void     test();
        double   getGridSize();
        void     setGridSize(double newSize);
        double   getWavelength();
        void     setWavelength(double newWavelength);
        int      getGridDimension();
    };
}
